from algorithms.utils import compute_total_cost
def branch_and_bound(graph, start, target, deadline, penalty):
    best_result = None
    import heapq
    def dijkstra_min_time(graph, start):
        dist = {node: float('inf') for node in graph}
        dist[start] = 0
        pq = [(0, start)]

        while pq:
            curr_time, node = heapq.heappop(pq)
            if curr_time > dist[node]:
                continue
            for neighbor, time, cost, mode in graph.get(node, []):
                new_time = curr_time + time
                if new_time < dist[neighbor]:
                    dist[neighbor] = new_time
                    heapq.heappush(pq, (new_time, neighbor))
        return dist
    def dijkstra_min_cost(graph, start):
        dist = {node: float('inf') for node in graph}
        dist[start] = 0
        pq = [(0, start)]

        while pq:
            curr_cost, node = heapq.heappop(pq)
            if curr_cost > dist[node]:
                continue
            for neighbor, time, cost, mode in graph.get(node, []):
                new_cost = curr_cost + cost
                if new_cost < dist[neighbor]:
                    dist[neighbor] = new_cost
                    heapq.heappush(pq, (new_cost, neighbor))
        return dist
    def reverse_graph(graph):
        rev = {node: [] for node in graph}

        for u in graph:
            for (v, time, cost, mode) in graph[u]:
                rev[v].append((u, time, cost, mode))

        return rev
    reverse_g = reverse_graph(graph)
    min_time_to_target = dijkstra_min_time(reverse_g, target)
    min_cost_to_target = dijkstra_min_cost(reverse_g, target)
    def bound(current_node, time_so_far, cost_so_far):
        estimated_time = time_so_far + min_time_to_target.get(current_node, float('inf'))
        estimated_cost = cost_so_far + min_cost_to_target.get(current_node, float('inf'))
        return compute_total_cost(estimated_time, estimated_cost, deadline, penalty)
    def backtrack(current_node, time_so_far, cost_so_far, path):
        nonlocal best_result
        
        current_total_cost = compute_total_cost(time_so_far, cost_so_far, deadline, penalty)
        if best_result is not None and bound(current_node, time_so_far, cost_so_far) >= best_result["total_cost"]:
            return
        if current_node == target:
            if best_result is None or current_total_cost < best_result["total_cost"]:
                best_result = {
                    "path": path.copy(),
                    "time": time_so_far,
                    "cost": cost_so_far,
                    "total_cost": current_total_cost,
                    "states_visited": len(path) // 2 + 1
                }
        for neighbor, time, cost, mode in graph.get(current_node, []):
            if neighbor not in path:
                backtrack(
                    neighbor,
                    time_so_far + time,
                    cost_so_far + cost,
                    path + [mode] + [neighbor]
                )
    backtrack(start, 0, 0, [start])
    return best_result