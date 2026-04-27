# data/sample_graph.py

def get_graph_case_1():
    """
    Graph đơn giản (test đúng)
    """
    return {
        "A": [("B", 2, 100, "road"), ("C", 6, 50, "water")],
        "B": [("D", 3, 200, "air")],
        "C": [("D", 2, 60, "water")],
        "D": []
    }


def get_graph_tradeoff():
    """
    Graph có trade-off (QUAN TRỌNG NHẤT)
    """
    return {
        "A": [
            ("B", 2, 200, "air"),    # nhanh - đắt
            ("C", 6, 50, "water")    # chậm - rẻ
        ],
        "B": [("D", 2, 200, "air")],
        "C": [("D", 2, 50, "water")],
        "D": []
    }


def get_graph_complex():
    """
    Graph phức tạp để benchmark
    """
    return {
        "A": [("B", 2, 100, "road"), ("C", 4, 80, "road"), ("D", 1, 300, "air")],
        "B": [("E", 3, 120, "road"), ("F", 5, 200, "air")],
        "C": [("E", 2, 60, "water")],
        "D": [("F", 2, 250, "air")],
        "E": [("G", 3, 90, "road")],
        "F": [("G", 1, 150, "air")],
        "G": []
    }