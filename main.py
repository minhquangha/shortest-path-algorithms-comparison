from data.sample_graph import get_graph_tradeoff
from algorithms.brute_force import brute_force


def main():
    graph = get_graph_tradeoff()

    start = "A"
    target = "D"
    deadline = 5
    penalty = 50

    result = brute_force(
        graph,
        start,
        target,
        deadline,
        penalty
    )

    print("RESULT:")
    print(result)


if __name__ == "__main__":
    main()