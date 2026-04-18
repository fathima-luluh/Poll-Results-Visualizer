import streamlit as st
import pandas as pd
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
# DATA UPLOAD SECTION
# ----------------------------
st.sidebar.header("📂 Upload Your Dataset")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
else:
    st.info("ℹ️ Using default dataset")

    # fallback synthetic dataset
    df = pd.DataFrame({
        "Preferred_Tool": ["Python", "R", "Excel", "Python", "Excel", "R", "Python"],
        "Satisfaction": [4, 3, 5, 4, 2, 3, 5],
        "Region": ["North", "South", "East", "West", "North", "East", "South"],
        "Feedback": [
            "Great tool", "Needs improvement", "Very useful",
            "Excellent", "Not bad", "Good experience", "Amazing"
        ]
    })

# ----------------------------
# DATA PREVIEW
# ----------------------------
st.subheader("📌 Dataset Preview")
st.dataframe(df)

# ----------------------------
# KPI METRICS
# ----------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Responses", len(df))
col2.metric("Avg Satisfaction", round(df["Satisfaction"].mean(), 2))
col3.metric("Top Tool", df["Preferred_Tool"].mode()[0])

# ----------------------------
# BAR CHART - TOOL PREFERENCE
# ----------------------------
st.subheader("📊 Tool Preference")

fig1, ax1 = plt.subplots()
sns.countplot(x="Preferred_Tool", data=df, ax=ax1)
plt.xticks(rotation=30)
st.pyplot(fig1)

# ----------------------------
# PIE CHART - REGION DISTRIBUTION
# ----------------------------
st.subheader("🌍 Region Distribution")

fig2, ax2 = plt.subplots()
df["Region"].value_counts().plot.pie(autopct="%1.1f%%", ax=ax2)
ax2.set_ylabel("")
st.pyplot(fig2)

# ----------------------------
# SATISFACTION DISTRIBUTION
# ----------------------------
st.subheader("⭐ Satisfaction Distribution")

fig3, ax3 = plt.subplots()
sns.histplot(df["Satisfaction"], bins=5, kde=True, ax=ax3)
st.pyplot(fig3)

# ----------------------------
# WORD CLOUD (FEEDBACK)
# ----------------------------
st.subheader("💬 Feedback Word Cloud")

text = " ".join(df["Feedback"].astype(str))

if text:
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white"
    ).generate(text)

    fig4, ax4 = plt.subplots()
    ax4.imshow(wordcloud, interpolation="bilinear")
    ax4.axis("off")
    st.pyplot(fig4)

# ----------------------------
# AUTO INSIGHTS
# ----------------------------
st.subheader("💡 Auto Insights")

top_tool = df["Preferred_Tool"].value_counts().idxmax()
avg_sat = df["Satisfaction"].mean()
top_region = df["Region"].value_counts().idxmax()

st.write(f"""
- 🏆 Most preferred tool: **{top_tool}**
- ⭐ Average satisfaction: **{round(avg_sat,2)}**
- 🌍 Most active region: **{top_region}**
""")

# ----------------------------
# DOWNLOAD DATA
# ----------------------------
st.sidebar.subheader("⬇ Download Data")

csv = df.to_csv(index=False).encode("utf-8")

st.sidebar.download_button(
    label="Download CSV",
    data=csv,
    file_name="poll_results.csv",
    mime="text/csv"
)