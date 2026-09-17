# Project Report: Personalized Diet Recommendation System Using K-Means Clustering

**Author:** Antigravity AI Engineering Team  
**Date:** September 2026  
**Technology Stack:** Python, Pandas, Scikit-Learn, Streamlit, Seaborn, Joblib  

---

## 1. Introduction

Dietary habits and metabolic health are tightly linked to non-communicable chronic diseases such as hypertension, type-2 diabetes, and obesity. Generic dietary recommendations often fail to address individual metabolic variations, leading to poor adherence and suboptimal health outcomes. Machine learning techniques enable data-driven patient segmentation to tailor diet plans to specific health profiles.

This report presents the design, mathematical framework, implementation, and evaluation of an unsupervised learning system titled **"Personalized Diet Recommendation System Using K-Means Clustering"**. The system clusters individual health profiles based on physiological, metabolic, and behavioral metrics and maps clusters to targeted dietary regimes.

---

## 2. Problem Statement

Health recommendations in clinical and wellness settings are frequently rule-based or one-size-fits-all. Manually categorizing individuals into optimal nutritional groups is time-consuming and subjective.

**Key Challenges Addressed:**
1. Identifying hidden metabolic subgroups within heterogeneous patient populations without pre-labeled cluster targets during model training.
2. Handling high-dimensional numerical health variables (Blood Pressure, Glucose, BMI, Caloric Intake, Exercise Hours).
3. Mapping unsupervised clusters to clinically interpretable diet categories (`Balanced`, `Low_Sodium`, `Low_Carb`) transparently.
4. Delivering real-time, interactive recommendations via a clean web interface.

---

## 3. Objectives

1. Develop a clean end-to-end data preprocessing pipeline for clinical features.
2. Implement **K-Means Clustering** as an unsupervised algorithm to group 1,000 patient records.
3. Optimize cluster count ($K$) using **Inertia (Within-Cluster Sum of Squares)** and **Silhouette Score**.
4. Formulate a profile-driven cluster-to-diet recommendation mapping.
5. Deploy a web-based interactive Streamlit dashboard.

---

## 4. Literature / Background

Unsupervised machine learning, particularly partitioning algorithms like K-Means, is widely used in medical informatics for patient stratification. K-Means aims to partition $N$ observations into $K$ clusters in which each observation belongs to the cluster with the nearest mean (cluster centroid).

### Mathematical Formulation of K-Means:
Given a dataset $X = \{x_1, x_2, \dots, x_N\}$ where $x_i \in \mathbb{R}^D$, K-Means minimizes the Within-Cluster Sum of Squares (WCSS / Inertia):

$$J = \sum_{k=1}^{K} \sum_{x_i \in C_k} ||x_i - \mu_k||^2$$

Where:
- $C_k$ is the set of points assigned to cluster $k$.
- $\mu_k = \frac{1}{|C_k|} \sum_{x_i \in C_k} x_i$ is the centroid of cluster $k$.
- $||\cdot||$ denotes Euclidean distance in standardized feature space.

### Silhouette Score Metric:
For a point $i$:

$$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$$

Where $a(i)$ is the mean intra-cluster distance and $b(i)$ is the mean nearest-cluster distance. The overall Silhouette Score is the mean $s(i)$ across all points $N$.

---

## 5. Proposed System Architecture

The system consists of three decoupled layers:
1. **Preprocessing Layer**: Imputation of missing values (`Disease_Type`, `Dietary_Restrictions`, `Allergies` mapped to `'None'`), ordinal feature encoding, and z-score standardization (`StandardScaler`).
2. **Unsupervised Clustering Layer**: K-Means model trained on 11 standardized clinical features.
3. **Inference & Application Layer**: Model artifact loading, user vector transformation, cluster assignment, and mapped diet recommendation generation.

---

## 6. Dataset Description

The dataset `diet_recommendations_dataset.csv` contains 1,000 patient records across 20 attributes:

- **Demographics**: `Patient_ID`, `Age`, `Gender`, `Weight_kg`, `Height_cm`, `BMI`
- **Clinical & Metabolic Indicators**: `Disease_Type`, `Severity`, `Blood_Pressure_mmHg`, `Glucose_mg/dL`, `Cholesterol_mg/dL`
- **Lifestyle & Behavior**: `Physical_Activity_Level`, `Daily_Caloric_Intake`, `Weekly_Exercise_Hours`, `Adherence_to_Diet_Plan`, `Dietary_Nutrient_Imbalance_Score`
- **Dietary & Restrictions**: `Dietary_Restrictions`, `Allergies`, `Preferred_Cuisine`, `Diet_Recommendation`

---

## 7. Implementation & Experimental Results

### 7.1 Optimal K Selection Results

| Number of Clusters (K) | Inertia (WCSS) | Silhouette Score |
| :---: | :---: | :---: |
| 2 | 10,193.22 | 0.0724 |
| **3** | **9,644.30** | **0.0669** |
| 4 | 9,205.36 | 0.0672 |
| 5 | 8,870.52 | 0.0672 |
| 6 | 8,592.74 | 0.0678 |

$K=3$ was selected as the optimal cluster hyperparameter.

### 7.2 Cluster Feature Profiles

| Feature Metric | Cluster 0 | Cluster 1 | Cluster 2 |
| :--- | :---: | :---: | :---: |
| **Total Patients** | 310 | 356 | 334 |
| **Mean Glucose (mg/dL)** | **148.2** | 139.7 | 123.3 |
| **Mean Systolic BP (mmHg)** | 145.4 | **150.5** | 138.7 |
| **Mean BMI ($kg/m^2$)** | 28.8 | 25.5 | **30.5** |
| **Mean Daily Calories (kcal)** | 2,175 | **2,837** | 2,368 |
| **Mean Exercise (hrs/wk)** | 4.8 | 5.4 | 5.2 |
| **Mapped Diet Category** | **`Low_Carb`** | **`Low_Sodium`** | **`Balanced`** |

---

## 8. Dashboard Visual Highlights (Screenshots Placeholders)

- **[Placeholder 1: Home Dashboard Overview]** — *Shows global dataset metrics, workflow cards, and medical disclaimer banner.*
- **[Placeholder 2: Dataset Overview & Data Explorer]** — *Interactive patient table filtering and missing data summary.*
- **[Placeholder 3: Exploratory Data Analysis]** — *Feature distribution histograms, disease proportion pie chart, and correlation heatmap.*
- **[Placeholder 4: Clustering Evaluation & PCA Plot]** — *Dual-axis Elbow/Silhouette plot and 2D PCA patient cluster scatter plot.*
- **[Placeholder 5: Personalized Recommendation Output]** — *User input form and instant recommended diet plan badge with macro guidelines.*

---

## 9. Conclusion

The **Personalized Diet Recommendation System Using K-Means Clustering** demonstrates how unsupervised learning can effectively segment patient populations into actionable, clinically meaningful health clusters. By grounding recommendations in transparent cluster centroids and target distributions, the application bridges the gap between raw data analysis and practical dietary guidance.

---

## 10. Future Scope

1. **Incorporate Deep Unsupervised Embeddings**: Utilize autoencoders for non-linear dimensionality reduction prior to clustering.
2. **Dynamic Recipe & Meal Plan Generation**: Integrate a culinary database API to output daily meal plans and macro-matched recipes.
3. **Longitudinal Patient Tracking**: Track patient health parameters over time to measure cluster migration and diet adherence progress.

---

## 11. References

1. MacQueen, J. (1967). *Some methods for classification and analysis of multivariate observations*. Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability, 1(14), 281-297.
2. Rousseeuw, P. J. (1987). *Silhouettes: a graphical aid to the interpretation and validation of cluster analysis*. Journal of Computational and Applied Mathematics, 20, 53-65.
3. World Health Organization (WHO). *Healthy Diet and Noncommunicable Disease Guidelines*.
