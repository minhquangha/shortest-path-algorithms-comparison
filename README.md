# Tối ưu định tuyến logistics đa phương thức với penalty thời gian

---

## 1. Giới thiệu bài toán

Project này nghiên cứu và so sánh các phương pháp tìm kiếm để giải bài toán định tuyến logistics đa phương thức.

Hệ thống vận chuyển được mô hình hóa bằng đồ thị có hướng ( G(V, E) ):

* Đỉnh (node): các địa điểm
* Cạnh (edge): tuyến vận chuyển giữa các địa điểm

Mỗi cạnh có các thuộc tính:

* Thời gian (time)
* Chi phí (cost)
* Phương thức vận chuyển (mode ∈ {road, water, air})

---

## 2. Mục tiêu bài toán

Tìm đường đi từ điểm bắt đầu ( S ) đến điểm đích ( T ) sao cho tổng chi phí là nhỏ nhất, với hàm mục tiêu:

```
Total Cost = Cost + Penalty
```

Trong đó:

* Nếu tổng thời gian ( \leq T_{max} ):

```
Total Cost = Cost
```

* Nếu tổng thời gian ( > T_{max} ):

```
Total Cost = Cost + P × (time - T_{max})
```

Với:

* ( T_{max} ): thời gian giới hạn (deadline)
* ( P ): hệ số phạt (penalty)

---

## 3. Các thuật toán sử dụng

Các phương pháp được triển khai và so sánh:

* Brute Force (vét cạn)
* Backtracking (quay lui có cắt nhánh)
* Branch and Bound (nhánh cận)
* A* Search (tìm kiếm heuristic)

---

## 4. Cấu trúc project

```
logistics-routing-optimization/
│
├── data/
│   ├── sample_graph.py
│   ├── config_data.py
│
├── algorithms/
│   ├── brute_force.py
│   ├── backtracking.py
│   ├── branch_and_bound.py
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

## 5. Flow hoạt động

Quy trình thực hiện project:

```
data → algorithms → experiments → visualization → report
```

Chi tiết:

1. data
   Tạo và quản lý dữ liệu đầu vào (graph)

2. algorithms
   Cài đặt các thuật toán tìm đường

3. experiments
   Chạy benchmark và thu thập kết quả

4. visualization
   Vẽ biểu đồ từ dữ liệu benchmark

5. report
   Phân tích và đưa ra kết luận

---

## 6. Định dạng dữ liệu

Graph được biểu diễn dưới dạng adjacency list:

```
(node) → [(neighbor, time, cost, mode)]
```

Ví dụ:

```
A → [(B, 2, 100, road), (C, 6, 50, water)]
```

---

## 7. Hướng dẫn chạy chương trình

### 7.1 Cài đặt môi trường

Nếu sử dụng uv:

```
uv sync
```

Hoặc:

```
pip install matplotlib pandas
```

---

### 7.2 Chạy thử thuật toán

```
python main.py
```

---

### 7.3 Chạy benchmark

```
python experiments/benchmark.py
```

Kết quả:

* In ra màn hình
* Lưu vào file CSV để phục vụ phân tích

---

## 8. Tiêu chí so sánh

Các thuật toán được đánh giá dựa trên:

* Thời gian chạy (execution time)
* Số trạng thái duyệt (states visited)
* Tổng chi phí (total cost)
* Độ chính xác (so với brute force)

---

## 9. Ý nghĩa thực nghiệm

Thay đổi các tham số:

* ( T_{max} )
* ( P )

Quan sát:

* Penalty lớn → ưu tiên đường nhanh
* Penalty nhỏ → ưu tiên đường rẻ

Điều này thể hiện trade-off giữa thời gian và chi phí.

---

## 10. Giới hạn bài toán

* Số node nhỏ (5–10)
* Không xét bài toán đa mục tiêu phức tạp
* Tập trung vào so sánh phương pháp

---

## 11. Kết luận

Project giúp:

* Hiểu và so sánh các chiến lược tìm kiếm
* Phân tích hiệu quả thuật toán trong bài toán thực tế
* Đánh giá trade-off giữa thời gian và chi phí

Brute Force được sử dụng làm baseline để đánh giá độ chính xác của các phương pháp khác.

---
