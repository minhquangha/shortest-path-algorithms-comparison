def dynamic_programming(graph, start, target, Tmax):
    INF = float("inf")


    nodes = list(graph.keys())


    dp = {
        node: [INF] * (Tmax + 1)
        for node in nodes
    }


    parent = {
        node: [None] * (Tmax + 1)
        for node in nodes
    }

    dp[start][0] = 0

    states_visited = 0


    for current_time in range(Tmax + 1):
        for current_node in nodes:


            if dp[current_node][current_time] == INF:
                continue

            states_visited += 1

            for neighbor, edge_time, edge_cost, mode in graph[current_node]:

                new_time = current_time + edge_time


                if new_time > Tmax:
                    continue

                new_cost = dp[current_node][current_time] + edge_cost


                if new_cost < dp[neighbor][new_time]:
                    dp[neighbor][new_time] = new_cost
                    parent[neighbor][new_time] = (
                        current_node,
                        current_time,
                        mode
                    )


    best_time = None
    best_cost = INF

    for time in range(Tmax + 1):
        if dp[target][time] < best_cost:
            best_cost = dp[target][time]
            best_time = time

    if best_time is None:
        return None


    path = []
    modes = []

    current_node = target
    current_time = best_time

    while current_node != start:
        path.append(current_node)

        prev_info = parent[current_node][current_time]

        if prev_info is None:
            return None

        prev_node, prev_time, mode = prev_info

        modes.append(mode)

        current_node = prev_node
        current_time = prev_time

    path.append(start)
    path.reverse()
    modes.reverse()

    return {
        "path": path,
        "modes": modes,
        "time": best_time,
        "cost": best_cost,
        "states_visited": states_visited
    }