import random


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

    # Số cạnh phụ tăng theo số node
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

    # Deadline cứng
    # Chọn Tmax dựa theo reference_time để không quá dễ cũng không quá khó
    Tmax = random.randint(
        max(5, int(reference_time * 0.45)),
        max(6, int(reference_time * 0.75))
    )

    return {
        "id": f"G{str(graph_id).zfill(3)}",
        "size_group": (
            "small" if num_nodes <= 15 else
            "medium" if num_nodes <= 35 else
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


def generate_dataset_step_5(
    min_nodes=5,
    max_nodes=50,
    step=5,
    graphs_per_size=3,
    seed=42
):
    random.seed(seed)

    dataset = []
    graph_id = 1

    for num_nodes in range(min_nodes, max_nodes + 1, step):
        for _ in range(graphs_per_size):

            if num_nodes <= 15:
                density = "low"
            elif num_nodes <= 35:
                density = "medium"
            else:
                density = "high"

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


EXPERIMENT_GRAPHS = generate_dataset_step_5(
    min_nodes=5,
    max_nodes=50,
    step=5,
    graphs_per_size=3,
    seed=42
)
for i in EXPERIMENT_GRAPHS:
    print(i)
