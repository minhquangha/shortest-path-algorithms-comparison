import random
import json
from pathlib import Path

def random_node_name(i):
    return f"N{str(i).zfill(2)}"

def generate_edge(mode):
    if mode == "road":
        return random.randint(5, 12), random.randint(10, 60), mode
    elif mode == "air":
        return random.randint(1, 4), random.randint(150, 350), mode
    elif mode == "ship":
        return random.randint(3, 8), random.randint(60, 180), mode
    else:
        raise ValueError(f"Unknown mode: {mode}")

def generate_graph(num_nodes, graph_id, edge_density="medium", tradeoff=True, cycles=True):
    nodes = ["A"] + [random_node_name(i) for i in range(1, num_nodes - 1)] + ["T"]
    graph = {node: [] for node in nodes}

    positions = {}
    for i, node in enumerate(nodes):
        positions[node] = (i * 2, random.uniform(-10, 10))

    # Đảm bảo luôn có đường từ A -> T
    reference_time = 0

    for i in range(len(nodes) - 1):
        u = nodes[i]
        v = nodes[i + 1]

        if tradeoff:
            for mode in ["road", "air", "ship"]:
                t, c, m = generate_edge(mode)
                graph[u].append((v, t, c, m))

            # dùng ship làm mốc deadline tương đối
            t_ref, _, _ = generate_edge("ship")
            reference_time += t_ref
        else:
            t, c, m = generate_edge("road")
            graph[u].append((v, t, c, m))
            reference_time += t

    # Số cạnh phụ tăng theo số node và mật độ cạnh
    if edge_density == "low":
        extra_edges = num_nodes
    elif edge_density == "medium":
        extra_edges = num_nodes * 2
    elif edge_density == "high":
        extra_edges = num_nodes * 4
    else:
        raise ValueError("edge_density must be low, medium, or high")

    for _ in range(extra_edges):
        u = random.choice(nodes[:-1])
        v = random.choice(nodes[1:])

        if u == v:
            continue

        mode = random.choice(["road", "air", "ship"])
        graph[u].append((v, *generate_edge(mode)))

    # Thêm cycle
    if cycles:
        cycle_edges = num_nodes

        for _ in range(cycle_edges):
            u = random.choice(nodes)
            v = random.choice(nodes)

            if u != v:
                mode = random.choice(["road", "ship"])
                graph[u].append((v, *generate_edge(mode)))

    # Deadline cứng dựa theo reference_time
    Tmax = random.randint(
        max(5, int(reference_time * 0.45)),
        max(6, int(reference_time * 0.75))
    )

    return {
        "id": f"G{str(graph_id).zfill(3)}",
        "size_group": (
            "small" if num_nodes <= 15 else
            "medium" if num_nodes <= 50 else
            "large"
        ),
        "nodes": num_nodes,
        "edge_density": edge_density,
        "tradeoff": tradeoff,
        "cycles": cycles,
        "start": "A",
        "goal": "T",
        "Tmax": Tmax,
        "positions": positions,
        "graph": graph
    }

def generate_dataset_by_sizes(sizes, graphs_per_density=1, start_id=1, seed=42):
    random.seed(seed)
    dataset = []
    graph_id = start_id
    
    for num_nodes in sizes:
        for density in ["low", "medium", "high"]:
            for _ in range(graphs_per_density):
                graph = generate_graph(
                    num_nodes=num_nodes,
                    graph_id=graph_id,
                    edge_density=density,
                    tradeoff=True,
                    cycles=True
                )
                dataset.append(graph)
                graph_id += 1
                
    return dataset

def save_dataset(dataset, path):
    """Lưu tập dữ liệu vào file JSON."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    return path

def load_dataset(path):
    """Tải tập dữ liệu từ file JSON."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Đường dẫn thư mục lưu dữ liệu
DATA_DIR = Path(__file__).resolve().parent

# Khởi tạo và sinh dữ liệu đầy đủ các mức độ quy mô và mật độ cạnh
SMALL_SIZES = [5, 10, 13]
MEDIUM_SIZES = [20, 30, 40, 50]
LARGE_SIZES = [100, 200, 300, 400, 500]

# Sinh từng phân khúc dữ liệu
small_dataset = generate_dataset_by_sizes(SMALL_SIZES, graphs_per_density=1, start_id=1, seed=42)
medium_dataset = generate_dataset_by_sizes(MEDIUM_SIZES, graphs_per_density=1, start_id=len(small_dataset) + 1, seed=43)
large_dataset = generate_dataset_by_sizes(LARGE_SIZES, graphs_per_density=1, start_id=len(small_dataset) + len(medium_dataset) + 1, seed=44)

# File JSON cụ thể cho mỗi quy mô
SMALL_PATH = DATA_DIR / "small_graphs.json"
MEDIUM_PATH = DATA_DIR / "medium_graphs.json"
LARGE_PATH = DATA_DIR / "large_graphs.json"

# Tập dữ liệu gộp tổng hợp để duy trì khả năng tương thích ngược với các file benchmark hiện tại
EXPERIMENT_GRAPHS = small_dataset + medium_dataset + large_dataset

if __name__ == "__main__":
    # Lưu ra 3 file JSON tương ứng với 3 quy mô
    save_dataset(small_dataset, SMALL_PATH)
    save_dataset(medium_dataset, MEDIUM_PATH)
    save_dataset(large_dataset, LARGE_PATH)
    
    # Lưu thêm cả file gộp tổng hợp để tương thích ngược nếu cần
    ALL_PATH = DATA_DIR / "EXPERIMENT_GRAPHS.json"
    save_dataset(EXPERIMENT_GRAPHS, ALL_PATH)
    
    print("Successfully generated and saved multi-modal graph datasets!")
    print(f"1. SMALL scale ({len(small_dataset)} graphs): {SMALL_PATH}")
    print(f"2. MEDIUM scale ({len(medium_dataset)} graphs): {MEDIUM_PATH}")
    print(f"3. LARGE scale ({len(large_dataset)} graphs): {LARGE_PATH}")
    print(f"4. Total combined ({len(EXPERIMENT_GRAPHS)} graphs): {ALL_PATH}")
