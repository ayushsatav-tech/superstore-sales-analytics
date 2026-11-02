
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

DATA_PATH = Path("data/superstore.csv")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            "Dataset not found. Add superstore.csv inside the data folder."
        )

    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()

    required_columns = [
        "Sales", "Profit", "Region", "Order ID", "Order Date"
    ]

    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")
    df["Order Date"] = pd.to_datetime(
        df["Order Date"], errors="coerce"
    )

    df = df.dropna(subset=["Sales", "Profit", "Region"])
    df = df.drop_duplicates()

    return df


def show_summary(df):
    print("\n--- SALES ANALYSIS SUMMARY ---")
    print("Total Sales:", round(df["Sales"].sum(), 2))
    print("Total Profit:", round(df["Profit"].sum(), 2))
    print("Total Orders:", df["Order ID"].nunique())
    print("Average Sales:", round(df["Sales"].mean(), 2))


def region_analysis(df):
    region_sales = df.groupby("Region")["Sales"].sum().sort_values(
        ascending=False
    )

    print("\n--- SALES BY REGION ---")
    print(region_sales)

    plt.figure(figsize=(9, 5))
    sns.barplot(x=region_sales.index, y=region_sales.values)
    plt.title("Sales by Region")
    plt.xlabel("Region")
    plt.ylabel("Total Sales")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "region_sales.png")
    plt.close()


def profit_analysis(df):
    plt.figure(figsize=(9, 5))
    sns.scatterplot(data=df, x="Sales", y="Profit", alpha=0.5)
    plt.title("Sales vs Profit")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "sales_profit.png")
    plt.close()


def monthly_analysis(df):
    monthly = (
        df.dropna(subset=["Order Date"])
        .set_index("Order Date")
        .resample("ME")["Sales"]
        .sum()
    )

    print("\n--- MONTHLY SALES ---")
    print(monthly)

    plt.figure(figsize=(10, 5))
    monthly.plot()
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "monthly_sales.png")
    plt.close()


if __name__ == "__main__":
    data = load_data()
    show_summary(data)
    region_analysis(data)
    profit_analysis(data)
    monthly_analysis(data)
    print("\nAnalysis completed. Check the outputs folder.")
