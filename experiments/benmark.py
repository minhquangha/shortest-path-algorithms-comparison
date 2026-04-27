import time
import csv

from data.sample_graph import get_graph_tradeoff
from algorithms.brute_force import brute_force
from algorithms.backtracking import backtracking
from algorithms.branch_and_bound import branch_and_bound
from algorithms.A_star import A_star


def run_benchmark():
    graph = get_graph_tradeoff()

    start = "A"
    target = "D"
    deadline = 5
    penalty = 50

    algorithms = [
        ("Brute Force", brute_force),
        ("Backtracking", backtracking),
        ("Branch and Bound", branch_and_bound),
        ("A_star", A_star),
    ]

    results = []

    for name, algo in algorithms:
        print(f"Running {name}...")

        start_time = time.time()

        result = algo(graph, start, target, deadline, penalty)

        end_time = time.time()
        exec_time = end_time - start_time

        if result is None:
            results.append([name, exec_time, 0, None])
        else:
            results.append([
                name,
                exec_time,
                result["states_visited"],
                result["total_cost"]
            ])

    return results