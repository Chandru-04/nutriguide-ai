import os
import joblib
import pandas as pd
import numpy as np

from src.data_preprocessing import (
    load_dataset,
    prepare_clustering_data,
    scale_features,
    ALL_CLUSTERING_FEATURES
)
from src.clustering import (
    evaluate_kmeans_k,
    train_kmeans,
    analyze_clusters,
    build_cluster_diet_mapping
)

def run_training_pipeline(dataset_path=None, models_dir=None):
    """
    Main training pipeline for Personalized Diet Recommendation System using K-Means Clustering.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    if dataset_path is None:
        dataset_path = os.path.join(base_dir, 'data', 'diet_recommendations_dataset.csv')
    if models_dir is None:
        models_dir = os.path.join(base_dir, 'models')
        
    os.makedirs(models_dir, exist_ok=True)
    
    print("=" * 60)
    print("1. LOADING DATASET")
    print("=" * 60)
    df = load_dataset(dataset_path)
    print(f"Dataset Loaded Successfully! Shape: {df.shape}")
    
    print("\n" + "=" * 60)
    print("2. PREPROCESSING & FEATURE ENGINEERING")
    print("=" * 60)
    cleaned_df, encoded_df, X = prepare_clustering_data(df)
    print(f"Cleaned DataFrame Shape: {cleaned_df.shape}")
    print(f"Selected Clustering Features ({len(ALL_CLUSTERING_FEATURES)}):")
    for feat in ALL_CLUSTERING_FEATURES:
        print(f" - {feat}")
        
    print("\n" + "=" * 60)
    print("3. FEATURE STANDARDIZATION")
    print("=" * 60)
    X_scaled, scaler = scale_features(X)
    print(f"Scaled Feature Matrix Shape: {X_scaled.shape}")
    
    print("\n" + "=" * 60)
    print("4. K-MEANS EVALUATION (ELBOW METHOD & SILHOUETTE SCORE)")
    print("=" * 60)
    eval_df = evaluate_kmeans_k(X_scaled, min_k=2, max_k=8, random_state=42)
    print(eval_df.to_string(index=False))
    
    # Pick optimal K (Highest silhouette score or elbow point, default K=3 matching target recommendation count)
    best_k_by_sil = eval_df.loc[eval_df['silhouette_score'].idxmax()]['k']
    optimal_k = int(best_k_by_sil) if best_k_by_sil in [3, 4] else 3
    print(f"\nSelected Optimal K: {optimal_k}")
    
    print("\n" + "=" * 60)
    print(f"5. TRAINING FINAL K-MEANS MODEL (K={optimal_k})")
    print("=" * 60)
    kmeans_model, cluster_labels, inertia, sil_score = train_kmeans(X_scaled, n_clusters=optimal_k, random_state=42)
    print(f"Training Complete!")
    print(f" - Final Inertia: {inertia:.4f}")
    print(f" - Final Silhouette Score: {sil_score:.4f}")
    
    # Add cluster labels to encoded dataframe
    encoded_df['Cluster'] = cluster_labels
    cleaned_df['Cluster'] = cluster_labels
    
    print("\n" + "=" * 60)
    print("6. CLUSTER PROFILING & CHARACTERISTICS")
    print("=" * 60)
    cluster_profiles = analyze_clusters(encoded_df, cluster_labels, ALL_CLUSTERING_FEATURES)
    print(cluster_profiles.T)
    
    print("\n" + "=" * 60)
    print("7. CLUSTER-TO-DIET RECOMMENDATION MAPPING")
    print("=" * 60)
    cluster_mapping, mapping_details, crosstab, crosstab_pct = build_cluster_diet_mapping(cleaned_df, cluster_labels)
    print("\nDominant Diet Mapping:")
    print(mapping_details.to_string(index=False))
    
    print("\nCrosstab (Cluster vs Original Diet_Recommendation):")
    print(crosstab)
    print("\nCrosstab Percentage Distribution (%):")
    print(crosstab_pct.round(2))
    
    print("\n" + "=" * 60)
    print("8. SAVING MODEL ARTIFACTS")
    print("=" * 60)
    joblib.dump(scaler, os.path.join(models_dir, 'scaler.pkl'))
    joblib.dump(kmeans_model, os.path.join(models_dir, 'kmeans_model.pkl'))
    joblib.dump(cluster_mapping, os.path.join(models_dir, 'cluster_mapping.pkl'))
    joblib.dump(cluster_profiles, os.path.join(models_dir, 'cluster_profiles.pkl'))
    joblib.dump(eval_df, os.path.join(models_dir, 'evaluation_metrics.pkl'))
    joblib.dump(mapping_details, os.path.join(models_dir, 'mapping_details.pkl'))
    
    print("Saved all artifacts to:", models_dir)
    print(" - scaler.pkl")
    print(" - kmeans_model.pkl")
    print(" - cluster_mapping.pkl")
    print(" - cluster_profiles.pkl")
    print(" - evaluation_metrics.pkl")
    print(" - mapping_details.pkl")
    
    print("\n" + "=" * 60)
    print("PIPELINE EXECUTED SUCCESSFULLY!")
    print("=" * 60)
    
    return {
        'eval_df': eval_df,
        'optimal_k': optimal_k,
        'inertia': inertia,
        'silhouette_score': sil_score,
        'cluster_mapping': cluster_mapping,
        'mapping_details': mapping_details
    }

if __name__ == '__main__':
    run_training_pipeline()
