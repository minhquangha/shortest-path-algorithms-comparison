def a_star(graph, start, target, Tmax):

    import heapq
    from collections import defaultdict

    def build_reverse_graph(graph):
        reverse = defaultdict(list)
        for u, neighbors in graph.items():
            for (v, t, c, mode) in neighbors:
                reverse[v].append((u, t, c, mode))
        return reverse

    def dijkstra_reverse(graph, target):
        reverse_graph = build_reverse_graph(graph)
        dist = {} 
        heap = [(0, target)]  
        while heap:
            cost, node = heapq.heappop(heap)
            if node in dist:
                continue
            dist[node] = cost
            for (prev, t, c, mode) in reverse_graph.get(node, []):
                if prev not in dist:
                    heapq.heappush(heap, (cost + c, prev))
        return dist

    states_visited = 0
    h = dijkstra_reverse(graph, target)
    if start not in h and start != target:
        pass 
    start_h = h.get(start, 0)
    heap = [(start_h, 0, 0, start, [start], [])]
    best_cost_at = {} 
    best_result = None

    while heap:
        f, g, time_so_far, node, path, modes = heapq.heappop(heap)
        states_visited += 1
        state_key = (node, time_so_far)
        if state_key in best_cost_at and best_cost_at[state_key] <= g:
            continue
        best_cost_at[state_key] = g
        if best_result is not None and f >= best_result["cost"]:
            continue
        if node == target:
            if time_so_far <= Tmax:
                if best_result is None or g < best_result["cost"]:
                    best_result = {
                        "path": path.copy(),
                        "modes": modes.copy(),
                        "time": time_so_far,
                        "cost": g,
                    }
            continue
        for (neighbor, edge_time, edge_cost, mode) in graph.get(node, []):
            new_time = time_so_far + edge_time
            if new_time > Tmax:
                continue
            new_g = g + edge_cost
            new_h = h.get(neighbor, 0)
            new_f = new_g + new_h
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
