import streamlit as st
import pandas as pd
import plotly.express as px

#Page Config
st.set_page_config(
    page_title="Nigeria Malnutrition Dashboard",
    page_icon="🇳🇬",
    layout="wide",
    initial_sidebar_state="expanded"
)

#Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .stMetric label { color: #555555; font-size: 14px; }
    .block-container { padding-top: 2rem; }
    h1 { color: #1a1a2e; }
    h2, h3 { color: #16213e; }
    .insight-box {
        background-color: #e8f4fd;
        border-left: 4px solid #2196F3;
        padding: 10px 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

#Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("Nigeria_malnutrition_cleaned.csv")
    return df

df = load_data()

#Sidebar
st.sidebar.title("🇳🇬 Nigeria Dashboard")
st.sidebar.markdown("Explore acute malnutrition data across Nigerian regions.")
st.sidebar.divider()

# Region filter
regions = ["All"] + sorted(df["Region"].unique().tolist())
selected_region = st.sidebar.selectbox("🌍 Select Region", regions)

# Malnutrition type filter
malnutrition_type = st.sidebar.radio(
    "📊 Select Malnutrition Type",
    ["GAM", "SAM", "MAM"]
)

st.sidebar.divider()

#Filter Data
if selected_region == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Region"] == selected_region]

st.sidebar.markdown(f"**Showing:** {len(filtered_df)} LGAs")

#Column Mapping
col_map = {
    "GAM": "Estimated # of GAM cases",
    "SAM": "Estimated # of SAM cases",
    "MAM": "Estimated # of MAM cases"
}
selected_col = col_map[malnutrition_type]
lga_col = filtered_df.columns[1]
region_col = "Region"

#Title
st.title("🇳🇬 Nigerian Acute Malnutrition Dashboard")
st.caption("Source: Humanitarian Data Exchange (HDX) — 2026")
st.divider()

#KPI Cards
st.subheader("📊 Key Statistics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total LGAs", len(filtered_df))
col2.metric("Total GAM Cases", f"{filtered_df['Estimated # of GAM cases'].sum():,.0f}")
col3.metric("Total SAM Cases", f"{filtered_df['Estimated # of SAM cases'].sum():,.0f}")
col4.metric("Total MAM Cases", f"{filtered_df['Estimated # of MAM cases'].sum():,.0f}")

st.divider()

#Row 1: Bar chart + Pie chart
col_left, col_right = st.columns(2)

with col_left:
    st.subheader(f"🏆 Top 10 LGAs by {malnutrition_type} Cases")
    top10 = filtered_df.nlargest(10, selected_col)
    fig1 = px.bar(
        top10,
        x=selected_col,
        y=lga_col,
        orientation='h',
        color=region_col,
        title=f"Top 10 LGAs by {malnutrition_type} Cases",
        labels={selected_col: f"{malnutrition_type} Cases", lga_col: "LGA"}
    )
    fig1.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader(f"🥧 {malnutrition_type} Cases by Region")
    region_summary = filtered_df.groupby(region_col)[selected_col].sum().reset_index()
    fig2 = px.pie(
        region_summary,
        names=region_col,
        values=selected_col,
        title=f"{malnutrition_type} Distribution by Region",
        hole=0.4
    )
    st.plotly_chart(fig2, use_container_width=True)


#Row 2: Grouped Bar chart
st.subheader("📈 GAM vs SAM vs MAM by Region")
region_compare = df.groupby(region_col).agg(
    GAM=('Estimated # of GAM cases', 'sum'),
    SAM=('Estimated # of SAM cases', 'sum'),
    MAM=('Estimated # of MAM cases', 'sum')
).reset_index()

fig3 = px.bar(
    region_compare,
    x=region_col,
    y=["GAM", "SAM", "MAM"],
    barmode="group",
    title="Malnutrition Types Comparison by Region",
    labels={"value": "Number of Cases", "variable": "Type"}
)
st.plotly_chart(fig3, use_container_width=True)

st.divider()

#Row 3: Summary table by region
st.subheader("📋 Regional Summary Table")
summary = df.groupby(region_col).agg(
    Total_LGAs=(lga_col, 'count'),
    Total_GAM=('Estimated # of GAM cases', 'sum'),
    Total_SAM=('Estimated # of SAM cases', 'sum'),
    Total_MAM=('Estimated # of MAM cases', 'sum')
).reset_index()
st.dataframe(summary, use_container_width=True)

st.divider()

#Raw data
st.subheader("📋 Raw Dataset")
st.dataframe(filtered_df, use_container_width=True)




