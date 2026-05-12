import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="SACCO Dashboard", layout="wide")

# Title
st.title("📊 SACCO Financial Dashboard")

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv("data.csv")
    data['Date'] = pd.to_datetime(data['Date'])
    return data

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Data")

branch = st.sidebar.multiselect(
    "Select Branch",
    options=df["Branch"].unique(),
    default=df["Branch"].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["Date"].min(), df["Date"].max()]
)

# Apply filters
filtered_df = df[
    (df["Branch"].isin(branch)) &
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
]

# KPIs
total_deposits = filtered_df["Deposits"].sum()
total_loans = filtered_df["Loans"].sum()
total_repayments = filtered_df["Repayments"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Total Deposits (KES)", f"{total_deposits:,}")
col2.metric("Total Loans (KES)", f"{total_loans:,}")
col3.metric("Total Repayments (KES)", f"{total_repayments:,}")

# Charts
st.subheader("📈 Trends Over Time")

st.line_chart(filtered_df.set_index("Date")[["Deposits", "Loans", "Repayments"]])

# Branch analysis
st.subheader("🏢 Branch Performance")

branch_data = filtered_df.groupby("Branch")[["Deposits", "Loans", "Repayments"]].sum()

st.bar_chart(branch_data)

# Raw data
st.subheader("📋 Data Table")
st.dataframe(filtered_df)

# Download button
st.download_button(
    label="Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)