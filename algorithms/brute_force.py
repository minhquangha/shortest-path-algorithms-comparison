from algorithms.utils import compute_total_cost

def brute_force(graph, start, target, deadline, penalty):
    best_result = None
    states_visited = 0

    def dfs(current_node, time_so_far, cost_so_far, path, visited):
        nonlocal best_result, states_visited

        states_visited += 1

        if current_node == target:
            total_cost = compute_total_cost(
                time_so_far,
                cost_so_far,
                deadline,
                penalty
            )

            if best_result is None or total_cost < best_result["total_cost"]:
                best_result = {
                    "path": path.copy(),
                    "time": time_so_far,
                    "cost": cost_so_far,
                    "total_cost": total_cost,
                }

            return

        for neighbor, time, cost, mode in graph.get(current_node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)

                dfs(
                    neighbor,
                    time_so_far + time,
                    cost_so_far + cost,
                    path,
                    visited
                )

                path.pop()
                visited.remove(neighbor)

    dfs(start, 0, 0, [start], {start})

    if best_result is not None:
        best_result["states_visited"] = states_visited

    return best_result

