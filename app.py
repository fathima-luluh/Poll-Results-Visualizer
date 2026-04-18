import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Poll Results Visualizer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Poll Results Visualizer Dashboard")

# ----------------------------
# DATA LOADING
# ----------------------------
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

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------
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

# ----------------------------
# DATA PREVIEW
# ----------------------------
st.subheader("📌 Dataset Preview")
st.dataframe(filtered_df)

# ----------------------------
# KPI METRICS
# ----------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Responses", len(filtered_df))
col2.metric("Avg Satisfaction", round(filtered_df["Satisfaction"].mean(), 2))
col3.metric("Top Tool", filtered_df["Preferred_Tool"].mode()[0])

# ----------------------------
# BAR CHART
# ----------------------------
st.subheader("📊 Tool Preference")

fig1, ax1 = plt.subplots()
sns.countplot(x="Preferred_Tool", data=filtered_df, ax=ax1)
plt.xticks(rotation=30)
st.pyplot(fig1)

# ----------------------------
# PIE CHART
# ----------------------------
st.subheader("🌍 Region Distribution")

fig2, ax2 = plt.subplots()
filtered_df["Region"].value_counts().plot.pie(autopct="%1.1f%%", ax=ax2)
ax2.set_ylabel("")
st.pyplot(fig2)

# ----------------------------
# SATISFACTION
# ----------------------------
st.subheader("⭐ Satisfaction Distribution")

fig3, ax3 = plt.subplots()
sns.histplot(filtered_df["Satisfaction"], bins=5, kde=True, ax=ax3)
st.pyplot(fig3)

# ----------------------------
# TREND
# ----------------------------
st.subheader("📈 Daily Trend")

daily = filtered_df.groupby("Date").size()

fig4, ax4 = plt.subplots()
daily.plot(ax=ax4)
st.pyplot(fig4)

# ----------------------------
# WORD CLOUD
# ----------------------------
st.subheader("💬 Feedback Word Cloud")

feedback_text = "Good Excellent Amazing Useful Great"

wordcloud = WordCloud(
    width=800,
    height=400,
    background_color="white"
).generate(feedback_text)

fig5, ax5 = plt.subplots()
ax5.imshow(wordcloud, interpolation="bilinear")
ax5.axis("off")
st.pyplot(fig5)

# ----------------------------
# INSIGHTS
# ----------------------------
st.subheader("💡 Insights")

st.write(f"""
- 🏆 Most Preferred Tool: **{filtered_df['Preferred_Tool'].mode()[0]}**
- ⭐ Average Satisfaction: **{round(filtered_df['Satisfaction'].mean(),2)}**
- 🌍 Most Active Region: **{filtered_df['Region'].mode()[0]}**
""")

# ----------------------------
# DOWNLOAD
# ----------------------------
st.sidebar.subheader("⬇ Download Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.sidebar.download_button(
    label="Download CSV",
    data=csv,
    file_name="poll_results.csv",
    mime="text/csv"
)