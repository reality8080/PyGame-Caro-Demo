import pandas as pd
import matplotlib.pyplot as plt
import os

if not os.path.exists("performance_log.json"):
    print("Chưa có dữ liệu.")
    exit()

df = pd.read_json("performance_log.json")
df_grouped = df.groupby("Algorithm").mean().reset_index()

plt.figure(figsize=(12, 6))

plt.plot(df_grouped["Algorithm"], df_grouped["Elapsed Time (s)"],
         marker='o', label="Thời gian (s)")
plt.plot(df_grouped["Algorithm"],
         df_grouped["RAM Used (MB)"], marker='s', label="RAM (MB)")
plt.plot(df_grouped["Algorithm"],
         df_grouped["ROM Used (GB)"], marker='^', label="ROM (GB)")

plt.title("Hiệu năng của các thuật toán AI")
plt.xlabel("Thuật toán")
plt.ylabel("Giá trị trung bình")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
