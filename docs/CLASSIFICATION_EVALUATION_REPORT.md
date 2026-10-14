# Phase 5: CPCB Health Hazard Classification Report

**Model:** Spark MLlib `RandomForestClassifier` (50 trees, maxDepth=8)  
**Target:** Future 24-Hour CPCB Air Quality Tier (0: Good to 5: Severe)  

---

## 1. Classification Performance Metrics

- **Test Accuracy:** `70.21%`
- **Weighted F1-Score:** `0.676`
- **Weighted Precision:** `0.674`
- **Weighted Recall:** `0.702`
- **Spark Cluster Training Time:** `3.48 seconds`

---

## 2. Confusion Matrix (True vs Predicted Counts)

| True Category \ Pred | Good (0) | Satisfactory (1) | Moderate (2) | Poor (3) | Very Poor (4) | Severe (5) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Good (0)** | 0 | 19 | 0 | 0 | 0 | 0 |
| **Satisfactory (1)** | 0 | 962 | 69 | 0 | 0 | 6 |
| **Moderate (2)** | 0 | 211 | 378 | 48 | 0 | 2 |
| **Poor (3)** | 0 | 9 | 204 | 79 | 0 | 1 |
| **Very Poor (4)** | 0 | 5 | 12 | 4 | 0 | 0 |
| **Severe (5)** | 0 | 0 | 12 | 0 | 0 | 0 |