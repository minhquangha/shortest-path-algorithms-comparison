# Tối ưu định tuyến logistics đa phương thức

## 1. Giới thiệu

Project này giải bài toán tìm đường đi tối ưu trong mạng logistics đa phương thức.

Mạng vận chuyển được mô hình hóa bằng đồ thị có hướng:

```text
G = (V, E)
```

Trong đó:

- `V`: tập các địa điểm (kho hàng, trạm trung chuyển, điểm giao hàng).
- `E`: tập các tuyến vận chuyển giữa các địa điểm.

Mỗi cạnh trong đồ thị có dạng:

```text
(neighbor, time, cost, mode)
```

Trong đó:

- `neighbor`: đỉnh kề.
- `time`: thời gian vận chuyển.
- `cost`: chi phí vận chuyển.
- `mode`: phương thức vận tải, gồm `road`, `air`, `ship`.

---

## 2. Mục tiêu bài toán

Tìm đường đi từ đỉnh xuất phát `A` đến đỉnh đích `T` sao cho:

- Tổng chi phí vận chuyển là nhỏ nhất.
- Tổng thời gian không vượt quá deadline `Tmax`.

Hàm mục tiêu:

```text
min cost(P)
```

Ràng buộc thời gian:

```text
time(P) <= Tmax
```

Một đường đi chỉ được xem là hợp lệ nếu thỏa mãn ràng buộc deadline trên.

---

## 3. Các thuật toán sử dụng

Project triển khai và so sánh 5 thuật toán:

### 3.1. Brute Force (`algorithms/brute_force.py`)

Liệt kê **tất cả** đường đi từ `A` đến `T` bằng DFS, sau đó chọn đường hợp lệ (`time <= Tmax`) có chi phí nhỏ nhất. Chỉ chạy trên đồ thị có `nodes <= 15` do độ phức tạp theo giai thừa.

- Độ phức tạp: `O(V!)`

### 3.2. Backtracking (`algorithms/backtracking.py`)

Duyệt đường đi bằng DFS với hai chiến lược cắt nhánh:
- Cắt khi tổng thời gian vượt quá `deadline`.
- Cắt khi chi phí hiện tại đã lớn hơn hoặc bằng kết quả tốt nhất tìm được.

- Độ phức tạp: `O(B_max^D)` với `B_max` là branching factor lớn nhất, `D` là độ sâu.

### 3.3. Dynamic Programming (`algorithms/dp.py`)

Sử dụng bảng `dp[v][t]` lưu chi phí nhỏ nhất để đến đỉnh `v` với tổng thời gian đúng bằng `t`. Duyệt theo từng mức thời gian từ `0` đến `Tmax`, cập nhật các đỉnh kề. Truy vết đường đi qua bảng `parent`.

- Độ phức tạp: `O(Tmax × (V + E))`

### 3.4. Ant Colony Optimization (`algorithms/aco.py`)

Mô phỏng hành vi tìm đường của đàn kiến. Các tham số tự động nội suy theo kích thước đồ thị:
- Số kiến `K = min(V, 50)`.
- Số vòng lặp `I = max(100, V × 5)`.
- Cơ chế **Early Stopping**: dừng khi không cải thiện sau `PATIENCE = 20` vòng.
- Cập nhật pheromone theo chiến lược **Elitist** (chỉ kiến đi tới đích mới nhả pheromone).

- Độ phức tạp: `O(I × K × V × D)`

### 3.5. A* Search (`algorithms/A_star.py`)

Sử dụng heuristic là khoảng cách Dijkstra ngược từ đỉnh đích `T` (tính trên chi phí). Trạng thái tìm kiếm là `(node, time_so_far)`, kết hợp cắt nhánh khi:
- `f(n) >= best_cost` đã tìm được.
- `time > Tmax`.

- Độ phức tạp: `O((V + E) log V + V × Tmax × log(V × Tmax))`

---

## 4. Dữ liệu thực nghiệm

Bộ dữ liệu được sinh tự động bởi `data/experiment_graphs.py`.

### Quy mô đồ thị

| Nhóm     | Số node                   | Số kích thước | Seed |
| -------- | ------------------------- | :-----------: | :--: |
| Small    | 5, 10, 13                 |       3       |  42  |
| Medium   | 20, 30, 40, 50            |       4       |  43  |
| Large    | 100, 200, 300, 400, 500   |       5       |  44  |

### Mật độ cạnh

Mỗi kích thước sinh 3 đồ thị tương ứng với 3 mức mật độ:

| Mật độ   | Số cạnh phụ thêm   |
| -------- | :-----------------: |
| low      | `num_nodes`         |
| medium   | `num_nodes × 2`     |
| high     | `num_nodes × 4`     |

**Tổng cộng: (3 + 4 + 5) × 3 = 36 đồ thị.**

### Phương thức vận tải

| Mode   | Time    | Cost      | Đặc điểm                        |
| ------ | :-----: | :-------: | -------------------------------- |
| road   | 5 – 12  | 10 – 60   | Rẻ nhất nhưng chậm nhất         |
| air    | 1 – 4   | 150 – 350 | Nhanh nhất nhưng đắt nhất       |
| ship   | 3 – 8   | 60 – 180  | Trung gian giữa road và air     |

### Đặc điểm đồ thị

- Mỗi đồ thị luôn có đường backbone `A → N01 → N02 → ... → T` với cả 3 phương thức vận tải (trade-off).
- Có thêm các cạnh ngẫu nhiên và **chu trình (cycles)**.
- Deadline `Tmax` được tính dựa trên `reference_time` của đường backbone: `Tmax ∈ [0.45 × ref, 0.75 × ref]`.

---

## 5. Cấu trúc thư mục

```text
shortest-path-algorithms-comparison/
│
├── algorithms/                          # Cài đặt các thuật toán
│   ├── __init__.py
│   ├── brute_force.py                   # Brute Force – duyệt toàn bộ
│   ├── backtracking.py                  # Backtracking – DFS có cắt nhánh
│   ├── dp.py                            # Dynamic Programming – dp[v][t]
│   ├── aco.py                           # Ant Colony Optimization
│   ├── A_star.py                        # A* Search với heuristic Dijkstra ngược
│   └── utils.py                         # Hàm tiện ích (compute_total_cost)
│
├── data/                                # Sinh và lưu trữ dữ liệu đồ thị
│   ├── __init__.py
│   ├── config_data.py                   # Cấu hình mặc định (START, TARGET, TMAX)
│   ├── experiment_graphs.py             # Script sinh đồ thị tự động
│   ├── small_graphs.json                # 9 đồ thị nhỏ (5–13 node)
│   ├── medium_graphs.json               # 12 đồ thị trung bình (20–50 node)
│   ├── large_graphs.json                # 15 đồ thị lớn (100–500 node)
│   └── EXPERIMENT_GRAPHS.json           # Tập gộp toàn bộ 36 đồ thị
│
├── experiments/                         # Chạy benchmark và phân tích
│   ├── __init__.py
│   ├── benchmark.py                     # Engine benchmark chính
│   ├── exp1.py                          # Thực nghiệm 1: Tỷ lệ tối ưu & Optimality Gap
│   ├── exp2.py                          # Thực nghiệm 2: Thời gian chạy theo số node
│   ├── exp3.py                          # Thực nghiệm 3: Phân tích độ phức tạp
│   ├── benchmark_results.csv            # Kết quả chi tiết từng test case
│   ├── benchmark_runtime_summary.csv    # Tổng hợp thời gian chạy
│   └── benchmark_complexity_summary.csv # Tổng hợp độ phức tạp
│
├── visualization/                       # Biểu đồ kết quả
│   ├── __init__.py
│   ├── plot_accuracy.py                 # Script vẽ biểu đồ độ chính xác
│   ├── accuracy_comparison.png          # Biểu đồ tỷ lệ tìm được tối ưu
│   ├── optimality_gap.png              # Biểu đồ optimality gap theo số node
│   ├── runtime_vs_nodes.png             # Biểu đồ thời gian chạy (log-log)
│   ├── complexity_actual_vs_theoretical.png  # So sánh tổng hợp thực tế vs lý thuyết
│   ├── complexity_all_algorithms.png    # Biểu đồ ghép 5 thuật toán (5×2)
│   ├── complexity_brute_force.png       # Độ phức tạp Brute Force
│   ├── complexity_backtracking.png      # Độ phức tạp Backtracking
│   ├── complexity_dp.png               # Độ phức tạp DP
│   ├── complexity_aco.png              # Độ phức tạp ACO
│   └── complexity_astar.png            # Độ phức tạp A*
│
├── .python-version                      # Python 3.10
├── pyproject.toml                       # Cấu hình project
├── uv.lock                             # Lock file cho uv
├── .gitignore
└── README.md
```

---

## 6. Hướng dẫn sử dụng

### Yêu cầu hệ thống

- Python >= 3.10
- Thư viện: `pandas`, `matplotlib`

### Cài đặt

Nếu dùng `uv` (khuyến nghị):

```bash
uv sync
```

Hoặc dùng `pip`:

```bash
pip install pandas matplotlib
```

### Sinh dữ liệu đồ thị

```bash
python data/experiment_graphs.py
```

Lệnh này sẽ sinh ra 4 file JSON trong thư mục `data/`:
- `small_graphs.json` (9 đồ thị)
- `medium_graphs.json` (12 đồ thị)
- `large_graphs.json` (15 đồ thị)
- `EXPERIMENT_GRAPHS.json` (36 đồ thị gộp)

### Chạy benchmark

```bash
python -m experiments.benchmark
```

Kết quả được lưu vào 3 file CSV trong thư mục `experiments/`:
- `benchmark_results.csv` — kết quả chi tiết từng test case.
- `benchmark_runtime_summary.csv` — thống kê thời gian chạy theo thuật toán.
- `benchmark_complexity_summary.csv` — thống kê độ phức tạp theo số node.

### Chạy từng thực nghiệm

```bash
python -m experiments.exp1    # Thực nghiệm 1: Accuracy + Optimality Gap
python -m experiments.exp2    # Thực nghiệm 2: Runtime vs Nodes
python -m experiments.exp3    # Thực nghiệm 3: Complexity Analysis
```

Mỗi lệnh tự động đọc `benchmark_results.csv` (nếu đã có), hoặc chạy benchmark lại nếu chưa có, rồi xuất biểu đồ vào thư mục `visualization/`.

---

## 7. Kịch bản thực nghiệm

### Thực nghiệm 1 — Tỷ lệ tối ưu và Optimality Gap (`exp1.py`)

**Mục tiêu:** Đánh giá chất lượng lời giải của từng thuật toán.

**Phương pháp:**
1. Với mỗi test case, xác định chi phí tối ưu (nhỏ nhất) trong các thuật toán chính xác (Brute Force, Backtracking, DP, A\*).
2. Tính **tỷ lệ tìm được tối ưu** = số test case mà thuật toán tìm được lời giải khớp chi phí tối ưu / tổng số test case.
3. Tính **Optimality Gap (%)** = `(cost_found − cost_optimal) / cost_optimal × 100`, trung bình theo từng mức số node.

**Đầu ra:**
- `visualization/accuracy_comparison.png` — biểu đồ cột so sánh tỷ lệ tối ưu.
- `visualization/optimality_gap.png` — biểu đồ đường gap theo số node.

**Kỳ vọng:** Brute Force, Backtracking, DP, A\* luôn tìm được nghiệm tối ưu (gap = 0%). ACO có gap > 0% nhưng vẫn ở mức chấp nhận được.

---

### Thực nghiệm 2 — Thời gian chạy theo quy mô đồ thị (`exp2.py`)

**Mục tiêu:** So sánh thời gian chạy thực tế của các thuật toán khi tăng số node.

**Phương pháp:**
1. Nhóm kết quả benchmark theo `(nodes, algorithm)`.
2. Tính thời gian chạy trung bình (`mean_time_s`) cho mỗi nhóm.
3. Vẽ biểu đồ log-log (cả trục X và Y đều dùng thang logarithm).

**Đầu ra:**
- `visualization/runtime_vs_nodes.png` — biểu đồ đường thời gian chạy.
- `experiments/benchmark_runtime_summary.csv` — bảng tổng hợp.

**Kỳ vọng:** A\* và DP nhanh nhất trên mọi kích thước. Brute Force chỉ chạy được trên đồ thị nhỏ (`<= 15` node). Backtracking tăng nhanh trên đồ thị lớn. ACO tăng tuyến tính nhưng chậm hơn A\*/DP do số vòng lặp lớn.

---

### Thực nghiệm 3 — Phân tích độ phức tạp thực tế vs lý thuyết (`exp3.py`)

**Mục tiêu:** Kiểm chứng độ phức tạp lý thuyết bằng số liệu thực tế.

**Phương pháp:**
1. **Actual complexity** (log₁₀): đo bằng `states_visited` (Brute Force, Backtracking, DP, A\*) hoặc `estimated_ops` (ACO).
2. **Theoretical complexity** (log₁₀): tính theo công thức lý thuyết của mỗi thuật toán.
3. Vẽ biểu đồ so sánh cho từng thuật toán và biểu đồ tổng hợp.

**Công thức lý thuyết:**

| Thuật toán   | Công thức                                                    |
| ------------ | ------------------------------------------------------------ |
| Brute Force  | `O(V!)`                                                      |
| Backtracking | `O(B_max^D)`                                                 |
| A*           | `O((V+E) log V + V × Tmax × log(V × Tmax))`                 |
| ACO          | `O(I × K × V × D)`                                           |
| DP           | `O(Tmax × (V + E))`                                          |

**Đầu ra:**
- `visualization/complexity_actual_vs_theoretical.png` — so sánh tổng hợp (1×2).
- `visualization/complexity_all_algorithms.png` — biểu đồ ghép 5 thuật toán (5×2).
- `visualization/complexity_<algorithm>.png` — biểu đồ riêng cho từng thuật toán.
- `experiments/benchmark_complexity_summary.csv` — bảng tổng hợp.

**Kỳ vọng:** Đường actual nằm **dưới** đường theoretical (complexity gap > 0), cho thấy cắt nhánh và heuristic hoạt động hiệu quả trong thực tế.

---

## 8. Tiêu chí so sánh tổng hợp

Các thuật toán được đánh giá dựa trên:

| Tiêu chí                          | Đo bằng                                                  |
| --------------------------------- | --------------------------------------------------------- |
| Chi phí lời giải                  | `total_cost` (chi phí đường đi tìm được)                 |
| Chất lượng lời giải               | Optimality Gap (%) so với nghiệm tối ưu                  |
| Thời gian chạy                    | `execution_time_s` (giây)                                 |
| Số trạng thái đã duyệt           | `states_visited`                                          |
| Khả năng tìm được đường đi       | `found` (True/False)                                      |
| Tỷ lệ giải thành công            | `solve_rate` = solved_cases / total_cases                 |
| Khả năng mở rộng (scalability)    | Biến thiên thời gian khi tăng số node                     |

Brute Force được dùng làm **baseline** vì luôn tìm nghiệm tối ưu trên đồ thị nhỏ.

---

## 9. Kết luận

Project giúp so sánh nhiều chiến lược tìm kiếm trong bài toán định tuyến logistics đa phương thức có ràng buộc thời gian.

Bài toán thể hiện rõ trade-off giữa thời gian và chi phí:

- Đường rẻ nhất có thể không hợp lệ nếu vượt quá `Tmax`.
- Đường nhanh hơn có thể có chi phí cao hơn.
- Thuật toán cần tìm đường đi hợp lệ có chi phí nhỏ nhất.
