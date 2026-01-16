# Ανάλυση Ανανεώσιμης Ενέργειας - ADMIE (Ελλάδα)

Αυτό το repository περιέχει Python scripts και εργαλεία για ανάλυση δεδομένων παραγωγής ανανεώσιμης ενέργειας στην Ελλάδα από τον διαχειριστή ADMIE (data.gov.gr). Το repository χρησιμοποιείται για βασική και προχωρημένη ανάλυση χρονοσειρών, ανίχνευση ανωμαλιών, και εποχικότητα.

---

## Δομή Repository


---

## Περιγραφή Scripts

### **1. analysis.py**
- **Τι κάνει:**  
  - Βασική ανάλυση χρονοσειρών για παραγωγή ενέργειας (hourly MWh)  
  - Time series decomposition (trend, seasonal, residual)  
  - Weekly patterns (Weekday vs Weekend)  
  - Προβλέψεις με Naive και Moving Average  
  - Υπολογισμός MAE & RMSE
- **Τι εμφανίζει / παράγει:**  
  - Plots: `decomposition.png`, `weekly_patterns.png`, `forecast.png`  
  - CSV metrics: `metrics.csv`  

---

### **2. analysis_advanced.py**
- **Τι κάνει:**  
  - Προχωρημένη ανάλυση χρονοσειρών  
  - Heatmap παραγωγής ανά ώρα και ημέρα  
  - Rolling statistics (μέσος όρος και std dev)  
  - Ανίχνευση ανωμαλιών (outliers)
- **Τι εμφανίζει / παράγει:**  
  - Plots: `heatmap_energy.png`, `rolling_stats.png`, `anomalies.png`  
  - CSV: `anomalies.csv`  

---

### **3. program.py**
- **Τι κάνει:**  
  - Ανάλυση παραγωγής ανά πηγή ενέργειας (energy source)  
  - Συνολική παραγωγή ανά πηγή (bar chart)  
  - Μηνιαία παραγωγή ανά source (line chart)  
  - Seasonal trends στη κονσόλα
- **Τι εμφανίζει / παράγει:**  
  - Plots: `total_production.png`, `monthly_trends.png`  

---

### **4. energy.py**
- **Τι κάνει:**  
  - Καθαρισμός και data quality των δεδομένων  
  - Ανίχνευση outliers με IQR  
  - Υπολογισμός hourly & monthly patterns  
  - Trend analysis με rolling mean  
- **Τι εμφανίζει / παράγει:**  
  - Plots: `monthly_seasonality.png`, `hourly_patterns.png`, `trend_analysis.png`  
  - CSV: `outliers_report.csv`  

---

## Οδηγίες Χρήσης

1. **Clone το repository:**
```bash
git clone https://github.com/<username>/admie-renewable-energy-data.git
cd admie-renewable-energy-data
