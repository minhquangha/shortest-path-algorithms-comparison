def brute_force(graph, start, target, Tmax):
    all_paths = []
    states_visited = 0

    def dfs(current_node, time_so_far, cost_so_far, path, modes, visited):
        nonlocal states_visited

        states_visited += 1
        if current_node == target:
            all_paths.append({
                "path": path.copy(),
                "modes": modes.copy(),
                "time": time_so_far,
                "cost": cost_so_far
            })
            return

        for neighbor, edge_time, edge_cost, mode in graph.get(current_node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                modes.append(mode)

                dfs(
                    neighbor,
                    time_so_far + edge_time,
                    cost_so_far + edge_cost,
                    path,
                    modes,
                    visited
                )

                modes.pop()
                path.pop()
                visited.remove(neighbor)

    dfs(
        current_node=start,
        time_so_far=0,
        cost_so_far=0,
        path=[start],
        modes=[],
        visited={start}
    )

    best_result = None

    for candidate in all_paths:
        if candidate["time"] <= Tmax:
            if best_result is None or candidate["cost"] < best_result["cost"]:
                best_result = candidate

    if best_result is None:
        return None

    best_result["states_visited"] = states_visited
    best_result["total_paths"] = len(all_paths)

    return best_result