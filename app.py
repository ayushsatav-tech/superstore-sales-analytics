
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Superstore Sales Analytics Dashboard")
st.write("Explore sales, profit and business performance.")

DATA_PATH = Path("data/superstore.csv.csv")

@st.cache_data
def load_data():
    df = df = pd.read_csv(DATA_PATH, encoding="latin1")
    df.columns = df.columns.str.strip()

    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")
    df["Order Date"] = pd.to_datetime(
        df["Order Date"], errors="coerce"
    )

    return df.dropna(subset=["Sales", "Profit", "Region"])

if not DATA_PATH.exists():
    st.error("Dataset not found. Add data/superstore.csv.csv to the repository.")
    st.stop()

df = load_data()

st.sidebar.header("Dashboard Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].dropna().unique()),
    default=sorted(df["Region"].dropna().unique())
)

filtered_df = df[df["Region"].isin(regions)]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
average_sales = filtered_df["Sales"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Average Sales", f"${average_sales:,.2f}")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Sales by Region")
    region_sales = filtered_df.groupby("Region")["Sales"].sum()
    st.bar_chart(region_sales)

with right:
    st.subheader("Profit by Region")
    region_profit = filtered_df.groupby("Region")["Profit"].sum()
    st.bar_chart(region_profit)

st.subheader("Sales vs Profit")

fig, ax = plt.subplots(figsize=(9, 4))
sns.scatterplot(
    data=filtered_df,
    x="Sales",
    y="Profit",
    alpha=0.5,
    ax=ax
)
ax.set_title("Relationship Between Sales and Profit")
st.pyplot(fig)
plt.close(fig)

st.subheader("Monthly Sales Trend")

monthly = (
    filtered_df.dropna(subset=["Order Date"])
    .set_index("Order Date")
    .resample("ME")["Sales"]
    .sum()
)

st.line_chart(monthly)

st.subheader("Dataset Preview")
st.dataframe(filtered_df.head(20), use_container_width=True)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="filtered_superstore.csv.csv",
    mime="text/csv"
)
