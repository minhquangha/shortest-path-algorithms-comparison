from algorithms.utils import compute_total_cost

def A_star(graph, start, target, deadline, penalty):
    import heapq

    def dijkstra_min_time(graph_in, start_node):
        dist = {node: float('inf') for node in graph_in}
        dist[start_node] = 0
        pq = [(0, start_node)]
        while pq:
            curr_time, node = heapq.heappop(pq)
            if curr_time > dist[node]:
                continue
            for neighbor, time, cost, mode in graph_in.get(node, []):
                new_time = curr_time + time
                if new_time < dist[neighbor]:
                    dist[neighbor] = new_time
                    heapq.heappush(pq, (new_time, neighbor))
        return dist

    def dijkstra_min_cost(graph_in, start_node):
        dist = {node: float('inf') for node in graph_in}
        dist[start_node] = 0
        pq = [(0, start_node)]
        while pq:
            curr_cost, node = heapq.heappop(pq)
            if curr_cost > dist[node]:
                continue
            for neighbor, time, cost, mode in graph_in.get(node, []):
                new_cost = curr_cost + cost
                if new_cost < dist[neighbor]:
                    dist[neighbor] = new_cost
                    heapq.heappush(pq, (new_cost, neighbor))
        return dist

    def reverse_graph(graph_in):
        rev = {node: [] for node in graph_in}
        for u in graph_in:
            for (v, time, cost, mode) in graph_in[u]:
                if v not in rev:
                    rev[v] = []
                rev[v].append((u, time, cost, mode))
        return rev

    reverse_g = reverse_graph(graph)
    min_time_to_target = dijkstra_min_time(reverse_g, target)
    min_cost_to_target = dijkstra_min_cost(reverse_g, target)

    def heuristic(node, current_time, current_cost):
        est_time = current_time + min_time_to_target.get(node, float('inf'))
        est_cost = current_cost + min_cost_to_target.get(node, float('inf'))
        return compute_total_cost(est_time, est_cost, deadline, penalty)

    # Nếu dùng heuristic là khoảng cách Euclid thì sửa thành
    # import math
    # def heuristic(node, current_time, current_cost):
    #     g_n = compute_total_cost(current_time, current_cost, deadline, penalty)
    #     x1, y1 = positions[node]
    #     x2, y2 = positions[target]
    #     h_n = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    #     return g_n + h_n
    # và sửa def A_star(graph, start, target, deadline, penalty):
    # thành def A_star(graph, start, target, deadline, penalty, positions):
    # Sau đó sửa run_benchmark

    pq = []
    counter = 0
    states_visited = 0
    start_f = heuristic(start, 0, 0)
    heapq.heappush(pq, (start_f, counter, 0, 0, start, [start]))
    visited_states = {node: [] for node in graph}
    while pq:
        f_score, _, time_so_far, cost_so_far, current_node, path = heapq.heappop(pq)
        states_visited += 1
        if current_node == target:
            return {
                "path": path.copy(),
                "time": time_so_far,
                "cost": cost_so_far,
                "total_cost": compute_total_cost(time_so_far, cost_so_far, deadline, penalty),
                "states_visited": states_visited
            }
        is_dominated = False
        for (v_time, v_cost) in visited_states.get(current_node, []):
            if v_time <= time_so_far and v_cost <= cost_so_far:
                is_dominated = True
                break
        if is_dominated:
            continue
        visited_states[current_node].append((time_so_far, cost_so_far))
        for neighbor, edge_time, edge_cost, mode in graph.get(current_node, []):
            if neighbor not in path:
                new_time = time_so_far + edge_time
                new_cost = cost_so_far + edge_cost
                new_f = heuristic(neighbor, new_time, new_cost)
                if new_f != float('inf'):
                    counter += 1
                    heapq.heappush(pq, (new_f, counter, new_time, new_cost, neighbor, path + [neighbor]))
                    # Nếu muốn lưu cả mode thì sửa if neighbor not in path: thành if neighbor not in path[0::2]: và
                    # heapq.heappush(pq, (new_f, counter, new_time, new_cost, neighbor, path + [mode, neighbor]))
    return None
