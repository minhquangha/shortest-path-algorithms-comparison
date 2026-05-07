from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

RESULTS_CSV = ROOT_DIR / "experiments" / "benchmark_results.csv"
TIME_PNG = ROOT_DIR / "visualization" / "execution_time_comparison.png"
STATES_PNG = ROOT_DIR / "visualization" / "states_visited_comparison.png"


def load_results(csv_path: Path = RESULTS_CSV) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file kết quả: {csv_path}")

    df = pd.read_csv(csv_path)
    df["execution_time_s"] = pd.to_numeric(df["execution_time_s"], errors="coerce")
    df["states_visited"] = pd.to_numeric(df["states_visited"], errors="coerce")
    df["total_cost"] = pd.to_numeric(df["total_cost"], errors="coerce")
    return df


def plot_bar(summary: pd.DataFrame, x_col: str, y_col: str, title: str, ylabel: str, output_path: Path):
    plt.figure(figsize=(10, 6))
    plt.bar(summary[x_col].astype(str), summary[y_col])
    plt.title(title)
    plt.xlabel("Algorithm")
    plt.ylabel(ylabel)
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.show()


def plot_comparison(csv_path: Path = RESULTS_CSV):
    df = load_results(csv_path)

    summary = (
        df.groupby("algorithm", as_index=False)
        .agg(
            mean_time_s=("execution_time_s", "mean"),
            mean_states=("states_visited", "mean"),
        )
        .sort_values("mean_time_s", ascending=True)
    )

    plot_bar(
        summary,
        x_col="algorithm",
        y_col="mean_time_s",
        title="So sánh thời gian chạy trung bình",
        ylabel="Execution time (seconds)",
        output_path=TIME_PNG,
    )

    plot_bar(
        summary,
        x_col="algorithm",
        y_col="mean_states",
        title="So sánh số trạng thái duyệt trung bình",
        ylabel="States visited",
        output_path=STATES_PNG,
    )

    return summary


def main():
    summary = plot_comparison()
    print(summary.to_string(index=False))
    print(f"\nSaved plot: {TIME_PNG}")
    print(f"Saved plot: {STATES_PNG}")


if __name__ == "__main__":
    main()

#        algorithm  mean_time_s  mean_states
#     Backtracking     0.000027    16.333333
#      Brute Force     0.000038    21.666667
#           A_star     0.000072     3.875000
# Branch and Bound     0.000079     3.666667