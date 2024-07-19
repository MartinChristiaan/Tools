import numpy as np
import pandas as pd
from pathlib import Path

# Load data
proposed = Path("./data_ppt/combo_combined_prcurve_proposed-0.csv")
df = pd.read_csv(proposed).iloc[::-1]

# Define recalls and precision values from the dataframe
recalls = df["recall"]
precisions = df["precision"]

# Fit a polynomial of degree 3 (you can adjust the degree as needed)
degree = 3
coefficients = np.polyfit(recalls, precisions, degree)

# Generate polynomial function
poly_function = np.poly1d(coefficients)

# Specify recall points where you want to get precision values
specified_recalls = np.arange(0, max(recalls), 0.01)

# Get precision values at the specified recall points using the polynomial function
precision_values_at_specified_recalls = poly_function(specified_recalls)

print("Recalls:", specified_recalls)
print(
    "Precision values at the specified recalls:", precision_values_at_specified_recalls
)
