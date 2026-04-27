def compute_total_cost(time_so_far, cost_so_far, deadline, penalty):
    if time_so_far <= deadline:
        return cost_so_far

    late_time = time_so_far - deadline
    return cost_so_far + penalty * late_time