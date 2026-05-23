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
COMBINED_PATH = ROOT_DIR / "visualization" / "complexity_all_algorithms.png"


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
            from experiments.benmark import theoretical_complexity_log10
            new_theories = []
            for _, row in df.iterrows():
                case_dict = {"nodes": row["nodes"], "Tmax": row["deadline"]}
                metrics_dict = {
                    "node_count": row["node_count"],
                    "edge_count": row["edge_count"],
                    "max_branching_factor": row["max_branching_factor"]
                }
                theory_val = theoretical_complexity_log10(
                    row["algorithm"],
                    case_dict,
                    metrics_dict
                )
                new_theories.append(theory_val)
            df["theoretical_complexity_log10"] = new_theories
            df["complexity_gap_log10"] = df["theoretical_complexity_log10"] - df["actual_complexity_log10"]
            df.to_csv(MASTER_CSV, index=False)
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


# --- Formulas that EXACTLY match the code in benmark.py ---
# Brute Force:  log10(V!)                            => O(V!)
# Backtracking: D * log10(B_max)                     => O(B_max^D)
# A*:           (V+E)logV + V*Tmax*log(V*Tmax)       => O((V+E)logV + V*Tmax*log(V*Tmax))
# ACO:          log10(I) + log10(K) + log10(V) + log10(D) => O(I * K * V * D)
# DP:           Tmax * (V+E)                         => O(Tmax * (V + E))

FORMULAS = {
    "Brute Force": r"$O(V!)$",
    "Backtracking": r"$O(B_{max}^{\,D})$",
    "A*": r"$O((V\!+\!E)\log V + V \cdot T_{max} \log(V \cdot T_{max}))$",
    "ACO": r"$O(I \cdot K \cdot V \cdot D)$",
    "DP": r"$O(T_{max} \cdot (V\!+\!E))$",
}

COLOR_MAP = {
    "A*": '#4C72B0',
    "Backtracking": '#DD8452',
    "ACO": '#55A868',
    "DP": '#C44E52',
    "Brute Force": '#8172B3'
}
MARKER_MAP = {
    "A*": 'o',
    "Backtracking": 's',
    "ACO": '^',
    "DP": 'd',
    "Brute Force": 'X'
}


def plot_complexity(summary: pd.DataFrame) -> None:
    """Combined overview plot (1x2)."""
    nodes_sorted = sorted(summary["nodes"].dropna().unique())

    fig, axes = plt.subplots(1, 2, figsize=(15, 6.5), sharex=True)

    for algorithm_name, _ in ALGORITHMS:
        algo_df = summary[summary["algorithm"] == algorithm_name].copy()
        algo_df = algo_df.set_index("nodes").reindex(nodes_sorted)

        # Plot Actual Complexity
        axes[0].plot(
            nodes_sorted,
            algo_df["mean_actual_complexity_log10"].tolist(),
            marker=MARKER_MAP.get(algorithm_name, 'o'),
            linewidth=2.5,
            markersize=7,
            label=algorithm_name,
            color=COLOR_MAP.get(algorithm_name)
        )

        # Plot Theoretical Complexity
        label_with_formula = f"{algorithm_name}  {FORMULAS.get(algorithm_name, '')}"
        axes[1].plot(
            nodes_sorted,
            algo_df["mean_theoretical_complexity_log10"].tolist(),
            marker=MARKER_MAP.get(algorithm_name, 'o'),
            linewidth=2.5,
            markersize=7,
            linestyle="--",
            label=label_with_formula,
            color=COLOR_MAP.get(algorithm_name)
        )

    axes[0].set_title("Thuc te (Actual)", fontsize=12, fontweight='bold', pad=10)
    axes[1].set_title("Ly thuyet (Theoretical)", fontsize=12, fontweight='bold', pad=10)

    for ax in axes:
        ax.set_xlabel("So node (thang Log)", fontsize=11, fontweight='bold', labelpad=10)
        ax.set_xscale("log")
        ax.set_xticks(nodes_sorted)
        ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
        ax.set_xticklabels([str(int(n)) for n in nodes_sorted], fontsize=9)
        ax.grid(True, which="both", linestyle="--", alpha=0.4)
        ax.legend(fontsize=9, loc="best", framealpha=0.9)

    axes[0].set_ylabel("log10(don vi do phuc tap)", fontsize=11, fontweight='bold')
    axes[1].set_ylabel("log10(gioi han tren ly thuyet)", fontsize=11, fontweight='bold')

    fig.suptitle("So sanh do phuc tap thuc te va ly thuyet (Tong hop)", fontsize=14, fontweight='bold', y=1.02)
    fig.tight_layout()

    PLOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PLOT_PATH, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_complexity_combined(summary: pd.DataFrame) -> None:
    """Combined 5-row figure: one row per algorithm, 2 subplots each (Actual | Theoretical)."""

    algo_order = [name for name, _ in ALGORITHMS]  # Brute Force, Backtracking, A*, ACO, DP

    fig, all_axes = plt.subplots(5, 2, figsize=(15, 28))

    for row_idx, algorithm_name in enumerate(algo_order):
        algo_df = summary[summary["algorithm"] == algorithm_name].copy()

        # Skip if this algorithm has no valid solved cases
        if algo_df.empty or algo_df["solved_cases"].sum() == 0:
            for ax in all_axes[row_idx]:
                ax.set_visible(False)
            continue

        # Only plot node sizes where this algorithm has data
        algo_df = algo_df.dropna(subset=["mean_actual_complexity_log10"])
        if algo_df.empty:
            for ax in all_axes[row_idx]:
                ax.set_visible(False)
            continue

        algo_nodes = sorted(algo_df["nodes"].unique())
        color = COLOR_MAP.get(algorithm_name, '#333333')
        marker = MARKER_MAP.get(algorithm_name, 'o')
        formula = FORMULAS.get(algorithm_name, '')

        ax_actual = all_axes[row_idx][0]
        ax_theory = all_axes[row_idx][1]

        # 1. Actual Complexity
        ax_actual.plot(
            algo_nodes,
            algo_df["mean_actual_complexity_log10"].tolist(),
            marker=marker,
            linewidth=2.5,
            markersize=7,
            label="Thuc te (Actual)",
            color=color
        )
        ax_actual.set_ylabel("log10(actual)", fontsize=10, fontweight='bold')
        ax_actual.set_title(f"{algorithm_name} - Thuc te", fontsize=11, fontweight='bold', pad=8)

        # 2. Theoretical Complexity
        ax_theory.plot(
            algo_nodes,
            algo_df["mean_theoretical_complexity_log10"].tolist(),
            marker=marker,
            linewidth=2.5,
            markersize=7,
            linestyle="--",
            label=f"Ly thuyet: {formula}",
            color=color
        )
        ax_theory.set_ylabel("log10(theoretical)", fontsize=10, fontweight='bold')
        ax_theory.set_title(f"{algorithm_name} - Ly thuyet  {formula}", fontsize=11, fontweight='bold', pad=8)

        for ax in (ax_actual, ax_theory):
            ax.set_xlabel("So node", fontsize=10, fontweight='bold', labelpad=6)
            ax.set_xscale("log")
            ax.set_xticks(algo_nodes)
            ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
            ax.set_xticklabels([str(int(n)) for n in algo_nodes], fontsize=9)
            ax.grid(True, which="both", linestyle="--", alpha=0.4)
            ax.legend(fontsize=9, loc="best", framealpha=0.9)

    fig.suptitle(
        "Phan tich do phuc tap tung thuat toan (Thuc te vs Ly thuyet)",
        fontsize=15, fontweight='bold', y=0.995
    )
    fig.tight_layout(rect=[0, 0, 1, 0.98])

    COMBINED_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(COMBINED_PATH, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Da luu bieu do ghep tai: {COMBINED_PATH}")


def main() -> None:
    df = load_results()
    summary = summarize_complexity(df)
    summary.to_csv(COMPLEXITY_SUMMARY_CSV, index=False, encoding="utf-8-sig")
    plot_complexity(summary)
    plot_complexity_combined(summary)

    print(summary.to_string(index=False))
    print(f"\nSaved plot: {PLOT_PATH}")
    print(f"Saved summary CSV: {COMPLEXITY_SUMMARY_CSV}")


if __name__ == "__main__":
    main()