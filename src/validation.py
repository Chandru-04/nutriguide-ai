def validate_user_input(user_data):
    """
    Validate user inputs for NutriGuide AI.
    Returns (is_valid: bool, errors: list of user-friendly error strings)
    """
    errors = []
    
    # 1. Check Safety Disclaimer Acknowledgment
    if not user_data.get('safety_agree', False):
        errors.append("Please acknowledge the Health & Safety Notice by ticking the agreement box before proceeding.")
        
    # 2. Validate Demographics
    age = user_data.get('Age')
    if age is None or not (18 <= age <= 100):
        errors.append("Age must be between 18 and 100 years.")
        
    height = user_data.get('Height_cm')
    if height is None or not (100.0 <= float(height) <= 220.0):
        errors.append("Height must be between 100 cm and 220 cm.")
        
    weight = user_data.get('Weight_kg')
    if weight is None or not (30.0 <= float(weight) <= 200.0):
        errors.append("Weight must be between 30 kg and 200 kg.")

    # 3. Validate Clinical Indicators
    bp = user_data.get('Blood_Pressure_mmHg')
    if bp is not None and not (70 <= int(bp) <= 220):
        errors.append("Blood Pressure must be between 70 mmHg and 220 mmHg.")
        
    glucose = user_data.get('Glucose_mg/dL')
    if glucose is not None and not (50.0 <= float(glucose) <= 350.0):
        errors.append("Fasting Glucose must be between 50 mg/dL and 350 mg/dL.")
        
    cholesterol = user_data.get('Cholesterol_mg/dL')
    if cholesterol is not None and not (100.0 <= float(cholesterol) <= 400.0):
        errors.append("Serum Cholesterol must be between 100 mg/dL and 400 mg/dL.")

    # 4. Validate Lifestyle Metrics
    calories = user_data.get('Daily_Caloric_Intake')
    if calories is not None and not (1000 <= int(calories) <= 5000):
        errors.append("Daily Calorie Intake must be between 1,000 kcal and 5,000 kcal.")
        
    exercise = user_data.get('Weekly_Exercise_Hours')
    if exercise is not None and not (0.0 <= float(exercise) <= 30.0):
        errors.append("Weekly Exercise Hours must be between 0 and 30 hours.")

    is_valid = len(errors) == 0
    return is_valid, errors
