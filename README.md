# Tối ưu định tuyến logistics đa phương thức

## 1. Giới thiệu

Project này giải bài toán tìm đường đi tối ưu trong mạng logistics đa phương thức.

Mạng vận chuyển được mô hình hóa bằng đồ thị có hướng:

```text
G = (V, E)
```

Trong đó:

- `V`: tập các địa điểm, ví dụ kho hàng, trạm trung chuyển, điểm giao hàng.
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

Một đường đi chỉ được xem là hợp lệ nếu thỏa mãn deadline trên.

---

## 3. Dữ liệu thực nghiệm

Bộ dữ liệu được sinh tự động để phục vụ so sánh thuật toán.

Đặc điểm chính:

- Số node tăng từ 5 đến 50.
- Bước tăng là 5 node.
- Mỗi kích thước sinh 3 đồ thị.
- Tổng cộng có 30 đồ thị.
- Sử dụng `random.seed(42)` để có thể tái lập kết quả.

Các nhóm dữ liệu:

| Nhóm | Số node | Mật độ cạnh |
|---|---:|---|
| small | 5--15 | low |
| medium | 20--35 | medium |
| large | 40--50 | high |

Các phương thức vận tải:

| Mode | Time | Cost | Ý nghĩa |
|---|---:|---:|---|
| road | 5--12 | 10--60 | Rẻ hơn nhưng chậm hơn |
| air | 1--4 | 150--350 | Nhanh nhất nhưng đắt nhất |
| ship | 3--8 | 60--180 | Trung gian giữa road và air |

---

## 4. Các thuật toán sử dụng

Project triển khai và so sánh 5 thuật toán:

1. **Brute Force**
   Liệt kê tất cả đường đi từ `A` đến `T`, sau đó chọn đường hợp lệ có chi phí nhỏ nhất.

2. **Backtracking**
   Duyệt các đường đi có cắt nhánh khi tổng thời gian vượt quá `Tmax`.

3. **Dynamic Programming**
   Lưu chi phí nhỏ nhất theo trạng thái `dp[v][t]`, trong đó `v` là đỉnh hiện tại và `t` là tổng thời gian đã dùng.

4. **Ant Colony Optimization**
   Mô phỏng hành vi tìm đường của đàn kiến để tìm lời giải tốt trên không gian tìm kiếm lớn.

5. **A\* Search**
   Sử dụng heuristic để định hướng quá trình tìm kiếm đường đi tối ưu.

---

## 5. Cấu trúc project

```text
logistics-routing-optimization/
│
├── data/
│   ├── sample_graph.py
│   └── config_data.py
│
├── algorithms/
│   ├── brute_force.py
│   ├── backtracking.py
│   ├── dynamic_programming.py
│   ├── aco.py
│   ├── astar.py
│   └── utils.py
│
├── experiments/
│   └── benchmark.py
│
├── visualization/
│   └── plot_results.py
│
├── main.py
├── README.md
└── pyproject.toml
```

---

## 6. Quy trình thực hiện

```text
data -> algorithms -> experiments -> visualization -> report
```

Trong đó:

- `data`: sinh và quản lý đồ thị đầu vào.
- `algorithms`: cài đặt các thuật toán tìm đường.
- `experiments`: chạy benchmark và lưu kết quả.
- `visualization`: vẽ biểu đồ so sánh.
- `report`: phân tích và rút ra kết luận.

---

## 7. Cách chạy chương trình

Cài đặt thư viện:

```bash
pip install matplotlib pandas
```

Hoặc nếu dùng `uv`:

```bash
uv sync
```

Chạy chương trình chính:

```bash
python main.py
```

Chạy benchmark:

```bash
python experiments/benchmark.py
```

---

## 8. Tiêu chí so sánh

Các thuật toán được đánh giá dựa trên:

- Tổng chi phí tìm được.
- Tổng thời gian của lộ trình.
- Thời gian chạy.
- Số trạng thái đã duyệt.
- Khả năng tìm được đường đi hợp lệ.
- Độ chính xác so với nghiệm tối ưu hoặc baseline.

Brute Force thường được dùng làm baseline vì có thể tìm nghiệm tối ưu trên đồ thị nhỏ.

---

## 9. Kết luận

Project giúp so sánh nhiều chiến lược tìm kiếm trong bài toán định tuyến logistics đa phương thức có ràng buộc thời gian.

Bài toán thể hiện rõ trade-off giữa thời gian và chi phí:

- Đường rẻ nhất có thể không hợp lệ nếu vượt quá `Tmax`.
- Đường nhanh hơn có thể có chi phí cao hơn.
- Thuật toán cần tìm đường đi hợp lệ có chi phí nhỏ nhất.
