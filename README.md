# Shortest Path Algorithms Comparison  
## Tối ưu định tuyến logistics đa phương thức với ràng buộc thời gian

Dự án này xây dựng một bộ dữ liệu đồ thị có hướng và hiện thực nhiều phương pháp tìm kiếm khác nhau để so sánh hiệu năng khi giải bài toán định tuyến logistics đa phương thức.  
Mỗi cạnh trong đồ thị mang đồng thời thông tin về **thời gian**, **chi phí** và **phương thức vận chuyển**.

---

## 1. Mục tiêu dự án

Dự án tập trung vào ba câu hỏi chính:

1. Mỗi thuật toán tìm đường cho kết quả như thế nào trên cùng một bộ dữ liệu?
2. Thời gian chạy thực tế của các thuật toán thay đổi ra sao khi số node tăng lên?
3. Độ phức tạp thực tế có phù hợp với độ phức tạp lý thuyết hay không?

Từ đó, dự án cho phép so sánh:

- **Brute Force**
- **Backtracking**
- **A\***
- **ACO**
- **Dynamic Programming**

---

## 2. Mô hình bài toán

Đồ thị được biểu diễn dưới dạng **adjacency list**:

```text
(node) -> [(neighbor, time, cost, mode)]

Trong đó:
- neighbor: đỉnh kế tiếp
- time: thời gian di chuyển
- cost: chi phí vận chuyển
- mode: phương thức vận chuyển, ví dụ road, air, ship
```

Bài toán đặt ra là tìm đường đi từ đỉnh nguồn `start` đến đỉnh đích `goal` sao cho đường đi là hợp lệ theo ràng buộc dữ liệu, đồng thời tối ưu theo tiêu chí đánh giá của từng thuật toán.

---

## 3. Cấu trúc repository hiện tại

```text
shortest-path-algorithms-comparison/
│
├── algorithms/
│   ├── A_star.py
│   ├── aco.py
│   ├── backtracking.py
│   ├── brute_force.py
│   ├── dp.py
│   └── utils.py
│
├── data/
│   ├── config_data.py
│   └── experiment_graphs.py
│
├── experiments/
│   ├── benmark.py
│   ├── exp1.py
│   ├── exp2.py
│   └── exp3.py
│
├── visualization/
│   └── ...
│
└── README.md
```

**Vai trò các thư mục:**
- `algorithms/`: chứa các thuật toán tìm kiếm và hàm tiện ích
- `data/`: chứa dữ liệu đồ thị và các tham số cấu hình
- `experiments/`: chứa các script thực nghiệm, benchmark và thống kê
- `visualization/`: lưu biểu đồ và kết quả trực quan hóa
- `pyproject.toml`: cấu hình môi trường và phụ thuộc

---

## 4. Định dạng dữ liệu trong data/

File `data/experiment_graphs.py` sinh ra biến: `EXPERIMENT_GRAPHS`

Mỗi phần tử trong danh sách này là một graph có cấu trúc:

```json
{
    "id": "G001",
    "size_group": "small",
    "nodes": 5,
    "edge_density": "low",
    "tradeoff": true,
    "cycles": true,
    "start": "A",
    "goal": "T",
    "Tmax": 18,
    "positions": {...},
    "graph": {...}
}
```

**Đặc điểm dữ liệu:**
- Số node được sinh theo bước 5
- Dải số node: từ 5 đến 50
- Mỗi mức kích thước có nhiều graph khác nhau
- Mỗi graph đều có:
  - node nguồn `A`
  - node đích `T`
  - deadline `Tmax`
  - các cạnh có thời gian, chi phí và mode

---

## 5. Các thuật toán trong algorithms/

### 5.1 Brute Force
### 5.2 Backtracking
### 5.3 A*
### 5.4 ACO
### 5.5 Dynamic Programming
---

## 6. Các file thực nghiệm trong experiments/

- **`benmark.py`**:
  - Chạy benchmark tổng hợp trên toàn bộ dữ liệu
  - Tính thời gian chạy
  - Thống kê số trạng thái duyệt
  - Tính độ phức tạp thực tế và lý thuyết
  - Lưu kết quả ra CSV
- **`exp1.py`**:
  - Script thực nghiệm bổ sung
  - Dùng để đối chiếu hoặc kiểm tra một kịch bản chạy riêng
- **`exp2.py`**:
  - Vẽ biểu đồ thời gian chạy theo số node
  - Dùng để so sánh hiệu năng tăng trưởng theo kích thước đồ thị
- **`exp3.py`**:
  - So sánh độ phức tạp thực tế và độ phức tạp lý thuyết
  - Trực quan hóa mức độ chênh lệch giữa thực nghiệm và phân tích

---

## 7. Quy trình thực nghiệm

Quy trình làm việc của dự án:  
`data -> algorithms -> experiments -> visualization -> report`

**Ý nghĩa từng bước:**
- **data**: Sinh và quản lý bộ đồ thị đầu vào
- **algorithms**: Cài đặt các phương pháp tìm đường
- **experiments**: Chạy benchmark và thu thập số liệu
- **visualization**: Vẽ biểu đồ so sánh kết quả
- **report**: Phân tích, nhận xét và rút ra kết luận

---

## 8. Cách chạy chương trình

### 8.1 Cài đặt môi trường

Nếu dùng `uv`:
```bash
uv sync
```

Hoặc cài thủ công:
```bash
pip install pandas matplotlib
```

### 8.2 Chạy benchmark
```bash
python experiments/benmark.py
```
Kết quả được lưu ra:
- `experiments/benchmark_results.csv`
- `experiments/benchmark_runtime_summary.csv`
- `experiments/benchmark_complexity_summary.csv`

### 8.3 Vẽ biểu đồ thời gian chạy
```bash
python experiments/exp2.py
```
Biểu đồ được lưu tại: `visualization/runtime_vs_nodes.png`

### 8.4 Vẽ biểu đồ độ phức tạp
```bash
python experiments/exp3.py
```
Biểu đồ được lưu tại: `visualization/complexity_actual_vs_theoretical.png`

---

## 9. Các chỉ số được so sánh

Dự án đánh giá thuật toán dựa trên các tiêu chí sau:

### 9.1 Thời gian chạy
- Đo bằng giây
- Dùng để so sánh tốc độ thực thi

### 9.2 Số trạng thái duyệt
- Phản ánh số bước tìm kiếm thực tế
- Cho thấy mức độ hiệu quả của cắt nhánh hoặc heuristic

### 9.3 Tổng chi phí
- Dùng để kiểm tra chất lượng nghiệm
- Đặc biệt hữu ích khi so sánh giữa các thuật toán exact và heuristic

### 9.4 Độ phức tạp thực tế
- Được xấp xỉ từ số trạng thái duyệt hoặc một đại lượng proxy phù hợp

### 9.5 Độ phức tạp lý thuyết
- Được ước lượng theo mô hình tăng trưởng của từng thuật toán
- Ví dụ: `O(n!)`, `O(b^d)`, `O(n*T*E)`