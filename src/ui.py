import streamlit as st
import os

def inject_custom_css():
    """
    Inject modern consumer-facing health-tech SaaS styling.
    """
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #F8FAFC;
            color: #0F172A;
        }

        .stApp {
            background-color: #F8FAFC;
        }

        /* Container padding */
        .block-container {
            padding-top: 1.75rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }

        /* Header Hero */
        .hero-banner {
            background: linear-gradient(135deg, #059669 0%, #0D9488 60%, #0284C7 100%);
            border-radius: 20px;
            padding: 2.5rem 2.5rem;
            color: #FFFFFF;
            box-shadow: 0 10px 25px -5px rgba(5, 150, 105, 0.2);
            margin-bottom: 2rem;
            position: relative;
        }

        .hero-brand {
            font-size: 0.875rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            background: rgba(255, 255, 255, 0.2);
            color: #FFFFFF;
            padding: 0.3rem 0.85rem;
            border-radius: 9999px;
            display: inline-block;
            margin-bottom: 0.75rem;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        .hero-title {
            font-size: 2.5rem;
            font-weight: 800;
            line-height: 1.15;
            color: #FFFFFF;
            margin: 0 0 0.5rem 0;
            letter-spacing: -0.02em;
        }

        .hero-subtitle {
            font-size: 1.1rem;
            font-weight: 400;
            color: #F0FDFA;
            margin: 0;
            max-width: 720px;
            line-height: 1.5;
        }

        /* SaaS Cards */
        .saas-card {
            background: #FFFFFF;
            border-radius: 16px;
            padding: 1.75rem;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03);
            margin-bottom: 1.25rem;
            height: 100%;
        }

        .benefit-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 0.5rem;
        }

        .benefit-desc {
            font-size: 0.925rem;
            color: #64748B;
            line-height: 1.5;
            margin: 0;
        }

        /* Step Card */
        .step-box {
            background: #FFFFFF;
            border-radius: 16px;
            padding: 1.5rem;
            border: 1px solid #E2E8F0;
            border-top: 4px solid #059669;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
            height: 100%;
        }

        .step-badge {
            color: #059669;
            font-weight: 800;
            font-size: 0.85rem;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }

        .step-heading {
            font-size: 1.1rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 0.4rem;
        }

        /* Step Form Progress Bar */
        .step-wizard-bar {
            display: flex;
            justify-content: space-between;
            margin-bottom: 2rem;
            background: #FFFFFF;
            padding: 1rem 1.5rem;
            border-radius: 14px;
            border: 1px solid #E2E8F0;
        }

        .step-wizard-item {
            flex: 1;
            text-align: center;
            font-size: 0.875rem;
            font-weight: 600;
            color: #94A3B8;
            padding: 0.5rem;
            border-bottom: 3px solid #E2E8F0;
        }

        .step-wizard-item.active {
            color: #059669;
            border-bottom: 3px solid #059669;
            font-weight: 700;
        }

        /* Form Controls & Buttons */
        .stButton button {
            border-radius: 12px !important;
            font-weight: 700 !important;
            padding: 0.75rem 1.5rem !important;
            min-height: 48px !important;
            font-size: 1rem !important;
            transition: all 0.2s ease !important;
        }

        .stButton button[kind="primary"] {
            background: linear-gradient(135deg, #059669 0%, #0D9488 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            box-shadow: 0 4px 14px rgba(5, 150, 105, 0.3) !important;
        }

        .stButton button[kind="primary"]:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(5, 150, 105, 0.4) !important;
        }

        /* Result Container */
        .result-card {
            background: linear-gradient(135deg, #ECFDF5 0%, #F0FDFA 100%);
            border: 2px solid #10B981;
            border-radius: 20px;
            padding: 2.25rem;
            box-shadow: 0 10px 30px rgba(16, 185, 129, 0.15);
            margin-top: 1.5rem;
            margin-bottom: 2rem;
        }

        .result-diet-badge {
            background-color: #059669;
            color: #FFFFFF;
            padding: 0.6rem 1.4rem;
            border-radius: 9999px;
            font-weight: 800;
            font-size: 1.35rem;
            display: inline-block;
            box-shadow: 0 4px 12px rgba(5, 150, 105, 0.25);
        }

        /* Safety & Privacy Notices */
        .safety-notice-box {
            background-color: #FFFBEB;
            border-left: 4px solid #F59E0B;
            color: #78350F;
            padding: 1.25rem 1.5rem;
            border-radius: 12px;
            font-size: 0.925rem;
            line-height: 1.6;
            margin-top: 2rem;
            margin-bottom: 1.5rem;
        }

        .privacy-notice-box {
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            color: #64748B;
            padding: 0.85rem 1.25rem;
            border-radius: 10px;
            font-size: 0.85rem;
            margin-top: 1rem;
        }

        /* Clean Footer */
        .footer-container {
            text-align: center;
            color: #94A3B8;
            font-size: 0.875rem;
            margin-top: 3.5rem;
            padding-top: 1.75rem;
            border-top: 1px solid #E2E8F0;
            font-weight: 500;
        }
    </style>
    """, unsafe_allow_html=True)

def render_hero(logo_path=None, on_primary_click=None, **kwargs):
    """
    Render main product hero section with official NutriGuide AI logo.
    Supports flexible signature (logo_path, on_primary_click, **kwargs) to prevent TypeErrors.
    """
    if logo_path is None:
        logo_path = kwargs.get('logo_path')
        
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if logo_path is None or not os.path.exists(logo_path):
        default_logo = os.path.join(base_dir, 'assets', 'nutriguide_logo.png')
        if os.path.exists(default_logo):
            logo_path = default_logo

    if logo_path and os.path.exists(logo_path):
        col_logo, col_text = st.columns([1, 4])
        with col_logo:
            st.image(logo_path, width=120)
        with col_text:
            st.markdown("""
            <div class="hero-banner" style="margin-bottom:0;">
                <span class="hero-brand">NutriGuide AI</span>
                <h1 class="hero-title">Personalized Nutrition, Powered by AI</h1>
                <p class="hero-subtitle">Get diet suggestions tailored to your health profile, lifestyle, dietary restrictions and food preferences.</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="hero-banner">
            <span class="hero-brand">NutriGuide AI</span>
            <h1 class="hero-title">Personalized Nutrition, Powered by AI</h1>
            <p class="hero-subtitle">Get diet suggestions tailored to your health profile, lifestyle, dietary restrictions and food preferences.</p>
        </div>
        """, unsafe_allow_html=True)

def render_benefit_cards():
    """
    Render 3 product benefit cards.
    """
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="saas-card">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🧬</div>
            <div class="benefit-title">Personalized</div>
            <p class="benefit-desc">Recommendations tailored specifically to your individual health indicators, BMI, and physical activity.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="saas-card">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
            <div class="benefit-title">Data-Driven</div>
            <p class="benefit-desc">Uses machine learning to identify similar health and lifestyle patterns across comprehensive data.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="saas-card">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">✨</div>
            <div class="benefit-title">Simple & Clear</div>
            <p class="benefit-desc">Easy-to-understand nutrition suggestions, macronutrient breakdowns, and actionable food guides.</p>
        </div>
        """, unsafe_allow_html=True)

def render_how_it_works():
    """
    Render 3-step 'How It Works' section.
    """
    st.markdown("### 🔄 How NutriGuide AI Works")
    st.markdown("<br>", unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown("""
        <div class="step-box">
            <div class="step-badge">01</div>
            <div class="step-heading">Tell Us About You</div>
            <p class="benefit-desc">Enter your basic demographics, health metrics, activity habits, and dietary preferences.</p>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown("""
        <div class="step-box">
            <div class="step-badge">02</div>
            <div class="step-heading">AI Analyzes Your Profile</div>
            <p class="benefit-desc">Our machine learning model compares your inputs with clinical cluster patterns in real-time.</p>
        </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown("""
        <div class="step-box">
            <div class="step-badge">03</div>
            <div class="step-heading">Get Your Suggestion</div>
            <p class="benefit-desc">Receive a personalized diet category, food recommendations, and health risk insights.</p>
        </div>
        """, unsafe_allow_html=True)

def render_disclaimer():
    """
    Render Health & Safety Notice.
    """
    st.markdown("""
    <div class="safety-notice-box">
        <strong>⚠️ Health & Safety Notice:</strong><br>
        NutriGuide AI provides general nutrition suggestions for educational and informational purposes. It does not diagnose or treat medical conditions and is not a substitute for advice from a qualified doctor or registered dietitian. If you have a medical condition, take medication, or have specific nutritional needs, consult a healthcare professional before making significant dietary changes.
    </div>
    """, unsafe_allow_html=True)

def render_privacy_notice():
    """
    Render Privacy Guarantee Notice.
    """
    st.markdown("""
    <div class="privacy-notice-box">
        🔒 <strong>Your Privacy Choice:</strong> Your health inputs are processed in-memory solely to generate your current recommendation and are not permanently stored by this application.
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    """
    Render clean product footer.
    """
    st.markdown("""
    <div class="footer-container">
        NutriGuide AI • Personalized Nutrition Guidance • Educational AI Platform
    </div>
    """, unsafe_allow_html=True)
