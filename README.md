# NutriGuide AI — Personalized Nutrition Platform

> **AI-powered personalized nutrition guidance based on individual health profiles, metabolic indicators, and lifestyle metrics.**

---

## 🌟 Product Overview

**NutriGuide AI** is a production-ready consumer-facing nutrition guidance application. It leverages **Unsupervised K-Means Machine Learning** to cluster health and lifestyle profiles into clinical subgroups and map them to targeted dietary recommendations (`Balanced`, `Low_Sodium`, `Low_Carb`).

---

## ✨ Key Features

### 👤 User-Facing Features
- **Modern Consumer Experience**: Clean SaaS health-tech dashboard built with a professional light teal theme, accessible typography, and soft cards.
- **4-Step Multi-Step Form**: Guided user onboarding covering *Personal Info*, *Health Profile*, *Lifestyle*, and *Food Preferences* with friendly, human-readable labels (`Body Mass Index`, `Daily Calorie Intake`, `Systolic Blood Pressure`).
- **Input Validation**: Bounds checking for age, weight, height, glucose, blood pressure, and calories with human-readable error messages.
- **Personalized Recommendations**: Instant diet plan category, macro distribution, key foods to include, foods to limit, and clear *"Why this recommendation?"* profile insights.
- **Health & Safety Guarantee**: Mandatory safety acknowledgment checkbox before generating suggestions.
- **Privacy Assurance**: In-memory data processing with zero permanent storage of health parameters.

### ⚙️ Developer & Model Insights Features
- **Dataset Summary**: Inspection of the 1,000 patient reference records and missing value imputation statistics.
- **Evaluation Metrics**: Dual-axis Elbow Method (Inertia WCSS) and Silhouette Score curve visualization ($K \in [2, 8]$).
- **Cluster Profiles**: Mean feature centroids table detailing metabolic risk factors.
- **2D PCA Projection**: Scatter plot visualization of patient clusters in 2-dimensional principal component space.

---

## 🧠 Machine Learning Architecture

```
NutriGuide AI Architecture
│
├── 1. User Input (11 Health & Lifestyle Metrics)
├── 2. Input Validation (src/validation.py)
├── 3. Feature Scaling (StandardScaler fitted during model training)
├── 4. Cluster Assignment (K-Means Clustering, K = 3)
├── 5. Dominant Target Mapping (Low_Carb, Low_Sodium, Balanced)
└── 6. Recommendation Generation (Nutritional Guidelines & Risk Insights)
```

### Clustering Features (11 Standardized Attributes):
- **Clinical & Metabolic**: `Age`, `BMI`, `Blood_Pressure_mmHg`, `Glucose_mg/dL`, `Cholesterol_mg/dL`, `Severity_Code`
- **Lifestyle & Behavior**: `Daily_Caloric_Intake`, `Weekly_Exercise_Hours`, `Adherence_to_Diet_Plan`, `Dietary_Nutrient_Imbalance_Score`, `Physical_Activity_Level_Code`

### Model Performance Metrics ($K=3$):
- **Inertia (WCSS)**: `9644.30`
- **Silhouette Score**: `0.0669`

---

## 📁 Project Directory Structure

```
personalized_diet_recommendation/
│
├── .streamlit/
│   └── config.toml               # Streamlit theme & server configuration
│
├── data/
│   └── diet_recommendations_dataset.csv
│
├── models/
│   ├── kmeans_model.pkl
│   ├── scaler.pkl
│   ├── cluster_mapping.pkl
│   ├── cluster_profiles.pkl
│   ├── evaluation_metrics.pkl
│   └── mapping_details.pkl
│
├── notebooks/
│   └── diet_recommendation_analysis.ipynb
│
├── src/
│   ├── __init__.py
│   ├── validation.py            # Form validation & error checking
│   ├── ui.py                    # Styling, SaaS components, headers, footers
│   ├── preprocessing.py         # Facade for data_preprocessing
│   ├── data_preprocessing.py
│   ├── clustering.py
│   └── recommendation.py
│
├── app.py                        # Main Streamlit application entry point
├── train_model.py
├── requirements.txt              # Cloud & local dependencies
├── README.md
├── PROJECT_REPORT.md
└── .gitignore
```

---

## 🚀 Local Installation & Execution

### 1. Clone & Set Working Directory
```bash
cd personalized_diet_recommendation
```

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. Train Model & Save Artifacts (Optional)
```bash
python train_model.py
```

### 4. Launch NutriGuide AI Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ Deployment Instructions (Streamlit Community Cloud)

1. Push this repository to GitHub.
2. Log into [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New app**, select your repository, branch (`main`), and set Main file path to `app.py`.
4. Streamlit Cloud will automatically detect `.streamlit/config.toml` and `requirements.txt` and launch the platform.

---

## ⚠️ Health & Safety Notice & Privacy Policy

> **DISCLAIMER**: NutriGuide AI provides general nutrition suggestions for educational and informational purposes. It does not diagnose or treat medical conditions and is not a substitute for advice from a qualified doctor or registered dietitian.
>
> **PRIVACY**: All user inputs are processed strictly in-memory to calculate recommendations and are never permanently stored, logged to databases, or tracked across sessions.
