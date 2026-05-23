import random

def aco(graph, start, target, deadline,
        ALPHA=1.0,         # Trọng số của Pheromone
        BETA=2.0,          # Trọng số của Heuristic
        EVAPORATION_RATE=0.5, 
        PATIENCE=20):      # Số vòng lặp tối đa không cải thiện trước khi dừng sớm
    
    # 1. Tự động nội suy cấu hình từ kích thước đồ thị
    num_nodes = len(graph)
    NUM_ANTS = min(num_nodes, 50)           # Linh hoạt theo số node, max 50 kiến
    NUM_ITERATIONS = max(100, num_nodes * 5) # Ít nhất 100, hoặc lớn hơn với đồ thị to
    
    # Khởi tạo pheromone
    pheromone = {}
    for u in graph:
        for v, t, c, m in graph[u]:
            pheromone[(u, v)] = 1.0

    states_visited = 0

    # Heuristic ưu tiên đường có chi phí thấp
    def heuristic(cost):
        return 1.0 / (cost + 1e-6)

    def construct_route():
        nonlocal states_visited
        current = start
        route = [start]
        total_time = 0
        total_cost = 0
        visited = set()
        
        states_visited += 1
        
        while current != target:
            visited.add(current)
            candidates = []
            probabilities = []
            
            for nei, time, cost, m in graph[current]:
                if nei in visited:
                    continue
                if total_time + time > deadline:
                    continue
                
                # Cập nhật công thức tính xác suất
                tau = pheromone[(current, nei)] ** ALPHA
                eta = heuristic(cost) ** BETA
                score = tau * eta
                
                candidates.append((nei, time, cost))
                probabilities.append(score)
                
            if not candidates:
                return None  # Kiến đi vào ngõ cụt
                
            total_score = sum(probabilities)
            # Tránh lỗi chia cho 0 nếu total_score quá nhỏ
            if total_score == 0:
                return None
                
            probabilities = [p / total_score for p in probabilities]
            nei, time, cost = random.choices(candidates, probabilities)[0]
            
            route.append(nei)
            total_time += time
            total_cost += cost
            current = nei
            states_visited += 1
            
        return route, total_time, total_cost

    def evaporate():
        for edge in pheromone:
            # Giới hạn pheromone không rớt xuống quá thấp để tránh mất hoàn toàn tính khám phá
            pheromone[edge] = max(1e-4, pheromone[edge] * (1 - EVAPORATION_RATE))

    def deposit(route, fitness):
        amount = 1.0 / (fitness + 1e-6)
        for i in range(len(route) - 1):
            u, v = route[i], route[i + 1]
            pheromone[(u, v)] += amount

    best_result = None
    best_cost = float('inf')
    iterations_without_improvement = 0 # Bộ đếm cho Early Stopping

    for iteration in range(NUM_ITERATIONS):
        solutions = []
        iteration_best_cost = float('inf')
        
        for ant in range(NUM_ANTS):
            result = construct_route()
            if result is None:
                continue
            
            route, time, cost = result
            solutions.append((route, cost))
            
            # Cập nhật kết quả tốt nhất mọi thời đại
            if cost < best_cost:
                best_result = {
                    "path": route.copy(),
                    "time": time,
                    "cost": cost,
                    "total_cost": cost,
                    "states_visited": states_visited,
                }
                best_cost = cost
                iterations_without_improvement = 0 # Reset bộ đếm khi tìm thấy kỷ lục mới
                
        # Nếu vòng lặp này không tìm được mốc mới, tăng bộ đếm
        iterations_without_improvement += 1
        
        # Dừng sớm (Early Stopping)
        if iterations_without_improvement >= PATIENCE:
            break 

        evaporate()
        
        # Cập nhật Elitist: Chỉ cho những kiến đi tới đích nhả pheromone, 
        for route, cost in solutions:
            deposit(route, cost)

    if best_result is not None:
        best_result["states_visited"] = states_visited

    return best_result