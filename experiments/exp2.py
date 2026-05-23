# experiments/exp2.py
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from experiments.benmark import (
    ALGORITHMS,
    MASTER_CSV,
    RUNTIME_SUMMARY_CSV,
    run_benchmark,
    save_outputs,
)

PLOT_PATH = ROOT_DIR / "visualization" / "runtime_vs_nodes.png"


def load_results() -> pd.DataFrame:
    required_columns = {
        "case_id",
        "nodes",
        "algorithm",
        "execution_time_s",
        "found",
        "states_visited",
    }

    if MASTER_CSV.exists():
        df = pd.read_csv(MASTER_CSV)
        if required_columns.issubset(df.columns):
            return df

    df = run_benchmark()
    save_outputs(df)
    return df


def summarize_runtime_by_nodes(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work["execution_time_s"] = pd.to_numeric(work["execution_time_s"], errors="coerce")
    work["nodes"] = pd.to_numeric(work["nodes"], errors="coerce")
    work["states_visited"] = pd.to_numeric(work["states_visited"], errors="coerce")

    summary = (
        work.groupby(["nodes", "algorithm"], as_index=False)
        .agg(
            cases=("case_id", "count"),
            solved_cases=("found", "sum"),
            mean_time_s=("execution_time_s", "mean"),
            min_time_s=("execution_time_s", "min"),
            max_time_s=("execution_time_s", "max"),
            mean_states_visited=("states_visited", "mean"),
        )
        .sort_values(["nodes", "algorithm"], ascending=[True, True])
    )
    summary["solve_rate"] = summary["solved_cases"] / summary["cases"]
    return summary


def plot_runtime(summary: pd.DataFrame) -> None:
    plt.figure(figsize=(12, 6.5))
    nodes_sorted = sorted(summary["nodes"].dropna().unique())

    # Map color and marker styles for consistency and visual clarity
    color_map = {
        "A*": '#4C72B0',
        "Backtracking": '#DD8452',
        "ACO": '#55A868',
        "DP": '#C44E52',
        "Brute Force": '#8172B3'
    }
    marker_map = {
        "A*": 'o',
        "Backtracking": 's',
        "ACO": '^',
        "DP": 'd',
        "Brute Force": 'X'
    }

    for algorithm_name, _ in ALGORITHMS:
        algo_df = summary[summary["algorithm"] == algorithm_name].copy()
        algo_df = algo_df.set_index("nodes").reindex(nodes_sorted)

        plt.plot(
            nodes_sorted,
            algo_df["mean_time_s"].tolist(),
            marker=marker_map.get(algorithm_name, 'o'),
            linewidth=2.5,
            markersize=7,
            label=algorithm_name,
            color=color_map.get(algorithm_name)
        )

    plt.xlabel("Số node (Quy mô đồ thị, thang Log)", fontsize=12, fontweight='bold', labelpad=10)
    plt.ylabel("Thời gian chạy trung bình (giây, thang Log)", fontsize=12, fontweight='bold', labelpad=10)
    plt.title("So sánh thời gian chạy trung bình theo số node", fontsize=14, fontweight='bold', pad=15)
    
    # Use logarithmic scale for X-axis because of wide-ranging node sizes (5 to 500)
    plt.xscale("log")
    plt.yscale("log")
    
    # Custom formatting for log X-axis ticks to display actual node sizes
    plt.xticks(nodes_sorted, labels=[str(int(n)) for n in nodes_sorted], fontsize=10)
    plt.yticks(fontsize=10)
    
    # Double-grid lines for easy log reading
    plt.grid(True, which="both", linestyle="--", alpha=0.4)
    
    plt.legend(fontsize=10, loc="lower right", framealpha=0.9, facecolor='white', edgecolor='#ddd')
    plt.tight_layout()

    PLOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(PLOT_PATH, dpi=300, bbox_inches="tight")
    plt.close()


def main() -> None:
    df = load_results()
    summary = summarize_runtime_by_nodes(df)
    summary.to_csv(RUNTIME_SUMMARY_CSV, index=False, encoding="utf-8-sig")
    plot_runtime(summary)

    print(summary.to_string(index=False))
    print(f"\nSaved plot: {PLOT_PATH}")
    print(f"Saved summary CSV: {RUNTIME_SUMMARY_CSV}")


if __name__ == "__main__":
    main()