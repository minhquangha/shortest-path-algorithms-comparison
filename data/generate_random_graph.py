import random

def generate_random_graph(n=6):
    nodes = [chr(65+i) for i in range(n)]
    graph = {node: [] for node in nodes}

    for u in nodes:
        for v in nodes:
            if u != v and random.random() < 0.3:
                time = random.randint(1, 10)
                cost = random.randint(50, 300)
                mode = random.choice(["road", "water", "air"])
                graph[u].append((v, time, cost, mode))

    return graph