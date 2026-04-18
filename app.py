import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Poll Results Visualizer", layout="wide")

st.title("📊 Poll Results Visualizer Dashboard")

# -----------------------------
# LOAD DATA (same logic as main.py)
# -----------------------------
import numpy as np

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

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔍 Filters")

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

selected_tool = st.sidebar.multiselect(
    "Select Tool",
    options=df["Preferred_Tool"].unique(),
    default=df["Preferred_Tool"].unique()
)

filtered_df = df[
    (df["Region"].isin(selected_region)) &
    (df["Preferred_Tool"].isin(selected_tool))
]

# -----------------------------
# SHOW DATA
# -----------------------------
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)

# -----------------------------
# KPI METRICS
# -----------------------------
col1, col2 = st.columns(2)

col1.metric("Total Responses", len(filtered_df))
col2.metric("Avg Satisfaction", round(filtered_df["Satisfaction"].mean(), 2))

# -----------------------------
# BAR CHART
# -----------------------------
st.subheader("📊 Tool Preference")

fig1, ax1 = plt.subplots()
sns.countplot(x="Preferred_Tool", data=filtered_df, ax=ax1)
st.pyplot(fig1)

# -----------------------------
# PIE CHART
# -----------------------------
st.subheader("🥧 Tool Share")

tool_counts = filtered_df["Preferred_Tool"].value_counts()

fig2, ax2 = plt.subplots()
tool_counts.plot.pie(autopct='%1.1f%%', ax=ax2)
ax2.set_ylabel("")
st.pyplot(fig2)

# -----------------------------
# REGION-WISE
# -----------------------------
st.subheader("🌍 Region vs Tool")

region_tool = pd.crosstab(filtered_df["Region"], filtered_df["Preferred_Tool"])

fig3, ax3 = plt.subplots()
region_tool.plot(kind="bar", stacked=True, ax=ax3)
st.pyplot(fig3)

# -----------------------------
# TREND
# -----------------------------
st.subheader("📈 Daily Trend")

daily = filtered_df.groupby("Date").size()

fig4, ax4 = plt.subplots()
daily.plot(ax=ax4)
st.pyplot(fig4)

# -----------------------------
# INSIGHTS
# -----------------------------
st.subheader("💡 Insights")

top_tool = tool_counts.idxmax()
st.write(f"🏆 Most Preferred Tool: **{top_tool}**")