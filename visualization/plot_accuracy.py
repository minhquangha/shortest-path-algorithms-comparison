import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT_DIR / "experiments" / "benchmark_summary.csv"
OUTPUT_PNG = ROOT_DIR / "visualization" / "accuracy_comparison.png"

def plot_accuracy():
    if not CSV_PATH.exists():
        print(f"Không tìm thấy file: {CSV_PATH}")
        return

    df = pd.read_csv(CSV_PATH)
    
    # Calculate accuracy as percentage
    if 'solve_rate' in df.columns:
        df['accuracy'] = df['solve_rate'] * 100
    elif 'solved_cases' in df.columns and 'cases' in df.columns:
        df['accuracy'] = (df['solved_cases'] / df['cases']) * 100
    else:
        print("Không tìm thấy cột dữ liệu phù hợp để tính độ chính xác.")
        return

    plt.figure(figsize=(8, 6))
    
    # Draw bar chart
    bars = plt.bar(df['algorithm'], df['accuracy'], color=['#4C72B0', '#DD8452', '#55A868', '#C44E52'])
    
    # Add values on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.0f}%', ha='center', va='bottom', fontweight='bold')

    plt.title("So sánh độ chính xác của các thuật toán", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Thuật toán", fontsize=12)
    plt.ylabel("Độ chính xác (%)", fontsize=12)
    plt.ylim(0, 115) # Set y-limit to have some space for text
    plt.xticks(rotation=15, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    OUTPUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
    print(f"Đã lưu biểu đồ tại: {OUTPUT_PNG}")

if __name__ == "__main__":
    plot_accuracy()
