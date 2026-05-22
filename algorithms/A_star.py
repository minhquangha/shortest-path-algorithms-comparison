import heapq
from collections import defaultdict


def build_reverse_graph(graph):
    """Xây đồ thị ngược để chạy Dijkstra từ target."""
    reverse = defaultdict(list)
    for u, neighbors in graph.items():
        for (v, t, c, mode) in neighbors:
            reverse[v].append((u, t, c, mode))
    return reverse


def dijkstra_reverse(graph, target):
    """
    Dijkstra ngược từ target, trả về dict h[v] = min cost từ v đến target.
    Dùng làm heuristic cho A* (admissible vì là chi phí thực tối thiểu).
    """
    reverse_graph = build_reverse_graph(graph)

    dist = {}  # dist[v] = min cost từ v -> target
    heap = [(0, target)]  # (cost, node)

    while heap:
        cost, node = heapq.heappop(heap)
        if node in dist:
            continue
        dist[node] = cost

        for (prev, t, c, mode) in reverse_graph.get(node, []):
            if prev not in dist:
                heapq.heappush(heap, (cost + c, prev))

    return dist


def A_star(graph, start, target, Tmax):
    """
    A* tìm đường từ start đến target:
      - Tối thiểu hoá cost
      - Ràng buộc: tổng time <= Tmax

    State: (node, time_so_far)
    f = g + h, trong đó:
      g = cost_so_far
      h = min cost từ node đến target (Dijkstra ngược, admissible)

    Returns dict giống brute_force, hoặc None nếu không tìm được.
    """
    states_visited = 0

    # Precompute heuristic: h[v] = min cost từ v -> target (bỏ qua time constraint)
    h = dijkstra_reverse(graph, target)

    # Nếu target không reachable về cost
    if start not in h and start != target:
        pass  # h.get(start, 0) sẽ trả 0, vẫn chạy được

    # Heap: (f, g, time, node, path, modes)
    # f = g + h(node)
    start_h = h.get(start, 0)
    heap = [(start_h, 0, 0, start, [start], [])]
    #         f       g  time  node  path    modes

    # Visited: (node, time) -> best cost đã thấy
    # Vì time là integer, state space hữu hạn trong [0, Tmax]
    best_cost_at = {}  # (node, time) -> min cost để đạt state này

    best_result = None

    while heap:
        f, g, time_so_far, node, path, modes = heapq.heappop(heap)

        states_visited += 1

        # Pruning: nếu state này đã được visit với cost thấp hơn -> bỏ qua
        state_key = (node, time_so_far)
        if state_key in best_cost_at and best_cost_at[state_key] <= g:
            continue
        best_cost_at[state_key] = g

        # Pruning: nếu lower bound của solution qua state này >= best đã tìm
        if best_result is not None and f >= best_result["cost"]:
            continue

        # Đến đích
        if node == target:
            if time_so_far <= Tmax:
                if best_result is None or g < best_result["cost"]:
                    best_result = {
                        "path": path.copy(),
                        "modes": modes.copy(),
                        "time": time_so_far,
                        "cost": g,
                    }
            continue  # Không cần expand thêm từ target

        # Expand neighbors
        for (neighbor, edge_time, edge_cost, mode) in graph.get(node, []):
            new_time = time_so_far + edge_time
            if new_time > Tmax:
                continue  # Cắt nhánh vi phạm thời gian

            new_g = g + edge_cost
            new_h = h.get(neighbor, 0)
            new_f = new_g + new_h

            # Pruning sớm theo best đã tìm
            if best_result is not None and new_f >= best_result["cost"]:
                continue

            new_state = (neighbor, new_time)
            if new_state in best_cost_at and best_cost_at[new_state] <= new_g:
                continue

            heapq.heappush(heap, (
                new_f,
                new_g,
                new_time,
                neighbor,
                path + [neighbor],
                modes + [mode]
            ))

    if best_result is None:
        return None

    best_result["states_visited"] = states_visited
    return best_result
