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

# Top N slider
top_n = st.sidebar.slider("🔢 Top N LGAs to Display", min_value=5, max_value=20, value=10)

st.sidebar.divider()

# Navigation
page = st.sidebar.selectbox("📄 Navigate", ["Home", "Charts", "About"])

# Filter data
if selected_region == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Region"] == selected_region]

st.sidebar.divider()
st.sidebar.markdown(f"**Showing:** {len(filtered_df)} LGAs")

#Column Mapping
col_map = {
    "GAM": "Estimated # of GAM cases",
    "SAM": "Estimated # of SAM cases",
    "MAM": "Estimated # of MAM cases"
}
selected_col = col_map[malnutrition_type]
lga_col = "Local Goverment area"
region_col = "Region"

# =====================
# HOME PAGE
# =====================
if page == "Home":
    st.title("🇳🇬 Nigerian Acute Malnutrition Dashboard")
    st.caption("Source: Humanitarian Data Exchange (HDX) — 2026")
    st.divider()

    # KPI Cards
    st.subheader("📊 Key Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total LGAs", len(filtered_df))
    col2.metric("Total GAM Cases",
                f"{filtered_df['Estimated # of GAM cases'].sum():,.0f}")
    col3.metric("Total SAM Cases",
                f"{filtered_df['Estimated # of SAM cases'].sum():,.0f}")
    col4.metric("Total MAM Cases",
                f"{filtered_df['Estimated # of MAM cases'].sum():,.0f}")

    st.divider()

    # Insight box
    st.markdown("""
    <div class="insight-box">
    💡 <b>Key Insight:</b> North-West Nigeria has the highest number of acute malnutrition 
    cases across all categories. Use the filters on the left to explore specific regions 
    and malnutrition types.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Regional Summary Table
    st.subheader("📋 Regional Summary")
    summary = df.groupby(region_col).agg(
        Total_LGAs=(lga_col, 'count'),
        Total_GAM=('Estimated # of GAM cases', 'sum'),
        Total_SAM=('Estimated # of SAM cases', 'sum'),
        Total_MAM=('Estimated # of MAM cases', 'sum')
    ).reset_index()
    st.dataframe(summary, use_container_width=True)

    st.divider()

    # Raw Data
    st.subheader("📋 Raw Dataset")
    st.dataframe(filtered_df, use_container_width=True)

# =====================
# CHARTS PAGE
# =====================
elif page == "Charts":
    st.title("📊 Data Visualisations")
    st.caption("Interactive charts — use sidebar filters to explore")
    st.divider()

    # Row 1: Bar + Pie
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader(f"🏆 Top {top_n} LGAs by {malnutrition_type} Cases")
        top_n_df = filtered_df.nlargest(top_n, selected_col)
        fig1 = px.bar(
            top_n_df,
            x=selected_col,
            y=lga_col,
            orientation='h',
            color=region_col,
            title=f"Top {top_n} LGAs by {malnutrition_type} Cases",
            labels={selected_col: f"{malnutrition_type} Cases", lga_col: "LGA"},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig1.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown(f"""
        <div class="insight-box">
        💡 The top {top_n} LGAs account for a significant proportion of 
        {malnutrition_type} cases. Adjust the slider to see more or fewer LGAs.
        </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        st.subheader(f"🥧 {malnutrition_type} Cases by Region")
        region_summary = filtered_df.groupby(region_col)[selected_col].sum().reset_index()
        fig2 = px.pie(
            region_summary,
            names=region_col,
            values=selected_col,
            title=f"{malnutrition_type} Distribution by Region",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("""
        <div class="insight-box">
        💡 The donut chart shows how malnutrition cases are distributed 
        across the three regions of Northern Nigeria.
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Row 2: Grouped bar
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
        labels={"value": "Number of Cases", "variable": "Type"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("""
    <div class="insight-box">
    💡 MAM cases are consistently higher than SAM cases across all regions, 
    with North-West showing the highest overall burden of malnutrition.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Row 3: Scatter plot
    st.subheader("🔵 GAM % vs Total Children Population")
    fig4 = px.scatter(
        filtered_df,
        x="Total #",
        y="Combined GAM percent",
        color=region_col,
        hover_name=lga_col,
        size="Estimated # of GAM cases",
        title="GAM % vs Total Children Population by LGA",
        labels={
            "Total #": "Total Children Under 5",
            "Combined GAM percent": "GAM %"
        },
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("""
    <div class="insight-box">
    💡 Each bubble represents an LGA. Larger bubbles indicate more GAM cases. 
    Hover over a bubble to see the LGA name and details.
    </div>
    """, unsafe_allow_html=True)

# =====================
# ABOUT PAGE
# =====================
elif page == "About":
    st.title("ℹ️ About This Dashboard")
    st.divider()

    st.markdown("""
    ## 📌 Purpose
    This dashboard was developed as part of the **5DATA004C Data Science Project 
    Lifecycle** individual coursework at the **University of Westminster**.

    It presents an interactive analysis of **acute malnutrition data** across 
    Northern Nigeria, sourced from the **Humanitarian Data Exchange (HDX)**.

    ## 📊 Dataset
    - **Source:** Humanitarian Data Exchange (HDX)
    - **Coverage:** North-Central, North-East, and North-West Nigeria
    - **Period:** April–September 2026
    - **Records:** 209 Local Government Areas (LGAs)

    ## 🔍 Key Metrics Explained
    - **GAM** — Global Acute Malnutrition: includes both MAM and SAM
    - **MAM** — Moderate Acute Malnutrition: moderate level of malnutrition
    - **SAM** — Severe Acute Malnutrition: most critical, life-threatening level

    ## 🛠️ Tools Used
    - **Python** — data processing and analysis
    - **Streamlit** — interactive web dashboard
    - **Plotly** — interactive charts and visualisations
    - **Pandas** — data manipulation
    - **GitHub** — version control

    ## 👩‍💻 Developer
    - **Name:** Aida Passela
    - **Student ID:** W2120549
    - **Module:** 5DATA004C Data Science Project Lifecycle
    """)

