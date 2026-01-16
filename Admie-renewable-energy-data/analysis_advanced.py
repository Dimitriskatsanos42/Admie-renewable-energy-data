import pandas as pd
import matplotlib.pyplot as plt
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
    df = df.rename(columns={"date": "datetime", "energy_mwh": "energy_mwh"})
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["energy_mwh"] = pd.to_numeric(df["energy_mwh"])
    df = df.sort_values("datetime")
    return df

# ============================================================
# HEATMAP ανά ώρα και ημέρα της εβδομάδας
# ============================================================
def plot_heatmap(df):
    df["weekday"] = df["datetime"].dt.day_name()  # πχ Monday
    df["hour"] = df["datetime"].dt.hour

    pivot = df.pivot_table(index="weekday", columns="hour", values="energy_mwh", aggfunc="mean")
    
    # Ταξινόμηση ημερών σωστά
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = pivot.reindex(days_order)

    plt.figure(figsize=(12, 6))
    plt.imshow(pivot, aspect="auto", cmap="viridis")
    plt.colorbar(label="Μέση Ενέργεια (MWh)")
    plt.xticks(ticks=np.arange(24), labels=np.arange(24))
    plt.yticks(ticks=np.arange(7), labels=days_order)
    plt.xlabel("Ώρα ημέρας")
    plt.ylabel("Ημέρα εβδομάδας")
    plt.title("Heatmap Παραγωγής Ενέργειας ανά Ώρα και Ημέρα")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/heatmap_energy.png")
    plt.close()
    print("Αποθηκεύτηκε heatmap_energy.png")

# ============================================================
# ROLLING ΣΤΑΤΙΣΤΙΚΑ
# ============================================================
def plot_rolling_stats(df, window=24):
    ts = df.set_index("datetime")["energy_mwh"]
    rolling_mean = ts.rolling(window=window).mean()
    rolling_std = ts.rolling(window=window).std()

    plt.figure(figsize=(12, 5))
    plt.plot(ts.index, ts.values, label="Πραγματικά", color="blue")
    plt.plot(rolling_mean.index, rolling_mean.values, label=f"Rolling Mean ({window}h)", color="red")
    plt.fill_between(rolling_std.index, rolling_mean - rolling_std, rolling_mean + rolling_std, color="orange", alpha=0.2, label="Rolling Std Dev")
    plt.title("Rolling Mean και Std Dev Παραγωγής Ενέργειας")
    plt.xlabel("Χρόνος")
    plt.ylabel("Ενέργεια (MWh)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/rolling_stats.png")
    plt.close()
    print("Αποθηκεύτηκε rolling_stats.png")

# ============================================================
# ΑΝΙΧΝΕΥΣΗ ΑΝΩΜΑΛΙΩΝ
# ============================================================
def detect_anomalies(df, threshold=3):
    ts = df.set_index("datetime")["energy_mwh"]
    rolling_mean = ts.rolling(window=24).mean()
    rolling_std = ts.rolling(window=24).std()

    anomalies = ts[(ts - rolling_mean).abs() > threshold * rolling_std]

    plt.figure(figsize=(12, 5))
    plt.plot(ts.index, ts.values, label="Πραγματικά", color="blue")
    plt.scatter(anomalies.index, anomalies.values, color="red", label="Ανωμαλίες")
    plt.title("Ανίχνευση Ανωμαλιών Παραγωγής Ενέργειας")
    plt.xlabel("Χρόνος")
    plt.ylabel("Ενέργεια (MWh)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/anomalies.png")
    plt.close()
    print("Αποθηκεύτηκε anomalies.png")

    # Αποθήκευση anomalies σε CSV
    anomalies_df = anomalies.reset_index()
    anomalies_df.to_csv(f"{OUTPUT_DIR}/anomalies.csv", index=False)
    print("Αποθηκεύτηκε anomalies.csv")

# ============================================================
# MAIN
# ============================================================
def main():
    df = load_and_clean()
    plot_heatmap(df)
    plot_rolling_stats(df)
    detect_anomalies(df)
    print("\nΟΛΟΚΛΗΡΩΘΗΚΕ Η ΠΡΟΧΩΡΗΜΕΝΗ ΑΝΑΛΥΣΗ")

if __name__ == "__main__":
    main()
