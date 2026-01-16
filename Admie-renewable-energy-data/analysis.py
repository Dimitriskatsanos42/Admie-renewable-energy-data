import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import os

# ============================================================
# ΡΥΘΜΙΣΕΙΣ
# ============================================================
DATA_PATH = "Export_admie_realtimescadares_2026-01-12.csv"
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# ΦΟΡΤΩΣΗ ΚΑΙ ΚΑΘΑΡΙΣΜΟΣ ΔΕΔΟΜΕΝΩΝ
# ============================================================
def load_and_clean():
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.lower().str.strip()

    df = df.rename(columns={
        "date": "datetime",
        "energy_mwh": "energy_mwh"
    })

    df["datetime"] = pd.to_datetime(df["datetime"])
    df["energy_mwh"] = pd.to_numeric(df["energy_mwh"])
    df = df.sort_values("datetime")

    return df

# ============================================================
# 1️⃣ ΑΝΑΛΥΣΗ TIME SERIES (DECOMPOSITION)
# ============================================================
def decomposition(df):
    ts = df.set_index("datetime")["energy_mwh"]

    result = seasonal_decompose(ts, model="additive", period=24)

    result.plot()
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/decomposition.png")
    plt.close()

    print("Αποθηκεύτηκε το διάγραμμα decomposition")

# ============================================================
# 2️⃣ ΕΒΔΟΜΑΔΙΑΙΑ ΠΡΟΤΥΠΑ
# ============================================================
def weekly_patterns(df):
    df["weekday"] = df["datetime"].dt.weekday
    df["day_type"] = np.where(df["weekday"] < 5, "Weekday", "Weekend")

    weekly = df.groupby("day_type")["energy_mwh"].mean()

    weekly.plot(kind="bar")
    plt.title("Μέση Παραγωγή Ενέργειας: Εβδομάδα vs Σαββατοκύριακο")
    plt.ylabel("Μέση Ενέργεια (MWh)")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/weekly_patterns.png")
    plt.close()

    print("Αποθηκεύτηκε το διάγραμμα εβδομαδιαίων προτύπων")

# ============================================================
# 3️⃣ ΠΡΟΒΛΕΨΗ
# ============================================================
def forecasting(df):
    ts = df.set_index("datetime")["energy_mwh"]

    split = int(len(ts) * 0.8)
    train, test = ts[:split], ts[split:]

    # Προβλεψη Naive
    naive_forecast = np.repeat(train.iloc[-1], len(test))

    # Προβλεψη Κινούμενου Μέσου
    window = 24
    rolling_mean = train.rolling(window).mean().iloc[-1]
    ma_forecast = np.repeat(rolling_mean, len(test))

    # Σχεδίαση
    plt.figure(figsize=(10, 5))
    plt.plot(test.index, test.values, label="Πραγματικά")
    plt.plot(test.index, naive_forecast, label="Naive Προβλεψη")
    plt.plot(test.index, ma_forecast, label="Προβλεψη Κινούμενου Μέσου")
    plt.legend()
    plt.title("Προβλέψεις Παραγωγής Ενέργειας")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/forecast.png")
    plt.close()

    return test.values, naive_forecast, ma_forecast

# ============================================================
# 4️⃣ ΑΞΙΟΛΟΓΗΣΗ
# ============================================================
def evaluation(actual, naive, ma):
    metrics = {
        "Model": ["Naive", "Moving Average"],
        "MAE": [
            mean_absolute_error(actual, naive),
            mean_absolute_error(actual, ma)
        ],
        "RMSE": [
            np.sqrt(mean_squared_error(actual, naive)),
            np.sqrt(mean_squared_error(actual, ma))
        ]
    }

    metrics_df = pd.DataFrame(metrics)
    metrics_df.to_csv(f"{OUTPUT_DIR}/metrics.csv", index=False)

    print("Αποθηκεύτηκαν τα metrics αξιολόγησης")

# ============================================================
# MAIN
# ============================================================
def main():
    df = load_and_clean()

    decomposition(df)
    weekly_patterns(df)

    actual, naive, ma = forecasting(df)
    evaluation(actual, naive, ma)

    print("\nΟΛΟΚΛΗΡΩΘΗΚΕ Η ΔΙΑΔΙΚΑΣΙΑ")

if __name__ == "__main__":
    main()
