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

from data.experiment_graphs_20_static import EXPERIMENT_GRAPHS_20
from algorithms.brute_force import brute_force
from algorithms.backtracking import backtracking
from algorithms.branch_and_bound import branch_and_bound
from algorithms.A_star import A_star

ALGORITHMS = [
("Brute Force", brute_force),
("Backtracking", backtracking),
("Branch and Bound", branch_and_bound),
("A_star", A_star),
]

DETAILS_CSV = ROOT_DIR / "visualization" / "exp2_runtime_results.csv"
SUMMARY_CSV = ROOT_DIR / "visualization" / "exp2_runtime_summary.csv"
PLOT_PATH = ROOT_DIR / "visualization" / "exp2_runtime_vs_nodes.png"

def run_benchmark():
    rows = []
    for case in EXPERIMENT_GRAPHS_20:
        graph = case["graph"]
        start = case["start"]
        target = case["goal"]
        deadline = case["Tmax"]
        penalty = case["P"]
        nodes = case["nodes"]

        for algorithm_name, algorithm_fn in ALGORITHMS:
            if algorithm_name == "Brute Force" and nodes > 15:
                continue

            print(f"Running {algorithm_name} on {case['id']}...")

            t0 = perf_counter()
            result = algorithm_fn(graph, start, target, deadline, penalty)
            elapsed = perf_counter() - t0

            rows.append({
                "case_id": case["id"],
                "size_group": case["size_group"],
                "tradeoff": case["tradeoff"],
                "nodes": nodes,
                "algorithm": algorithm_name,
                "execution_time_s": elapsed,
                "found": result is not None,
                "states_visited": None if result is None else result.get("states_visited"),
                "total_cost": None if result is None else result.get("total_cost"),
                "path": None if result is None else str(result.get("path")),
            })

    return pd.DataFrame(rows)

def summarize_by_nodes(df: pd.DataFrame) -> pd.DataFrame:
    work_df = df.copy()
    work_df["execution_time_s"] = pd.to_numeric(work_df["execution_time_s"], errors="coerce")
    work_df["nodes"] = pd.to_numeric(work_df["nodes"], errors="coerce")
    summary = (
        work_df.groupby(["nodes", "algorithm"], as_index=False).agg(
            mean_time_s=("execution_time_s", "mean"),
            min_time_s=("execution_time_s", "min"),
            max_time_s=("execution_time_s", "max"),
            solved_cases=("found", "sum"),
            cases=("case_id", "count"),
        ).sort_values(["nodes", "algorithm"], ascending=[True, True])
    )

    summary["solve_rate"] = summary["solved_cases"] / summary["cases"]
    return summary

def save_outputs(df: pd.DataFrame) -> pd.DataFrame:
    DETAILS_CSV.parent.mkdir(parents=True, exist_ok=True)
    PLOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DETAILS_CSV, index=False, encoding="utf-8-sig")
    summary = summarize_by_nodes(df)
    summary.to_csv(SUMMARY_CSV, index=False, encoding="utf-8-sig")
    return summary

def plot_runtime_by_nodes(summary: pd.DataFrame):
    plt.figure(figsize=(11, 6))

    nodes_sorted = sorted(summary["nodes"].dropna().unique())

    for algorithm_name in [name for name, _ in ALGORITHMS]:
        algo_df = summary[summary["algorithm"] == algorithm_name].copy()
        algo_df = algo_df.set_index("nodes").reindex(nodes_sorted)

        plt.plot(
            nodes_sorted,
            algo_df["mean_time_s"].tolist(),
            marker="o",
            linewidth=2,
            markersize=7,
            label=algorithm_name,
        )

    plt.xlabel("Số node")
    plt.ylabel("Thời gian chạy trung bình (giây, thang log)")

    plt.title("So sánh thời gian chạy trung bình theo số node")

    plt.xticks(nodes_sorted)

    plt.yscale("log")

    plt.grid(True, which="both", linestyle="--", alpha=0.4)

    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOT_PATH, dpi=300, bbox_inches="tight")
    plt.show()

def main():
    df = run_benchmark()
    summary = save_outputs(df)
    print("\nBenchmark Results by Number of Nodes:")
    print("-" * 110)
    print(
        f"{'Nodes':>6} {'Algorithm':18} {'Cases':>6} {'Solved':>6} "
        f"{'Mean Time(s)':>14} {'Min Time(s)':>12} {'Max Time(s)':>12}"
    )

    for _, row in summary.iterrows():
        print(
            f"{int(row['nodes']):6d} "
            f"{row['algorithm'][:18]:18} "
            f"{int(row['cases']):6d} "
            f"{int(row['solved_cases']):6d} "
            f"{row['mean_time_s']:14.8f} "
            f"{row['min_time_s']:12.8f} "
            f"{row['max_time_s']:12.8f}"
        )

    print(f"\nSaved detail CSV: {DETAILS_CSV}")
    print(f"Saved summary CSV: {SUMMARY_CSV}")

    plot_runtime_by_nodes(summary)
    print(f"Saved plot: {PLOT_PATH}")

if __name__ == "__main__":
    main()