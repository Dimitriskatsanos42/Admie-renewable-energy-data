# =====================================================
# Renewable Energy Analysis - ADMIE Open Data (Greece)
# =====================================================
# Author: Dimitrios katsanos
# Data Source: data.gov.gr (ADMIE)
# =====================================================

import pandas as pd
import matplotlib.pyplot as plt
import os


# -----------------------------------------------------
# 1. LOAD DATA
# -----------------------------------------------------
def load_data(path):
    """
    Loads CSV data from the given path.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    df = pd.read_csv(path)
    return df


# -----------------------------------------------------
# 2. INITIAL INSPECTION
# -----------------------------------------------------
def inspect_data(df):
    """
    Prints basic information about the dataset.
    """
    print("\n--- DATA INFO ---")
    print(df.info())

    print("\n--- COLUMNS ---")
    for col in df.columns:
        print(col)

    print("\n--- FIRST ROWS ---")
    print(df.head())


# -----------------------------------------------------
# 3. CLEAN DATA
# -----------------------------------------------------
def clean_data(df):
    """
    Cleans column names (lowercase, strip, replace spaces).
    """
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
    )
    return df


# -----------------------------------------------------
# 4. COLUMN MAPPING (ΣΗΜΑΝΤΙΚΟ)
# -----------------------------------------------------
def map_columns(df):
    """
    Maps ADMIE column names to standard names.
    Προσαρμοσμένο για CSV με 'date' και 'energy_mwh'
    """
    column_mapping = {
        "date": "datetime",
        "date_time": "datetime",
        "datetime": "datetime",
        "ημερομηνια": "datetime",

        "energy_mwh": "production_mw",
        "value": "production_mw",
        "mw": "production_mw",
        "ισχυς": "production_mw",

        "fuel_type": "energy_source",
        "energy_source": "energy_source",
        "τεχνολογια": "energy_source"
    }

    df = df.rename(columns=column_mapping)

    # Αν δεν υπάρχει energy_source, προσθέτουμε default
    if "energy_source" not in df.columns:
        df["energy_source"] = "unknown"

    required_cols = {"datetime", "energy_source", "production_mw"}
    missing = required_cols - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df


# -----------------------------------------------------
# 5. DATETIME + NA CLEANING
# -----------------------------------------------------
def prepare_data(df):
    """
    Converts datetime and removes missing values.
    """
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    df = df.dropna(subset=["datetime", "energy_source", "production_mw"])
    return df


# -----------------------------------------------------
# 6. TOTAL PRODUCTION PER SOURCE
# -----------------------------------------------------
def total_production(df):
    return (
        df
        .groupby("energy_source")["production_mw"]
        .sum()
        .sort_values(ascending=False)
    )


# -----------------------------------------------------
# 7. PLOT TOTAL PRODUCTION
# -----------------------------------------------------
def plot_total(total):
    plt.figure(figsize=(8, 5))
    total.plot(kind="bar")
    plt.title("Total Renewable Energy Production in Greece")
    plt.xlabel("Energy Source")
    plt.ylabel("Total Production (MW)")
    plt.tight_layout()
    plt.show()


# -----------------------------------------------------
# 8. MONTHLY TIME SERIES
# -----------------------------------------------------
def monthly_production(df):
    df["month"] = df["datetime"].dt.to_period("M")
    return (
        df
        .groupby(["month", "energy_source"])["production_mw"]
        .sum()
        .reset_index()
    )


# -----------------------------------------------------
# 9. PLOT MONTHLY TRENDS
# -----------------------------------------------------
def plot_monthly(monthly):
    plt.figure(figsize=(10, 6))
    for source in monthly["energy_source"].unique():
        data = monthly[monthly["energy_source"] == source]
        plt.plot(
            data["month"].astype(str),
            data["production_mw"],
            label=source
        )
    plt.title("Monthly Renewable Energy Production in Greece")
    plt.xlabel("Month")
    plt.ylabel("Production (MW)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# -----------------------------------------------------
# 10. SEASONALITY ANALYSIS
# -----------------------------------------------------
def seasonality(df):
    df["month_number"] = df["datetime"].dt.month
    return (
        df
        .groupby(["month_number", "energy_source"])["production_mw"]
        .mean()
        .reset_index()
    )


# -----------------------------------------------------
# 11. MAIN
# -----------------------------------------------------
def main():
    # 🔴 ΑΛΛΑΞΕ ΕΔΩ ΤΟ ΟΝΟΜΑ ΑΡΧΕΙΟΥ
    data_path = r"C:\Users\usr1\Documents\Data\Export_admie_realtimescadares_2026-01-12.csv"

    # Load
    df = load_data(data_path)

    # Inspect
    inspect_data(df)

    # Clean + map
    df = clean_data(df)
    df = map_columns(df)
    df = prepare_data(df)

    # Analysis
    total = total_production(df)
    plot_total(total)

    monthly = monthly_production(df)
    plot_monthly(monthly)

    seasonal = seasonality(df)
    print("\n--- SEASONALITY (AVG PER MONTH) ---")
    print(seasonal.head())


# -----------------------------------------------------
# RUN
# -----------------------------------------------------
if __name__ == "__main__":
    main()
