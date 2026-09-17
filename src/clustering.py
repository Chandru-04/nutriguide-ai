import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def evaluate_kmeans_k(X_scaled, min_k=2, max_k=10, random_state=42):
    """
    Evaluate K-Means for a range of K values using Inertia (Elbow method) and Silhouette Score.
    """
    results = []
    
    for k in range(min_k, max_k + 1):
        kmeans = KMeans(n_clusters=k, random_state=random_state, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        inertia = kmeans.inertia_
        sil = silhouette_score(X_scaled, labels)
        
        results.append({
            'k': k,
            'inertia': float(inertia),
            'silhouette_score': float(sil)
        })
        
    return pd.DataFrame(results)

def train_kmeans(X_scaled, n_clusters=3, random_state=42):
    """
    Train K-Means clustering model on scaled features.
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    cluster_labels = kmeans.fit_predict(X_scaled)
    
    inertia = kmeans.inertia_
    sil_score = silhouette_score(X_scaled, cluster_labels)
    
    return kmeans, cluster_labels, inertia, sil_score

def analyze_clusters(df, cluster_labels, feature_cols):
    """
    Generate mean feature profiles for each cluster.
    """
    df_analysis = df.copy()
    df_analysis['Cluster'] = cluster_labels
    
    cluster_profiles = df_analysis.groupby('Cluster')[feature_cols].mean().reset_index()
    return cluster_profiles

def build_cluster_diet_mapping(df, cluster_labels):
    """
    Determine the mapped Diet_Recommendation category for each cluster.
    Uses cluster metabolic profiles (Glucose, Blood Pressure, BMI, Caloric Intake)
    and relative diet target distributions to establish a transparent, distinct mapping.
    
    Returns:
    - cluster_mapping: dict mapping cluster_id -> recommended_diet_category
    - mapping_summary: DataFrame showing counts and percentage distribution
    - crosstab: DataFrame contingency table
    - crosstab_pct: DataFrame percentage contingency table
    """
    df_temp = df.copy()
    df_temp['Cluster'] = cluster_labels
    
    crosstab = pd.crosstab(df_temp['Cluster'], df_temp['Diet_Recommendation'])
    crosstab_pct = pd.crosstab(df_temp['Cluster'], df_temp['Diet_Recommendation'], normalize='index') * 100
    
    # Calculate cluster mean clinical features to assign profile-driven mapping if raw modes overlap
    cluster_means = df_temp.groupby('Cluster')[['Glucose_mg/dL', 'Blood_Pressure_mmHg', 'BMI', 'Daily_Caloric_Intake']].mean()
    
    cluster_mapping = {}
    mapping_details = []
    
    # Define mapping strategy: assign distinct primary recommendation based on dominant metabolic risk profile
    for cluster_id in crosstab.index:
        mean_glucose = cluster_means.loc[cluster_id, 'Glucose_mg/dL']
        mean_bp = cluster_means.loc[cluster_id, 'Blood_Pressure_mmHg']
        mean_bmi = cluster_means.loc[cluster_id, 'BMI']
        
        # Profile-driven mapping assignment based on cluster characteristics:
        if mean_glucose == cluster_means['Glucose_mg/dL'].max():
            assigned_diet = "Low_Carb" # High glucose cluster benefit most from carbohydrate restriction
        elif mean_bp == cluster_means['Blood_Pressure_mmHg'].max():
            assigned_diet = "Low_Sodium" # High BP cluster benefits most from sodium restriction
        else:
            assigned_diet = "Balanced" # Weight & overall metabolic balance cluster
            
        total_pts = crosstab.loc[cluster_id].sum()
        assigned_count = crosstab.loc[cluster_id, assigned_diet]
        assigned_pct = (assigned_count / total_pts) * 100
        
        cluster_mapping[int(cluster_id)] = assigned_diet
        mapping_details.append({
            'Cluster': int(cluster_id),
            'Mapped_Diet_Category': assigned_diet,
            'Category_Patient_Count': int(assigned_count),
            'Total_Cluster_Patients': int(total_pts),
            'Category_Percentage': round(assigned_pct, 2),
            'Mean_Glucose': round(mean_glucose, 1),
            'Mean_Blood_Pressure': round(mean_bp, 1),
            'Mean_BMI': round(mean_bmi, 1)
        })
        
    return cluster_mapping, pd.DataFrame(mapping_details), crosstab, crosstab_pct
