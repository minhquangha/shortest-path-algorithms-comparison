# experiments/exp3.py
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
    COMPLEXITY_SUMMARY_CSV,
    MASTER_CSV,
    run_benchmark,
    save_outputs,
)

PLOT_PATH = ROOT_DIR / "visualization" / "complexity_actual_vs_theoretical.png"


def load_results() -> pd.DataFrame:
    required_columns = {
        "case_id",
        "nodes",
        "algorithm",
        "execution_time_s",
        "found",
        "states_visited",
        "actual_complexity_log10",
        "theoretical_complexity_log10",
        "complexity_gap_log10",
    }

    if MASTER_CSV.exists():
        df = pd.read_csv(MASTER_CSV)
        if required_columns.issubset(df.columns):
            return df

    df = run_benchmark()
    save_outputs(df)
    return df


def summarize_complexity(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    for col in (
        "states_visited",
        "actual_complexity_log10",
        "theoretical_complexity_log10",
        "complexity_gap_log10",
    ):
        work[col] = pd.to_numeric(work[col], errors="coerce")

    summary = (
        work.groupby(["nodes", "algorithm"], as_index=False)
        .agg(
            cases=("case_id", "count"),
            solved_cases=("found", "sum"),
            mean_time_s=("execution_time_s", "mean"),
            mean_states=("states_visited", "mean"),
            mean_actual_complexity_log10=("actual_complexity_log10", "mean"),
            mean_theoretical_complexity_log10=("theoretical_complexity_log10", "mean"),
            mean_complexity_gap_log10=("complexity_gap_log10", "mean"),
        )
        .sort_values(["nodes", "algorithm"], ascending=[True, True])
    )
    summary["solve_rate"] = summary["solved_cases"] / summary["cases"]
    return summary


def plot_complexity(summary: pd.DataFrame) -> None:
    nodes_sorted = sorted(summary["nodes"].dropna().unique())

    fig, axes = plt.subplots(1, 3, figsize=(20, 6), sharex=True)

    for algorithm_name, _ in ALGORITHMS:
        algo_df = summary[summary["algorithm"] == algorithm_name].copy()
        algo_df = algo_df.set_index("nodes").reindex(nodes_sorted)

        axes[0].plot(
            nodes_sorted,
            algo_df["mean_actual_complexity_log10"].tolist(),
            marker="o",
            linewidth=2,
            markersize=6,
            label=algorithm_name,
        )

        axes[1].plot(
            nodes_sorted,
            algo_df["mean_theoretical_complexity_log10"].tolist(),
            marker="o",
            linewidth=2,
            markersize=6,
            linestyle="--",
            label=algorithm_name,
        )

        axes[2].plot(
            nodes_sorted,
            algo_df["mean_complexity_gap_log10"].tolist(),
            marker="o",
            linewidth=2,
            markersize=6,
            label=algorithm_name,
        )

    axes[0].set_title("Độ phức tạp thực tế")
    axes[1].set_title("Độ phức tạp lý thuyết")
    axes[2].set_title("Chênh lệch lý thuyết - thực tế")

    axes[0].set_xlabel("Số node")
    axes[1].set_xlabel("Số node")
    axes[2].set_xlabel("Số node")

    axes[0].set_ylabel("log10(proxy)")
    axes[1].set_ylabel("log10(upper bound)")
    axes[2].set_ylabel("log10(gap)")

    for ax in axes:
        ax.set_xticks(nodes_sorted)
        ax.grid(True, linestyle="--", alpha=0.35)
        ax.legend(fontsize=9)

    fig.suptitle("So sánh độ phức tạp thực tế và độ phức tạp lý thuyết", y=1.03)
    fig.tight_layout()

    PLOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PLOT_PATH, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    df = load_results()
    summary = summarize_complexity(df)
    summary.to_csv(COMPLEXITY_SUMMARY_CSV, index=False, encoding="utf-8-sig")
    plot_complexity(summary)

    print(summary.to_string(index=False))
    print(f"\nSaved plot: {PLOT_PATH}")
    print(f"Saved summary CSV: {COMPLEXITY_SUMMARY_CSV}")


if __name__ == "__main__":
    main()