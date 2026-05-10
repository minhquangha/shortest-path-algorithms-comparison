from __future__ import annotations

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

DETAILS_CSV = ROOT_DIR / "experiments" / "benchmark_results.csv"
SUMMARY_CSV = ROOT_DIR / "experiments" / "benchmark_summary.csv"


def run_benchmark():
    rows = []

    for case in EXPERIMENT_GRAPHS_20:
        graph = case["graph"]
        start = case["start"]
        target = case["goal"]
        deadline = case["Tmax"]
        penalty = case["P"]

        for algorithm_name, algorithm_fn in ALGORITHMS:
            if algorithm_name == "Brute Force" and case["nodes"] > 15:
                print(
                    f"Skipping {algorithm_name} on {case['id']} (nodes={case['nodes']})"
                )
                continue

            print(f"Running {algorithm_name} on {case['id']}...")

            t0 = perf_counter()
            result = algorithm_fn(graph, start, target, deadline, penalty)
            elapsed = perf_counter() - t0

            row = {
                "case_id": case["id"],
                "size_group": case["size_group"],
                "tradeoff": case["tradeoff"],
                "nodes": case["nodes"],
                "algorithm": algorithm_name,
                "execution_time_s": elapsed,
                "states_visited": None,
                "total_cost": None,
                "found": result is not None,
                "path": None,
            }

            if result is not None:
                row["states_visited"] = result.get("states_visited")
                row["total_cost"] = result.get("total_cost")
                row["path"] = str(result.get("path"))

            rows.append(row)

    return pd.DataFrame(rows)


def summarize_results(df: pd.DataFrame) -> pd.DataFrame:
    work_df = df.copy()

    for col in ["execution_time_s", "states_visited", "total_cost"]:
        work_df[col] = pd.to_numeric(work_df[col], errors="coerce")

    summary = (
        work_df.groupby("algorithm", as_index=False)
        .agg(
            cases=("case_id", "count"),
            solved_cases=("found", "sum"),
            mean_time_s=("execution_time_s", "mean"),
            min_time_s=("execution_time_s", "min"),
            max_time_s=("execution_time_s", "max"),
            mean_states=("states_visited", "mean"),
            mean_total_cost=("total_cost", "mean"),
        )
        .sort_values("mean_time_s", ascending=True)
    )

    summary["solve_rate"] = summary["solved_cases"] / summary["cases"]
    return summary


def save_outputs(df: pd.DataFrame) -> pd.DataFrame:
    DETAILS_CSV.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(DETAILS_CSV, index=False, encoding="utf-8-sig")
    summary = summarize_results(df)
    summary.to_csv(SUMMARY_CSV, index=False, encoding="utf-8-sig")

    return summary


def main():
    df = run_benchmark()
    summary = save_outputs(df)

    print("\nBenchmark Results:")
    print("-" * 110)
    print(
        f"{'Algorithm':18} {'Cases':>6} {'Solved':>6} {'Mean Time(s)':>14} "
        f"{'Min Time(s)':>12} {'Max Time(s)':>12} {'Mean States':>12} {'Mean Cost':>12}"
    )

    for _, row in summary.iterrows():
        print(
            f"{row['algorithm'][:18]:18} "
            f"{int(row['cases']):6d} "
            f"{int(row['solved_cases']):6d} "
            f"{row['mean_time_s']:14.8f} "
            f"{row['min_time_s']:12.8f} "
            f"{row['max_time_s']:12.8f} "
            f"{row['mean_states']:12.2f} "
            f"{row['mean_total_cost']:12.2f}"
        )

    print(f"\nSaved detail CSV: {DETAILS_CSV}")
    print(f"Saved summary CSV: {SUMMARY_CSV}")


if __name__ == "__main__":
    main()

# Benchmark Results:
# --------------------------------------------------------------------------------------------------------------
# Algorithm           Cases Solved   Mean Time(s)  Min Time(s)  Max Time(s)  Mean States    Mean Cost
# Backtracking           24     24     0.00002745   0.00001580   0.00007420        16.33       187.92
# Brute Force            24     24     0.00003799   0.00002590   0.00014520        21.67       187.92
# A_star                 24     24     0.00007247   0.00003710   0.00011930         3.88       187.92
# Branch and Bound       24     24     0.00007900   0.00005120   0.00013220         3.67       187.92