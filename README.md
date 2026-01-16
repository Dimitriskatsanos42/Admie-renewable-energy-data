# Ανάλυση Ανανεώσιμης Ενέργειας - ADMIE (Ελλάδα)

Αυτό το repository περιέχει Python scripts και εργαλεία για ανάλυση δεδομένων παραγωγής ανανεώσιμης ενέργειας στην Ελλάδα από τον διαχειριστή ADMIE (data.gov.gr).  
Στόχος είναι η **βασική και προχωρημένη ανάλυση χρονοσειρών**, η **ανίχνευση ανωμαλιών**, η μελέτη **εποχικότητας** και η προετοιμασία δεδομένων για περαιτέρω προβλέψεις.

---

## 📂 Περιεχόμενα Repository

| Φάκελος / Αρχείο           | Περιγραφή |
|----------------------------|-----------|
| `data/`                    | Αρχεία CSV με raw δεδομένα παραγωγής (hourly MWh) |
| `outputs/`                 | Όλα τα plots και CSV outputs που παράγονται από τα scripts |
| `scripts/analysis.py`      | Βασική ανάλυση χρονοσειρών: decomposition, weekly patterns, forecasts |
| `scripts/analysis_advanced.py` | Προχωρημένη ανάλυση: heatmap, rolling statistics, ανίχνευση ανωμαλιών |
| `scripts/program.py`       | Ανάλυση ανά energy source και μηνιαία trends |
| `scripts/energy.py`        | Data cleaning, ανίχνευση outliers, hourly & monthly patterns, trend analysis |
| `requirements.txt`         | Απαιτούμενες Python βιβλιοθήκες |
| `.gitignore`               | Αγνοεί outputs, cache, virtual envs, logs |
| `README.md`                | Οδηγός χρήσης και περιγραφή του repository |

---

## 📝 Περιγραφή Scripts

### **1. analysis.py**
- **Τι κάνει:**  
  - Βασική ανάλυση χρονοσειρών (hourly MWh)  
  - Time series decomposition (trend, seasonal, residual)  
  - Weekly patterns (Weekday vs Weekend)  
  - Προβλέψεις με Naive και Moving Average  
  - Υπολογισμός MAE & RMSE
- **Τι παράγει:**  
  - Plots: `decomposition.png`, `weekly_patterns.png`, `forecast.png`  
  - CSV: `metrics.csv` (MAE & RMSE)

### **2. analysis_advanced.py**
- **Τι κάνει:**  
  - Heatmap παραγωγής ανά ώρα και ημέρα  
  - Rolling statistics (μέσος όρος, std dev)  
  - Ανίχνευση ανωμαλιών (outliers)  
- **Τι παράγει:**  
  - Plots: `heatmap_energy.png`, `rolling_stats.png`, `anomalies.png`  
  - CSV: `anomalies.csv`

### **3. program.py**
- **Τι κάνει:**  
  - Ανάλυση παραγωγής ανά πηγή ενέργειας (energy source)  
  - Συνολική παραγωγή ανά πηγή (bar chart)  
  - Μηνιαία παραγωγή ανά source (line chart)  
  - Seasonal trends στη κονσόλα
- **Τι παράγει:**  
  - Plots: `total_production.png`, `monthly_trends.png`

### **4. energy.py**
- **Τι κάνει:**  
  - Καθαρισμός δεδομένων και data quality checks  
  - Ανίχνευση outliers με IQR  
  - Υπολογισμός hourly & monthly patterns  
  - Trend analysis με rolling mean
- **Τι παράγει:**  
  - Plots: `monthly_seasonality.png`, `hourly_patterns.png`, `trend_analysis.png`  
  - CSV: `outliers_report.csv`

---

## ⚙️ Απαιτήσεις / Dependencies

- Python 3.11+  
- pandas  
- numpy  
- matplotlib  
- statsmodels  
- scikit-learn  

**Προαιρετικά για advanced visualizations:**  
- seaborn  
- plotly  

Όλες οι βιβλιοθήκες μπορούν να εγκατασταθούν μέσω του `requirements.txt`:
```bash
pip install -r requirements.txt
