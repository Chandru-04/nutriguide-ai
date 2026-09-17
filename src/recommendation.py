import os
import joblib
import pandas as pd
import numpy as np
from src.data_preprocessing import ALL_CLUSTERING_FEATURES, ACTIVITY_MAPPING, SEVERITY_MAPPING

def get_default_models_dir():
    """
    Get absolute path to models folder.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'models')

def load_saved_artifacts(models_dir=None):
    """
    Load saved scaler, kmeans model, and cluster mapping.
    """
    if models_dir is None:
        models_dir = get_default_models_dir()
        
    scaler_path = os.path.join(models_dir, 'scaler.pkl')
    kmeans_path = os.path.join(models_dir, 'kmeans_model.pkl')
    mapping_path = os.path.join(models_dir, 'cluster_mapping.pkl')
    profiles_path = os.path.join(models_dir, 'cluster_profiles.pkl')
    
    if not (os.path.exists(scaler_path) and os.path.exists(kmeans_path) and os.path.exists(mapping_path)):
        raise FileNotFoundError("Model artifacts not found in models/ directory. Run train_model.py first.")
        
    scaler = joblib.load(scaler_path)
    kmeans_model = joblib.load(kmeans_path)
    cluster_mapping = joblib.load(mapping_path)
    
    cluster_profiles = None
    if os.path.exists(profiles_path):
        cluster_profiles = joblib.load(profiles_path)
        
    return scaler, kmeans_model, cluster_mapping, cluster_profiles

def recommend_diet(user_input, models_dir=None):
    """
    Predict K-Means cluster for a user profile and return mapped diet recommendation,
    BMI analysis, health insights, and nutritional guidelines.
    """
    scaler, kmeans_model, cluster_mapping, cluster_profiles = load_saved_artifacts(models_dir)
    
    # Fill defaults for optional user inputs if omitted
    age = float(user_input.get('Age', 45))
    weight = float(user_input.get('Weight_kg', 70.0))
    height = float(user_input.get('Height_cm', 170.0))
    
    # Calculate BMI if missing or zero
    bmi = user_input.get('BMI')
    if bmi is None or float(bmi) <= 0:
        bmi = round(weight / ((height / 100.0) ** 2), 2)
    else:
        bmi = float(bmi)
        
    caloric_intake = float(user_input.get('Daily_Caloric_Intake', 2200))
    cholesterol = float(user_input.get('Cholesterol_mg/dL', 200.0))
    blood_pressure = float(user_input.get('Blood_Pressure_mmHg', 120.0))
    glucose = float(user_input.get('Glucose_mg/dL', 100.0))
    weekly_exercise = float(user_input.get('Weekly_Exercise_Hours', 3.0))
    adherence = float(user_input.get('Adherence_to_Diet_Plan', 75.0))
    imbalance_score = float(user_input.get('Dietary_Nutrient_Imbalance_Score', 2.5))
    
    activity_str = user_input.get('Physical_Activity_Level', 'Moderate')
    activity_code = ACTIVITY_MAPPING.get(activity_str, 1)
    
    severity_str = user_input.get('Severity', 'None')
    severity_code = SEVERITY_MAPPING.get(severity_str, 0)
    
    disease_type = user_input.get('Disease_Type', 'None')
    dietary_restrictions = user_input.get('Dietary_Restrictions', 'None')
    allergies = user_input.get('Allergies', 'None')
    cuisine = user_input.get('Preferred_Cuisine', 'Any')
    
    # Construct feature row matching ALL_CLUSTERING_FEATURES order exactly
    feature_row = pd.DataFrame([{
        'Age': age,
        'BMI': bmi,
        'Daily_Caloric_Intake': caloric_intake,
        'Cholesterol_mg/dL': cholesterol,
        'Blood_Pressure_mmHg': blood_pressure,
        'Glucose_mg/dL': glucose,
        'Weekly_Exercise_Hours': weekly_exercise,
        'Adherence_to_Diet_Plan': adherence,
        'Dietary_Nutrient_Imbalance_Score': imbalance_score,
        'Physical_Activity_Level_Code': activity_code,
        'Severity_Code': severity_code
    }])[ALL_CLUSTERING_FEATURES]
    
    # Scale feature vector
    X_scaled = scaler.transform(feature_row)
    
    # Predict Cluster
    cluster_id = int(kmeans_model.predict(X_scaled)[0])
    
    # Map Cluster to dominant Diet Recommendation
    recommended_diet = cluster_mapping.get(cluster_id, "Balanced")
    
    # Determine BMI Category
    if bmi < 18.5:
        bmi_cat = "Underweight"
    elif 18.5 <= bmi < 25.0:
        bmi_cat = "Normal Weight"
    elif 25.0 <= bmi < 30.0:
        bmi_cat = "Overweight"
    else:
        bmi_cat = "Obese"
        
    # Generate Profile Explanations & Health Insights
    insights = []
    if blood_pressure >= 130:
        insights.append(f"Elevated Blood Pressure ({blood_pressure} mmHg): Sodium reduction is strongly advised.")
    if glucose >= 125:
        insights.append(f"Elevated Blood Glucose ({glucose} mg/dL): Glycemic control with lower carbohydrate intake is indicated.")
    if cholesterol >= 200:
        insights.append(f"Elevated Cholesterol ({cholesterol} mg/dL): Heart-healthy lipid management recommended.")
    if bmi >= 25.0:
        insights.append(f"BMI ({bmi} - {bmi_cat}): Calorie monitoring and nutrient-dense options are recommended.")
    if weekly_exercise < 2.5:
        insights.append(f"Low weekly exercise ({weekly_exercise} hrs/week): Regular aerobic and strength activity recommended.")
        
    if not insights:
        insights.append("Health parameters are within standard optimal ranges; balanced metabolic support recommended.")
        
    # Nutritional Guidelines for Recommended Diet Category
    guidelines = {
        'Balanced': {
            'title': 'Balanced Diet Plan',
            'summary': 'Focuses on an even distribution of macro and micronutrients for total health optimization.',
            'macronutrients': '50% Complex Carbohydrates, 25% Lean Protein, 25% Healthy Fats',
            'recommended_foods': 'Whole grains, fresh vegetables, lean meats (chicken, fish), legumes, nuts, seeds, and fruits.',
            'foods_to_limit': 'Ultra-processed foods, added sugars, refined grains, and trans fats.'
        },
        'Low_Sodium': {
            'title': 'Low Sodium Diet Plan',
            'summary': 'Designed to support cardiovascular health, control blood pressure, and reduce fluid retention.',
            'macronutrients': '55% Complex Carbohydrates, 25% Protein, 20% Healthy Fats (< 1500-2000mg Sodium/day)',
            'recommended_foods': 'Fresh vegetables, unprocessed fruits, unsalted nuts, whole grains, fresh poultry, herbs and spices for seasoning.',
            'foods_to_limit': 'Canned soups, processed meats, pickles, salty snacks, soy sauce, and fast foods.'
        },
        'Low_Carb': {
            'title': 'Low Carbohydrate Diet Plan',
            'summary': 'Targeted at blood glucose regulation, insulin sensitivity improvement, and weight management.',
            'macronutrients': '20-30% Carbohydrates, 35-40% Protein, 35-40% Healthy Fats',
            'recommended_foods': 'Leafy greens, non-starchy vegetables, eggs, fish, lean beef, poultry, olive oil, and avocados.',
            'foods_to_limit': 'Sugary beverages, refined breads, pastries, white rice, potatoes, and high-sugar fruits.'
        }
    }
    
    specific_guideline = guidelines.get(recommended_diet, guidelines['Balanced'])
    
    # Retrieve cluster centroid specs if available
    cluster_centroid = {}
    if cluster_profiles is not None and cluster_id in cluster_profiles.index:
        cluster_centroid = cluster_profiles.loc[cluster_id].to_dict()
        
    return {
        'cluster_id': cluster_id,
        'recommended_diet': recommended_diet,
        'calculated_bmi': bmi,
        'bmi_category': bmi_cat,
        'insights': insights,
        'guidelines': specific_guideline,
        'cluster_centroid': cluster_centroid,
        'user_summary': {
            'Age': age,
            'Disease_Type': disease_type,
            'Severity': severity_str,
            'Physical_Activity_Level': activity_str,
            'Dietary_Restrictions': dietary_restrictions,
            'Allergies': allergies,
            'Preferred_Cuisine': cuisine
        }
    }
