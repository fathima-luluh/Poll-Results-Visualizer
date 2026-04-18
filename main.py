import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------------
# CREATE OUTPUT FOLDER
# -----------------------------
os.makedirs("outputs", exist_ok=True)

# -----------------------------
# STEP 1: GENERATE SYNTHETIC DATA
# -----------------------------
np.random.seed(42)

n = 200

df = pd.DataFrame({
    "Respondent_ID": range(1, n+1),
    "Age_Group": np.random.choice(["18-24","25-34","35-44"], n),
    "Gender": np.random.choice(["Male","Female"], n),
    "Preferred_Tool": np.random.choice(["Python","R","Excel"], n, p=[0.5,0.2,0.3]),
    "Satisfaction": np.random.randint(1,6,n),
    "Region": np.random.choice(["North","South","East","West"], n),
    "Date": pd.date_range(start="2024-01-01", periods=n, freq="D")
})

print("\n📊 Dataset Preview:\n", df.head())

# -----------------------------
# STEP 2: CLEANING
# -----------------------------
df = df.drop_duplicates()
df = df.dropna()

# -----------------------------
# STEP 3: ANALYSIS
# -----------------------------
tool_counts = df["Preferred_Tool"].value_counts()
tool_percent = round((tool_counts / len(df)) * 100, 2)

print("\n📈 Tool Distribution (%):\n", tool_percent)

# Region-wise analysis
region_tool = pd.crosstab(df["Region"], df["Preferred_Tool"])

# -----------------------------
# STEP 4: VISUALIZATION
# -----------------------------

# Bar Chart
plt.figure(figsize=(6,4))
sns.countplot(x="Preferred_Tool", data=df)
plt.title("Tool Preference Distribution")
plt.savefig("outputs/bar_chart.png")
plt.show()

# Pie Chart
plt.figure()
tool_counts.plot.pie(autopct='%1.1f%%')
plt.title("Tool Share (%)")
plt.ylabel("")
plt.savefig("outputs/pie_chart.png")
plt.show()

# Region-wise stacked chart
region_tool.plot(kind="bar", stacked=True, figsize=(7,5))
plt.title("Region vs Tool Preference")
plt.savefig("outputs/region_chart.png")
plt.show()

# Trend over time
daily = df.groupby("Date").size()

plt.figure(figsize=(8,4))
daily.plot(marker='o')
plt.title("Daily Responses Trend")
plt.savefig("outputs/trend_chart.png")
plt.show()

# -----------------------------
# STEP 5: INSIGHTS
# -----------------------------
top_tool = tool_counts.idxmax()
avg_satisfaction = df["Satisfaction"].mean()

print(f"\n🏆 Most Preferred Tool: {top_tool}")
print(f"⭐ Average Satisfaction: {round(avg_satisfaction,2)}")