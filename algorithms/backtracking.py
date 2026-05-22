def backtracking(graph, start, target, deadline, penalty):
    best_result = None
    states_visited = 0

    def dfs(current_node, time_so_far, cost_so_far, path):
        nonlocal best_result, states_visited

        if time_so_far > deadline:
            return

        states_visited += 1

        if best_result is not None and cost_so_far >= best_result["cost"]:
            return

        if current_node == target:
            if best_result is None or cost_so_far < best_result["cost"]:
                best_result = {
                    "path": path.copy(),
                    "time": time_so_far,
                    "cost": cost_so_far,
                    "total_cost": cost_so_far,
                    "states_visited": states_visited,
                }
            return

        for neighbor, time, cost, mode in graph.get(current_node, []):
            if neighbor not in path:
                next_time = time_so_far + time
                if next_time <= deadline:
                    dfs(
                        neighbor,
                        next_time,
                        cost_so_far + cost,
                        path + [neighbor],
                    )

    dfs(start, 0, 0, [start])
    return best_result