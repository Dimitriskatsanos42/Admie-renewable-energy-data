# ============================================================
# ADMIE Renewable Energy Production Analysis (Greece)
# ============================================================
# Dataset: Hourly renewable energy production (MWh)
# Source: data.gov.gr - ADMIE
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import os


# ============================================================
# CONFIG
# ============================================================
DATA_PATH = "Export_admie_realtimescadares_2026-01-12.csv"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# 1. LOAD DATA
# ============================================================
def load_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    return pd.read_csv(path)


# ============================================================
# 2. INSPECT DATA
# ============================================================
def inspect_data(df):
    print("\n--- COLUMNS ---")
    print(df.columns.tolist())

    print("\n--- FIRST ROWS ---")
    print(df.head())


# ============================================================
# 3. CLEAN DATA
# ============================================================
def clean_data(df):
    df.columns = df.columns.str.lower().str.strip()

    df = df.rename(columns={
        "date": "datetime",
        "energy_mwh": "energy_mwh"
    })

    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    df["energy_mwh"] = pd.to_numeric(df["energy_mwh"], errors="coerce")

    df = df.dropna()
    df = df[df["energy_mwh"] >= 0]

    return df


# ============================================================
# 4. DATA QUALITY – OUTLIERS (IQR)
# ============================================================
def detect_outliers(df):
    q1 = df["energy_mwh"].quantile(0.25)
    q3 = df["energy_mwh"].quantile(0.75)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = df[(df["energy_mwh"] < lower) | (df["energy_mwh"] > upper)]
    outliers.to_csv(f"{OUTPUT_DIR}/outliers_report.csv", index=False)

    print(f"✔ Outliers detected: {len(outliers)}")


# ============================================================
# 5. MONTHLY SEASONALITY
# ============================================================
def monthly_seasonality(df):
    df["month"] = df["datetime"].dt.month

    monthly = df.groupby("month")["energy_mwh"].mean()

    plt.figure(figsize=(8, 5))
    monthly.plot(marker="o")
    plt.title("Average Monthly Renewable Energy Production (MWh)")
    plt.xlabel("Month")
    plt.ylabel("Average Energy (MWh)")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/monthly_seasonality.png")
    plt.close()

    print("✔ Monthly seasonality plot saved")


# ============================================================
# 6. HOURLY PATTERNS
# ============================================================
def hourly_patterns(df):
    df["hour"] = df["datetime"].dt.hour

    hourly = df.groupby("hour")["energy_mwh"].mean()

    plt.figure(figsize=(8, 5))
    hourly.plot(marker="o")
    plt.title("Average Hourly Renewable Energy Production")
    plt.xlabel("Hour of Day")
    plt.ylabel("Average Energy (MWh)")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/hourly_patterns.png")
    plt.close()

    print("✔ Hourly pattern plot saved")


# ============================================================
# 7. TREND ANALYSIS (ROLLING MEAN)
# ============================================================
def trend_analysis(df):
    df = df.sort_values("datetime")
    df["rolling_7d"] = df["energy_mwh"].rolling(24 * 7).mean()

    plt.figure(figsize=(10, 5))
    plt.plot(df["datetime"], df["energy_mwh"], alpha=0.3, label="Hourly")
    plt.plot(df["datetime"], df["rolling_7d"], color="red", label="7-day rolling mean")
    plt.title("Renewable Energy Production Trend")
    plt.xlabel("Date")
    plt.ylabel("Energy (MWh)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/trend_analysis.png")
    plt.close()

    print("✔ Trend analysis plot saved")


# ============================================================
# MAIN
# ============================================================
def main():
    df = load_data(DATA_PATH)

    inspect_data(df)

    df = clean_data(df)

    detect_outliers(df)
    monthly_seasonality(df)
    hourly_patterns(df)
    trend_analysis(df)

    print("\n🎉 ANALYSIS COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()
