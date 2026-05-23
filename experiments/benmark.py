from __future__ import annotations

import importlib
import io
import math
import random
import sys
from contextlib import redirect_stdout
from pathlib import Path
from time import perf_counter
from typing import Any

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from algorithms.A_star import a_star
from algorithms.aco import aco
from algorithms.backtracking import backtracking
from algorithms.brute_force import brute_force
from algorithms.dp import dynamic_programming

DATA_MODULE_CANDIDATES = (
    "data.experiment_graphs",
    "data.experiment_graphs_20_static",
)

ALGORITHMS = [
    ("Brute Force", brute_force),
    ("Backtracking", backtracking),
    ("A*", a_star),
    ("ACO", aco),
    ("DP", dynamic_programming),
]


MASTER_CSV = ROOT_DIR / "experiments" / "benchmark_results.csv"
RUNTIME_SUMMARY_CSV = ROOT_DIR / "experiments" / "benchmark_runtime_summary.csv"
COMPLEXITY_SUMMARY_CSV = ROOT_DIR / "experiments" / "benchmark_complexity_summary.csv"


def load_dataset() -> list[dict[str, Any]]:

    last_error: Exception | None = None

    for module_name in DATA_MODULE_CANDIDATES:
        try:
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                module = importlib.import_module(module_name)
        except Exception as exc:  
            last_error = exc
            continue

        for attr_name in ("EXPERIMENT_GRAPHS", "EXPERIMENT_GRAPHS_20"):
            dataset = getattr(module, attr_name, None)
            if isinstance(dataset, list) and dataset:
                return dataset

    raise RuntimeError(
        "Không tải được dataset từ data/experiment_graphs.py hoặc data/experiment_graphs_20_static.py"
    ) from last_error


def normalize_graph(graph: dict[str, list[tuple[Any, ...]]]) -> dict[str, list[tuple[Any, ...]]]:
    normalized = {node: list(edges) for node, edges in graph.items()}
    for edges in graph.values():
        for neighbor, *_ in edges:
            normalized.setdefault(neighbor, [])
    return normalized


def graph_metrics(graph: dict[str, list[tuple[Any, ...]]]) -> dict[str, float]:
    node_count = len(graph)
    edge_count = sum(len(edges) for edges in graph.values())
    avg_branching = edge_count / node_count if node_count else 0.0
    max_branching = max((len(edges) for edges in graph.values()), default=0)

    return {
        "node_count": float(node_count),
        "edge_count": float(edge_count),
        "avg_branching_factor": float(avg_branching),
        "max_branching_factor": float(max_branching),
    }


def safe_log10(x: float) -> float:
    return math.log10(max(float(x), 1.0))


def log10_factorial(n: int) -> float:
    if n <= 1:
        return 0.0
    return sum(math.log10(i) for i in range(2, n + 1))


def run_algorithm(
    algorithm_name: str,
    algorithm_fn,
    graph: dict[str, list[tuple[Any, ...]]],
    start: str,
    target: str,
    deadline: int,
    case_index: int,
) -> dict[str, Any] | None:
    if algorithm_name == "Brute Force":
        return algorithm_fn(graph, start, target, deadline)

    if algorithm_name == "Backtracking":
        return algorithm_fn(graph, start, target, deadline)

    if algorithm_name == "A*":
        return algorithm_fn(graph, start, target, deadline)

    if algorithm_name == "ACO":
        state = random.getstate()
        random.seed(10_000 + case_index)
        try:
            return algorithm_fn(graph, start, target, deadline)
        finally:
            random.setstate(state)

    if algorithm_name == "DP":
        return algorithm_fn(graph, start, target, deadline)

    raise ValueError(f"Unknown algorithm: {algorithm_name}")


def actual_complexity_units(
    algorithm_name: str,
    case: dict[str, Any],
    metrics: dict[str, float],
    elapsed_s: float,
    result: dict[str, Any] | None,
) -> tuple[float, str]:

    if algorithm_name == "ACO":
        n = int(metrics["node_count"])
        ants = min(n, 50)
        iterations = max(100, n * 5)
        depth_proxy = max(1, int(case["nodes"]) - 1)
        estimated_ops = ants * iterations * max(1.0, metrics["avg_branching_factor"]) * depth_proxy
        return float(max(estimated_ops, 1.0)), "estimated_ops_aco"

    states_visited = None if result is None else result.get("states_visited")
    if isinstance(states_visited, (int, float)) and states_visited > 0:
        return float(states_visited), "states_visited"

    return float(max(elapsed_s * 1_000_000.0, 1.0)), "runtime_microseconds"


def theoretical_complexity_log10(
    algorithm_name: str,
    case: dict[str, Any],
    metrics: dict[str, float],
) -> float:

    n = max(1, int(metrics["node_count"]))
    e = max(1, int(metrics["edge_count"]))
    max_b = max(1.0, metrics["max_branching_factor"])
    depth = max(1, int(case["nodes"]) - 1)
    tmax = max(1, int(case["Tmax"]))

    if algorithm_name == "Brute Force":
        return log10_factorial(n)

    if algorithm_name == "Backtracking":
        return depth * math.log10(max_b)

    if algorithm_name == "A*":
        # O((V + E) log V + V * Tmax * log(V * Tmax))
        val = (n + e) * math.log2(max(2.0, n)) + n * tmax * math.log2(max(2.0, n * tmax))
        return math.log10(max(1.0, val))

    if algorithm_name == "ACO":
        ants = min(n, 50)  # K
        iterations = max(100, n * 5)  # I
        # O(I * K * V * D)
        return (
            math.log10(iterations)
            + math.log10(ants)
            + math.log10(n)
            + math.log10(depth)
        )

    if algorithm_name == "DP":
        # O(Tmax * (V + E))
        val = tmax * (n + e)
        return math.log10(max(1.0, val))

    raise ValueError(f"Unknown algorithm: {algorithm_name}")


def run_benchmark() -> pd.DataFrame:
    dataset = load_dataset()
    rows: list[dict[str, Any]] = []

    for case_index, case in enumerate(dataset):
        graph = normalize_graph(case["graph"])
        metrics = graph_metrics(graph)

        start = case["start"]
        target = case["goal"]
        deadline = int(case["Tmax"])
        nodes = int(case["nodes"])

        for algorithm_name, algorithm_fn in ALGORITHMS:
            if algorithm_name == "Brute Force" and nodes > 15:
                continue

            # if algorithm_name == "Backtracking" and nodes > 50:
            #     continue

            print(f"Running {algorithm_name} on {case['id']}...")

            t0 = perf_counter()
            result = run_algorithm(
                algorithm_name=algorithm_name,
                algorithm_fn=algorithm_fn,
                graph=graph,
                start=start,
                target=target,
                deadline=deadline,
                case_index=case_index,
            )
            elapsed_s = max(perf_counter() - t0, 1e-12)

            path = None if result is None else result.get("path")
            total_cost = None if result is None else result.get("total_cost", result.get("cost"))
            states_visited = None if result is None else result.get("states_visited")
            found = result is not None

            actual_units, actual_kind = actual_complexity_units(
                algorithm_name=algorithm_name,
                case=case,
                metrics=metrics,
                elapsed_s=elapsed_s,
                result=result,
            )
            theoretical_log10 = theoretical_complexity_log10(
                algorithm_name=algorithm_name,
                case=case,
                metrics=metrics,
            )

            rows.append(
                {
                    "case_id": case.get("id", f"case_{case_index:03d}"),
                    "nodes": nodes,
                    "size_group": case.get("size_group"),
                    "edge_density": case.get("edge_density"),
                    "tradeoff": case.get("tradeoff"),
                    "cycles": case.get("cycles"),
                    "start": start,
                    "goal": target,
                    "deadline": deadline,
                    "algorithm": algorithm_name,
                    "execution_time_s": elapsed_s,
                    "found": found,
                    "states_visited": states_visited,
                    "total_cost": total_cost,
                    "path": None if path is None else str(path),
                    "node_count": metrics["node_count"],
                    "edge_count": metrics["edge_count"],
                    "avg_branching_factor": metrics["avg_branching_factor"],
                    "max_branching_factor": metrics["max_branching_factor"],
                    "actual_complexity_units": actual_units,
                    "actual_complexity_log10": safe_log10(actual_units),
                    "actual_complexity_kind": actual_kind,
                    "theoretical_complexity_log10": theoretical_log10,
                    "complexity_gap_log10": theoretical_log10 - safe_log10(actual_units),
                }
            )

    return pd.DataFrame(rows)


def summarize_runtime(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work["execution_time_s"] = pd.to_numeric(work["execution_time_s"], errors="coerce")
    work["states_visited"] = pd.to_numeric(work["states_visited"], errors="coerce")

    summary = (
        work.groupby("algorithm", as_index=False)
        .agg(
            cases=("case_id", "count"),
            solved_cases=("found", "sum"),
            mean_time_s=("execution_time_s", "mean"),
            min_time_s=("execution_time_s", "min"),
            max_time_s=("execution_time_s", "max"),
            mean_states_visited=("states_visited", "mean"),
            mean_actual_complexity_log10=("actual_complexity_log10", "mean"),
            mean_theoretical_complexity_log10=("theoretical_complexity_log10", "mean"),
            mean_complexity_gap_log10=("complexity_gap_log10", "mean"),
        )
        .sort_values("mean_time_s", ascending=True)
    )
    summary["solve_rate"] = summary["solved_cases"] / summary["cases"]
    return summary


def summarize_complexity(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    for col in ("actual_complexity_log10", "theoretical_complexity_log10", "complexity_gap_log10"):
        work[col] = pd.to_numeric(work[col], errors="coerce")

    summary = (
        work.groupby(["nodes", "algorithm"], as_index=False)
        .agg(
            cases=("case_id", "count"),
            solved_cases=("found", "sum"),
            mean_time_s=("execution_time_s", "mean"),
            mean_actual_complexity_log10=("actual_complexity_log10", "mean"),
            mean_theoretical_complexity_log10=("theoretical_complexity_log10", "mean"),
            mean_complexity_gap_log10=("complexity_gap_log10", "mean"),
        )
        .sort_values(["nodes", "algorithm"], ascending=[True, True])
    )
    summary["solve_rate"] = summary["solved_cases"] / summary["cases"]
    return summary


def save_outputs(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    MASTER_CSV.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(MASTER_CSV, index=False, encoding="utf-8-sig")

    runtime_summary = summarize_runtime(df)
    runtime_summary.to_csv(RUNTIME_SUMMARY_CSV, index=False, encoding="utf-8-sig")

    complexity_summary = summarize_complexity(df)
    complexity_summary.to_csv(COMPLEXITY_SUMMARY_CSV, index=False, encoding="utf-8-sig")

    return runtime_summary, complexity_summary


def main() -> None:
    df = run_benchmark()
    runtime_summary, complexity_summary = save_outputs(df)

    print("\nRuntime summary:")
    print("-" * 120)
    print(
        f"{'Algorithm':16} {'Cases':>6} {'Solved':>6} {'Mean Time(s)':>14} "
        f"{'Min Time(s)':>12} {'Max Time(s)':>12} {'Mean States':>12}"
    )
    for _, row in runtime_summary.iterrows():
        print(
            f"{row['algorithm'][:16]:16} "
            f"{int(row['cases']):6d} "
            f"{int(row['solved_cases']):6d} "
            f"{row['mean_time_s']:14.8f} "
            f"{row['min_time_s']:12.8f} "
            f"{row['max_time_s']:12.8f} "
            f"{row['mean_states_visited']:12.2f}"
        )

    print("\nComplexity summary (mean by nodes):")
    print("-" * 120)
    print(
        f"{'Nodes':>6} {'Algorithm':16} {'Cases':>6} {'Solved':>6} "
        f"{'Actual log10':>14} {'Theory log10':>14} {'Gap log10':>12}"
    )
    for _, row in complexity_summary.iterrows():
        print(
            f"{int(row['nodes']):6d} "
            f"{row['algorithm'][:16]:16} "
            f"{int(row['cases']):6d} "
            f"{int(row['solved_cases']):6d} "
            f"{row['mean_actual_complexity_log10']:14.6f} "
            f"{row['mean_theoretical_complexity_log10']:14.6f} "
            f"{row['mean_complexity_gap_log10']:12.6f}"
        )

    print(f"\nSaved master CSV: {MASTER_CSV}")
    print(f"Saved runtime summary CSV: {RUNTIME_SUMMARY_CSV}")
    print(f"Saved complexity summary CSV: {COMPLEXITY_SUMMARY_CSV}")


if __name__ == "__main__":
    main()