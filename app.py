import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import joblib
import os

from src.preprocessing import (
    load_dataset, clean_dataset, encode_features, scale_features, ALL_CLUSTERING_FEATURES
)
from src.recommendation import recommend_diet
from src.validation import validate_user_input
from src.ui import (
    inject_custom_css,
    render_hero,
    render_benefit_cards,
    render_how_it_works,
    render_disclaimer,
    render_privacy_notice,
    render_footer
)

# Relative Asset Paths
base_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(base_dir, 'assets', 'nutriguide_logo.png')

# Page Setup
st.set_page_config(
    page_title="NutriGuide AI – Personalized Nutrition",
    page_icon=logo_path if os.path.exists(logo_path) else "🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom CSS
inject_custom_css()

# Set Matplotlib Theme
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#E2E8F0'

# -----------------------------------------------------------------------------
# CACHED DATA & ARTIFACT LOADERS
# -----------------------------------------------------------------------------
@st.cache_data
def load_app_data():
    data_path = os.path.join(base_dir, 'data', 'diet_recommendations_dataset.csv')
    df_raw = load_dataset(data_path)
    df_clean = clean_dataset(df_raw)
    df_encoded = encode_features(df_clean)
    return df_raw, df_clean, df_encoded

@st.cache_resource
def load_model_artifacts():
    models_dir = os.path.join(base_dir, 'models')
    
    scaler = joblib.load(os.path.join(models_dir, 'scaler.pkl'))
    kmeans_model = joblib.load(os.path.join(models_dir, 'kmeans_model.pkl'))
    cluster_mapping = joblib.load(os.path.join(models_dir, 'cluster_mapping.pkl'))
    cluster_profiles = joblib.load(os.path.join(models_dir, 'cluster_profiles.pkl'))
    eval_df = joblib.load(os.path.join(models_dir, 'evaluation_metrics.pkl'))
    mapping_details = joblib.load(os.path.join(models_dir, 'mapping_details.pkl'))
    
    return scaler, kmeans_model, cluster_mapping, cluster_profiles, eval_df, mapping_details

# Safely load data & models
try:
    df_raw, df_clean, df_encoded = load_app_data()
    scaler, kmeans_model, cluster_mapping, cluster_profiles, eval_df, mapping_details = load_model_artifacts()
except Exception as e:
    st.error(f"Error initializing NutriGuide AI system artifacts: {str(e)}")

# Initialize Session State for Wizard & Result View
if 'nav_page' not in st.session_state:
    st.session_state['nav_page'] = 'Home'
if 'rec_result' not in st.session_state:
    st.session_state['rec_result'] = None

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<div style='padding-top: 0.5rem;'></div>", unsafe_allow_html=True)
    if os.path.exists(logo_path):
        st.image(logo_path, width=70)
        
    st.markdown("""
    <div style="padding: 0.2rem 0 0.8rem 0;">
        <h3 style="margin: 0.2rem 0 0 0; color: #0F172A; font-weight: 800; font-size: 1.35rem;">NutriGuide AI</h3>
        <p style="margin: 0; color: #64748B; font-size: 0.8rem; font-weight: 500;">Personalized Nutrition Platform</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='margin: 0.5rem 0 1.25rem 0; border-color: #E2E8F0;'>", unsafe_allow_html=True)

    page_choice = st.radio(
        "Menu",
        [
            "🏠 Home",
            "🥗 Get Recommendation",
            "❓ How It Works",
            "ℹ️ About",
            "⚙️ Developer / Model Insights"
        ],
        index=0
    )

    st.markdown("<hr style='margin: 1.5rem 0; border-color: #E2E8F0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: #F0FDFA; border: 1px solid #CCFBF1; padding: 0.9rem; border-radius: 12px; font-size: 0.825rem; color: #0F766E;">
        🛡️ <strong>NutriGuide Safety Guarantee</strong><br>
        AI-generated general nutrition suggestions. Non-clinical & privacy preserving.
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PAGE 1: 🏠 HOME
# -----------------------------------------------------------------------------
if page_choice == "🏠 Home":
    render_hero(logo_path=logo_path)
    
    # CTA Buttons
    col_cta1, col_cta2, col_space = st.columns([1.5, 1.5, 3])
    with col_cta1:
        if st.button("🥗 Get My Recommendation", type="primary", use_container_width=True):
            st.session_state['nav_page'] = 'Get Recommendation'
            st.rerun()
    with col_cta2:
        if st.button("❓ Learn How It Works", use_container_width=True):
            st.session_state['nav_page'] = 'How It Works'
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 🌟 Why Choose NutriGuide AI?")
    render_benefit_cards()

    st.markdown("<br><br>", unsafe_allow_html=True)
    render_how_it_works()

    st.markdown("<br>", unsafe_allow_html=True)
    render_disclaimer()
    render_privacy_notice()

# -----------------------------------------------------------------------------
# PAGE 2: 🥗 GET RECOMMENDATION (MULTI-STEP ONBOARDING FORM)
# -----------------------------------------------------------------------------
elif page_choice == "🥗 Get Recommendation":
    st.markdown("### 🥗 Get Your Personalized Diet Suggestion")
    st.write("Complete the multi-step profile below to receive data-driven nutrition suggestions.")

    # Check if a recommendation result already exists
    if st.session_state['rec_result'] is not None:
        res = st.session_state['rec_result']
        u_data = st.session_state.get('last_user_data', {})

        st.markdown(f"""
        <div class="result-card">
            <div style="margin-bottom: 0.5rem;">
                <span class="result-diet-badge">{res['recommended_diet']} Diet</span>
            </div>
            <h2 style="color: #0F172A; font-weight: 800; margin-top: 1rem; margin-bottom: 0.5rem;">
                Plan: {res['guidelines']['title']}
            </h2>
            <p style="color: #334155; font-size: 1.05rem; line-height: 1.6;">
                {res['guidelines']['summary']}
            </p>
            <hr style="border-color: #CBD5E1; margin: 1.25rem 0;">
            <div style="color: #1E293B; font-size: 0.95rem; line-height: 1.8;">
                <p><strong>📊 Body Mass Index (BMI):</strong> {res['calculated_bmi']} kg/m² ({res['bmi_category']})</p>
                <p><strong>🥗 Recommended Macro Ratio:</strong> {res['guidelines']['macronutrients']}</p>
                <p><strong>✅ Key Foods to Include:</strong> {res['guidelines']['recommended_foods']}</p>
                <p><strong>⚠️ Foods to Limit:</strong> {res['guidelines']['foods_to_limit']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🔍 Why this recommendation?")
        st.write("Based on your input metrics, the system identified the following health characteristics:")
        for insight in res['insights']:
            st.markdown(f"- **{insight}**")

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🛠️ Technical Details (Model Analysis)"):
            st.write(f"- **Assigned Cluster:** Cluster {res['cluster_id']}")
            st.write(f"- **Cluster Profile Mean BMI:** {res.get('cluster_centroid', {}).get('BMI', 'N/A')}")
            st.write(f"- **Cluster Profile Mean Glucose:** {res.get('cluster_centroid', {}).get('Glucose_mg/dL', 'N/A')} mg/dL")

        st.markdown("<br>", unsafe_allow_html=True)
        col_b1, col_b2, col_b3 = st.columns([1, 1, 1])
        with col_b1:
            if st.button("🔄 Start Over", use_container_width=True):
                st.session_state['rec_result'] = None
                st.rerun()

        render_disclaimer()

    else:
        # Multi-Step Form Layout
        with st.form("onboarding_form"):
            st.markdown("#### 👤 Step 1: Personal Information")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                age = st.number_input("Age (Years):", min_value=18, max_value=100, value=48, step=1)
            with c2:
                gender = st.selectbox("Gender:", ["Male", "Female"])
            with c3:
                height = st.number_input("Height (cm):", min_value=100.0, max_value=220.0, value=170.0, step=1.0)
            with c4:
                weight = st.number_input("Weight (kg):", min_value=30.0, max_value=200.0, value=76.0, step=0.5)

            st.markdown("<hr style='margin: 1.5rem 0; border-color: #E2E8F0;'>", unsafe_allow_html=True)
            st.markdown("#### ❤️ Step 2: Health Profile")
            h1, h2, h3, h4 = st.columns(4)
            with h1:
                bp = st.number_input("Systolic Blood Pressure (mmHg):", min_value=70, max_value=220, value=135, step=1)
            with h2:
                glucose = st.number_input("Fasting Blood Glucose (mg/dL):", min_value=50.0, max_value=350.0, value=120.0, step=1.0)
            with h3:
                cholesterol = st.number_input("Serum Cholesterol (mg/dL):", min_value=100.0, max_value=400.0, value=205.0, step=1.0)
            with h4:
                disease = st.selectbox("Pre-existing Condition:", ["None", "Hypertension", "Diabetes", "Obesity"])

            h5, h6 = st.columns(2)
            with h5:
                severity = st.selectbox("Condition Severity:", ["None", "Mild", "Moderate", "Severe"])
            with h6:
                nutrient_imbalance = st.slider("Nutrient Imbalance Score (0 - 5):", min_value=0.0, max_value=5.0, value=2.4, step=0.1)

            st.markdown("<hr style='margin: 1.5rem 0; border-color: #E2E8F0;'>", unsafe_allow_html=True)
            st.markdown("#### 🏃 Step 3: Lifestyle & Activity")
            l1, l2, l3, l4 = st.columns(4)
            with l1:
                activity = st.selectbox("Physical Activity Level:", ["Sedentary", "Moderate", "Active"])
            with l2:
                calories = st.number_input("Daily Calorie Intake (kcal):", min_value=1000, max_value=5000, value=2400, step=50)
            with l3:
                exercise = st.number_input("Weekly Exercise (Hours):", min_value=0.0, max_value=30.0, value=4.5, step=0.5)
            with l4:
                adherence = st.slider("Past Diet Adherence Score (%):", min_value=0.0, max_value=100.0, value=75.0, step=1.0)

            st.markdown("<hr style='margin: 1.5rem 0; border-color: #E2E8F0;'>", unsafe_allow_html=True)
            st.markdown("#### 🍽️ Step 4: Food Preferences & Restrictions")
            f1, f2, f3 = st.columns(3)
            with f1:
                restrictions = st.selectbox("Dietary Restrictions:", ["None", "Low_Sodium", "Low_Sugar"])
            with f2:
                allergies = st.selectbox("Known Food Allergies:", ["None", "Peanuts", "Gluten"])
            with f3:
                cuisine = st.selectbox("Preferred Cuisine:", ["Mexican", "Indian", "Chinese", "Italian"])

            st.markdown("<br>", unsafe_allow_html=True)
            safety_agree = st.checkbox("I understand that this is an AI-generated general suggestion and not medical advice.", value=False)

            st.markdown("<br>", unsafe_allow_html=True)
            submit_form = st.form_submit_button("🥗 Get My Personalized Suggestion", type="primary", use_container_width=True)

        if submit_form:
            user_data = {
                'Age': age,
                'Gender': gender,
                'Height_cm': height,
                'Weight_kg': weight,
                'Blood_Pressure_mmHg': bp,
                'Glucose_mg/dL': glucose,
                'Cholesterol_mg/dL': cholesterol,
                'Disease_Type': disease,
                'Severity': severity,
                'Dietary_Nutrient_Imbalance_Score': nutrient_imbalance,
                'Physical_Activity_Level': activity,
                'Daily_Caloric_Intake': calories,
                'Weekly_Exercise_Hours': exercise,
                'Adherence_to_Diet_Plan': adherence,
                'Dietary_Restrictions': restrictions,
                'Allergies': allergies,
                'Preferred_Cuisine': cuisine,
                'safety_agree': safety_agree
            }

            # Validate Inputs
            is_valid, validation_errors = validate_user_input(user_data)
            if not is_valid:
                for err in validation_errors:
                    st.error(f"⚠️ {err}")
            else:
                try:
                    with st.spinner("Analyzing your profile through NutriGuide AI engine..."):
                        result = recommend_diet(user_data)
                        st.session_state['rec_result'] = result
                        st.session_state['last_user_data'] = user_data
                        st.rerun()
                except Exception as ex:
                    st.error(f"Unable to compute recommendation: {str(ex)}")

        render_privacy_notice()

# -----------------------------------------------------------------------------
# PAGE 3: ❓ HOW IT WORKS
# -----------------------------------------------------------------------------
elif page_choice == "❓ How It Works":
    st.markdown("### ❓ How NutriGuide AI Works")
    st.write("Understand the methodology, transparency, and trust principles behind NutriGuide AI.")

    st.markdown("""
    <div class="saas-card">
        <h4 style="color:#0F172A; margin-top:0;">🤖 Machine Learning Clustering Methodology</h4>
        <p style="color:#475569; font-size:0.95rem; line-height:1.6;">
            NutriGuide AI uses <strong>K-Means Unsupervised Clustering</strong> to analyze physiological parameters (Age, BMI, Blood Pressure, Fasting Glucose, Cholesterol) alongside lifestyle metrics (Daily Caloric Intake, Weekly Exercise).
            <br><br>
            Instead of manually setting rigid rules, the algorithm identifies hidden clinical clusters among 1,000 reference profiles. When you enter your health information, your profile is standardized and mapped to the nearest cluster centroid using Euclidean distance.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="saas-card">
        <h4 style="color:#0F172A; margin-top:0;">🛡️ Why Should I Trust This System?</h4>
        <ul style="color:#475569; font-size:0.95rem; line-height:1.8;">
            <li><strong>Data-Driven Consistency:</strong> Inputs are transformed using the exact same standardization scaler used during training.</li>
            <li><strong>Transparent Risk Profiling:</strong> Each cluster is associated with clear metabolic characteristics (e.g. elevated glucose, high systolic blood pressure, high BMI).</li>
            <li><strong>Non-Medical Boundaries:</strong> NutriGuide AI provides general nutritional suggestions and does not attempt to diagnose or treat medical conditions.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    render_disclaimer()

# -----------------------------------------------------------------------------
# PAGE 4: ℹ️ ABOUT
# -----------------------------------------------------------------------------
elif page_choice == "ℹ️ About":
    st.markdown("### ℹ️ About NutriGuide AI")

    st.markdown("""
    <div class="saas-card">
        <h3 style="color:#0F172A; margin-top:0;">NutriGuide AI Platform</h3>
        <p style="color:#475569; font-size:0.95rem; line-height:1.6;">
            NutriGuide AI is an educational AI-assisted nutrition platform designed to demonstrate how unsupervised machine learning can empower personalized dietary recommendations.
        </p>
        <hr style="border-color:#E2E8F0;">
        <h4 style="color:#0F172A;">🛠️ Product & Technology Architecture</h4>
        <p style="color:#475569; font-size:0.9rem; line-height:1.6;">
            - <strong>Frontend:</strong> Streamlit (Python)<br>
            - <strong>Machine Learning:</strong> Scikit-Learn (K-Means Clustering, StandardScaler, PCA)<br>
            - <strong>Data Engine:</strong> Pandas, NumPy<br>
            - <strong>Model Serialization:</strong> Joblib
        </p>
        <hr style="border-color:#E2E8F0;">
        <h4 style="color:#0F172A;">🔒 Privacy & Safety Guarantee</h4>
        <p style="color:#475569; font-size:0.9rem; line-height:1.6;">
            Your personal information is processed strictly in-memory during active sessions. No health records are saved to external databases or tracked across requests.
        </p>
    </div>
    """, unsafe_allow_html=True)

    render_disclaimer()

# -----------------------------------------------------------------------------
# PAGE 5: ⚙️ DEVELOPER / MODEL INSIGHTS
# -----------------------------------------------------------------------------
elif page_choice == "⚙️ Developer / Model Insights":
    st.markdown("### ⚙️ Developer & Model Insights")
    st.write("Technical analytics and machine learning model metrics (intended for developers and evaluators).")

    # Metrics Summary
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        st.metric("Total Dataset Records", df_raw.shape[0])
    with d2:
        st.metric("Total Attributes", df_raw.shape[1])
    with d3:
        st.metric("Trained K-Means Clusters", 3)
    with d4:
        st.metric("Model Silhouette Score", f"{eval_df.loc[eval_df['k']==3, 'silhouette_score'].values[0]:.4f}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📊 Evaluation Metrics Table")
    st.dataframe(eval_df, use_container_width=True)

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("#### 📈 Elbow Method & Silhouette Score Curve")
        fig, ax1 = plt.subplots(figsize=(6, 3.5))
        ax1.set_xlabel("Number of Clusters (K)")
        ax1.set_ylabel("Inertia (WCSS)", color="#0284C7")
        ax1.plot(eval_df["k"], eval_df["inertia"], marker="o", color="#0284C7", linewidth=2)
        
        ax2 = ax1.twinx()
        ax2.set_ylabel("Silhouette Score", color="#059669")
        ax2.plot(eval_df["k"], eval_df["silhouette_score"], marker="s", color="#059669", linestyle="--", linewidth=2)
        st.pyplot(fig)

    with col_m2:
        st.markdown("#### 🌌 2D PCA Cluster Scatter Plot")
        X = df_encoded[ALL_CLUSTERING_FEATURES]
        X_scaled = scaler.transform(X)
        labels = kmeans_model.predict(X_scaled)
        
        pca = PCA(n_components=2, random_state=42)
        pca_coords = pca.fit_transform(X_scaled)
        pca_df = pd.DataFrame(pca_coords, columns=['PCA1', 'PCA2'])
        pca_df['Cluster'] = [f"Cluster {l}" for l in labels]
        
        fig, ax = plt.subplots(figsize=(6, 3.5))
        sns.scatterplot(x='PCA1', y='PCA2', hue='Cluster', data=pca_df, palette=['#059669', '#0D9488', '#0284C7'], ax=ax, alpha=0.8, s=50)
        st.pyplot(fig)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📋 Cluster Mean Centroids Profile")
    st.dataframe(cluster_profiles, use_container_width=True)

# Render Global Footer
render_footer()
