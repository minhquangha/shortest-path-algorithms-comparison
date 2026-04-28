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
        ("Backtracking", backtracking)
    ]

    results = []

    for name, algo in algorithms:
        print(f"Running {name}...")

        start_time = time.perf_counter()

        result = algo(graph, start, target, deadline, penalty)

        end_time = time.perf_counter()
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

if __name__ == "__main__":
    results = run_benchmark()

    print("\nBenchmark Results:")
    print("-" * 60)
    print(f"{'Algorithm':20} {'Time(s)':10} {'States':10} {'Cost'}")

    for row in results:
        print(f"{row[0]:20} {row[1]:<10.6f} {row[2]:<10} {row[3]}")