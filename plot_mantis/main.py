# %%
import pandas as pd
import plotly.express as px

df = pd.read_csv("./performance_mAP.csv")
df.sort_values(by="size", inplace=True)
print(df.columns)
model_types = []
for x, y, name in zip(df["precision"], df["relu"], df["detector name"]):
    name = "single-frame" if "single" in name else "multi-frame"
    model_type = f"{name}-{x}"
    if y:
        model_type += "-relu"
    model_types.append(model_type)

df["model_type"] = model_types
import matplotlib.pyplot as plt

plt.figure()

for label, df in df.groupby("model_type"):
    if "single" in label:
        continue
    plt.plot(df["throughput"], df["mAP"], marker="o", linestyle="-", label=label)
plt.xlabel("Throughput")
plt.ylabel("mAP")
plt.title("mAP vs Throughput")
plt.legend()
plt.show()
