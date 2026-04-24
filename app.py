import streamlit as st
import pandas as pd

#Page Config
st.set_page_config(
    page_title="Nigeria Malnutrition Dashboard",
    page_icon="🇳🇬",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

#Region filter
regions = ["All"] + sorted(df["Region"].unique().tolist())
selected_region = st.sidebar.selectbox("🌍 Select Region", regions)

#Filter Data
if selected_region == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Region"] == selected_region]

st.sidebar.divider()
st.sidebar.markdown(f"**Showing:** {len(filtered_df)} LGAs")

#Title
st.title("🇳🇬 Nigerian Acute Malnutrition Dashboard")
st.caption("Source: Humanitarian Data Exchange (HDX) — 2026")
st.divider()

#KPI Cards
st.subheader("📊 Key Statistics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total LGAs", len(filtered_df))
col2.metric("Total GAM Cases", f"{filtered_df.iloc[:, 5].sum():,.0f}")
col3.metric("Total SAM Cases", f"{filtered_df.iloc[:, 7].sum():,.0f}")
col4.metric("Total MAM Cases", f"{filtered_df.iloc[:, 6].sum():,.0f}")

st.divider()

#Raw Data Table
st.subheader("📋 Raw Dataset")
st.dataframe(filtered_df, use_container_width=True)


