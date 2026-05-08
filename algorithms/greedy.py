from algorithms.utils import compute_total_cost

def greedy(graph, start, target, deadline, penalty):
    current = start
    time_so_far = 0
    cost_so_far = 0
    path = [start]
    visited = set([start])

    states_visited = 0

    while current != target:
        states_visited += 1

        candidates = []

        for neighbor, time, cost, mode in graph.get(current, []):
            if neighbor not in visited:
                candidates.append((cost, time, neighbor))

        if not candidates:
            return None


        candidates.sort(key=lambda x: x[0])
        cost, time, next_node = candidates[0]


        cost_so_far += cost
        time_so_far += time
        current = next_node

        path.append(current)
        visited.add(current)

    total_cost = compute_total_cost(
        time_so_far,
        cost_so_far,
        deadline,
        penalty
    )

    return {
        "path": path,
        "time": time_so_far,
        "cost": cost_so_far,
        "total_cost": total_cost,
        "states_visited": states_visited
    }