import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Define standard feature lists and categorical mappings
CLUSTERING_NUMERICAL_FEATURES = [
    'Age',
    'BMI',
    'Daily_Caloric_Intake',
    'Cholesterol_mg/dL',
    'Blood_Pressure_mmHg',
    'Glucose_mg/dL',
    'Weekly_Exercise_Hours',
    'Adherence_to_Diet_Plan',
    'Dietary_Nutrient_Imbalance_Score'
]

CLUSTERING_ENCODED_FEATURES = [
    'Physical_Activity_Level_Code',
    'Severity_Code'
]

ALL_CLUSTERING_FEATURES = CLUSTERING_NUMERICAL_FEATURES + CLUSTERING_ENCODED_FEATURES

ACTIVITY_MAPPING = {'Sedentary': 0, 'Moderate': 1, 'Active': 2}
SEVERITY_MAPPING = {'None': 0, 'Mild': 1, 'Moderate': 2, 'Severe': 3}
GENDER_MAPPING = {'Male': 0, 'Female': 1}

def load_dataset(filepath):
    """
    Load dataset from CSV file path.
    """
    df = pd.read_csv(filepath)
    return df

def clean_dataset(df):
    """
    Clean dataset by handling missing values and verifying data types.
    """
    df_clean = df.copy()
    
    # Handle missing values
    df_clean['Disease_Type'] = df_clean['Disease_Type'].fillna('None')
    df_clean['Dietary_Restrictions'] = df_clean['Dietary_Restrictions'].fillna('None')
    df_clean['Allergies'] = df_clean['Allergies'].fillna('None')
    
    # If BMI is missing or needs recalculation, ensure Weight and Height are present
    if 'BMI' in df_clean.columns and 'Weight_kg' in df_clean.columns and 'Height_cm' in df_clean.columns:
        calculated_bmi = df_clean['Weight_kg'] / ((df_clean['Height_cm'] / 100) ** 2)
        df_clean['BMI'] = df_clean['BMI'].fillna(calculated_bmi)
    
    return df_clean

def encode_features(df):
    """
    Encode ordinal categorical variables for numerical clustering.
    """
    df_encoded = df.copy()
    
    df_encoded['Physical_Activity_Level_Code'] = df_encoded['Physical_Activity_Level'].map(ACTIVITY_MAPPING).fillna(1).astype(int)
    df_encoded['Severity_Code'] = df_encoded['Severity'].map(SEVERITY_MAPPING).fillna(0).astype(int)
    if 'Gender' in df_encoded.columns:
        df_encoded['Gender_Code'] = df_encoded['Gender'].map(GENDER_MAPPING).fillna(0).astype(int)
        
    return df_encoded

def prepare_clustering_data(df):
    """
    Full pipeline to clean, encode, and extract features matrix X.
    """
    cleaned_df = clean_dataset(df)
    encoded_df = encode_features(cleaned_df)
    
    X = encoded_df[ALL_CLUSTERING_FEATURES].copy()
    return cleaned_df, encoded_df, X

def scale_features(X, scaler=None):
    """
    Scale features using StandardScaler. Fits new scaler if scaler is None.
    """
    if scaler is None:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
    else:
        X_scaled = scaler.transform(X)
        
    return X_scaled, scaler
