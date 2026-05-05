from data.experiment_graphs_20_static import EXPERIMENT_GRAPHS_20
from algorithms.brute_force import brute_force
from algorithms.backtracking import backtracking

for case in EXPERIMENT_GRAPHS_20:
    result = brute_force(
        graph=case["graph"],
        start=case["start"],
        target=case["goal"],
        deadline=case["Tmax"],
        penalty=case["P"],
    )

    print(case["id"], result)