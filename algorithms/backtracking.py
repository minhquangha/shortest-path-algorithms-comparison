from algorithms.utils import compute_total_cost

def backtracking(graph, start, target, deadline, penalty):
    best_result = None
    states_visited = 0

    def dfs(current_node, time_so_far, cost_so_far, path):
        nonlocal best_result, states_visited

        states_visited += 1

        current_total_cost = compute_total_cost(time_so_far, cost_so_far, deadline, penalty)
        if best_result is not None and current_total_cost >= best_result["total_cost"]:
            return

        if current_node == target:
            if best_result is None or current_total_cost < best_result["total_cost"]:
                best_result = {
                    "path": path.copy(),
                    "time": time_so_far,
                    "cost": cost_so_far,
                    "total_cost": current_total_cost,
                    "states_visited": states_visited,
                }
            return

        for neighbor, time, cost, mode in graph.get(current_node, []):
            if neighbor not in path:
                dfs(
                    neighbor,
                    time_so_far + time,
                    cost_so_far + cost,
                    path + [neighbor],
                )

    dfs(start, 0, 0, [start])
    return best_result