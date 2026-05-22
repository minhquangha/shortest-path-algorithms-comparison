import time
import matplotlib.pyplot as plt
import numpy as np

import sys
from pathlib import Path
from time import perf_counter

import pandas as pd
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from data.experiment_graphs import EXPERIMENT_GRAPHS_20
from algorithms.brute_force import brute_force
from algorithms.backtracking import backtracking
from algorithms.branch_and_bound import branch_and_bound
from algorithms.A_star import A_star


def run_benchmark():
    algorithms = [
        ("Brute Force", brute_force),
        ("Backtracking", backtracking),
        ("Branch and Bound", branch_and_bound),
        ("A*", A_star)
    ]

    graph_sizes = sorted({graph["nodes"] for graph in EXPERIMENT_GRAPHS_20})

    # stats[algo_name][size] = list execution times
    stats = {
        name: {size: [] for size in graph_sizes}
        for name, _ in algorithms
    }

    for graph in EXPERIMENT_GRAPHS_20:
        size = graph["nodes"]
        print(f"\nTesting graph size = {size}")
        print(f"  Graph ID: {graph['id']}")

        case = graph

        graph = case["graph"]
        start = case["start"]
        target = case["goal"]
        deadline = case["Tmax"]
        penalty = case["P"]

        for name, algo in algorithms:

            # Skip Brute Force for large graphs
            if name == "Brute Force" and size > 15:
                stats[name][size].append(np.nan)
                continue

            start_time = time.perf_counter()

            algo(graph, start, target, deadline, penalty)

            exec_time = time.perf_counter() - start_time

            stats[name][size].append(exec_time)

    return stats, graph_sizes


def analyze_and_plot(
    stats,
    graph_sizes,
    *,
    include_bruteforce=True,
    use_log_y=True,
    output_path=None,
    print_stats=True,
):
    plt.figure(figsize=(10, 6))

    for algo_name, size_data in stats.items():
        if not include_bruteforce and algo_name == "Brute Force":
            continue

        avg_times = []

        for size in graph_sizes:
            times = size_data[size]

            # bỏ NaN khi tính trung bình
            if len(times) == 0 or np.all(np.isnan(times)):
                avg_time = np.nan
                avg_times.append(avg_time)
                if print_stats:
                    print(
                        f"{algo_name:<20} | Size={size:<3} | "
                        "Avg Time = n/a"
                    )
                continue

            avg_time = np.nanmean(times)
            avg_times.append(avg_time)

            if print_stats:
                print(
                    f"{algo_name:<20} | Size={size:<3} | "
                    f"Avg Time = {avg_time:.6f}s"
                )

        # vẽ line chart
        plt.plot(
            graph_sizes,
            avg_times,
            marker='o',
            linewidth=2,
            label=algo_name
        )

    plt.xlabel("Graph Size (number of nodes)")
    plt.ylabel("Average Execution Time (seconds)")
    plt.title("Algorithm Runtime vs Graph Size")
    plt.legend()
    plt.grid(True)
    plt.xticks(graph_sizes)
    if use_log_y:
        plt.yscale("log")  # dùng log scale khi có Brute Force

    if output_path:
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()
    else:
        plt.show()


if __name__ == "__main__":
    stats, graph_sizes = run_benchmark()

    viz_dir = ROOT_DIR / "visualization"
    plot_with_bruteforce = viz_dir / "exp3_with_bruteforce_logy.png"
    plot_no_bruteforce = viz_dir / "exp3_no_bruteforce.png"

    analyze_and_plot(
        stats,
        graph_sizes,
        include_bruteforce=True,
        use_log_y=True,
        output_path=plot_with_bruteforce,
        print_stats=True,
    )
    analyze_and_plot(
        stats,
        graph_sizes,
        include_bruteforce=False,
        use_log_y=False,
        output_path=plot_no_bruteforce,
        print_stats=False,
    )