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

#Title
st.title("🇳🇬 Nigerian Acute Malnutrition Dashboard")
st.caption("Source: Humanitarian Data Exchange (HDX) — 2026")
st.divider()

#Show raw data
st.subheader("📋 Raw Dataset")
st.dataframe(df, use_container_width=True)

#Basic Info
st.subheader("📊 Dataset Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Rows", len(df))
col2.metric("Total Columns", len(df.columns))
col3.metric("Regions", df["Region"].nunique())
