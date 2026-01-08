import streamlit as st
import pickle
import numpy as np
import pandas as pd

# 1. Load the Model
# Ensure this file is in the same folder!
model = pickle.load(open('house_price_model.pkl', 'rb'))

# 2. Page Configuration
st.set_page_config(
    page_title="Boston Real Estate AI Predictor",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Session State for Reset Functionality ---
defaults = {
    'RM': 6.0, 'LSTAT': 10.0, 'PTRATIO': 15.0, 'CRIM': 0.1,
    'ZN': 10.0, 'INDUS': 5.0, 'CHAS': 0, 'NOX': 0.5,
    'AGE': 50, 'DIS': 4.0, 'RAD': 5, 'TAX': 300, 'B': 390.0
}

# Initialize session state
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

def reset_values():
    for key, value in defaults.items():
        st.session_state[key] = value

# --- Custom CSS for Enhanced UI ---
st.markdown("""
    <style>
    /* Main Background gradient */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    /* Card-like container for main content */
    .main-card {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #f0f2f6;
        border-right: 1px solid #dce1e6;
    }
    /* Primary Button Styling (Predict) */
    .stButton>button[data-testid="baseButton-primary"] {
        width: 100%;
        background: linear-gradient(to right, #FF512F, #DD2476);
        color: white;
        border: none;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    /* Secondary Button Styling (Reset) */
    .stButton>button[data-testid="baseButton-secondary"] {
        width: 100%;
        border: 2px solid #555;
        color: #555;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar (Controls) ---
st.sidebar.title("⚙️ Control Panel")

# FIXED: Changed 'kind' to 'type'
st.sidebar.button("🔄 Reset All Inputs", on_click=reset_values, type="secondary", help="Reset all features to their default values.")

st.sidebar.markdown("---")
st.sidebar.write("Adjust features below:")

def user_input_features():
    # Group 1: Key Drivers
    with st.sidebar.expander("🔑 Key Features (High Impact)", expanded=True):
        RM = st.slider("Number of Rooms (RM)", 1.0, 9.0, key='RM')
        LSTAT = st.slider("Lower Status Population % (LSTAT)", 0.0, 40.0, key='LSTAT')
        PTRATIO = st.slider("Pupil-Teacher Ratio", 12.0, 22.0, key='PTRATIO')
        CRIM = st.number_input("Crime Rate (Per Capita)", 0.0, 90.0, step=0.1, key='CRIM')

    # Group 2: Advanced
    with st.sidebar.expander("📐 Technical Specs & Others"):
        ZN = st.number_input("Residential Land Zone (ZN)", step=1.0, key='ZN')
        INDUS = st.number_input("Industrial Business Acres", step=1.0, key='INDUS')
        CHAS = st.selectbox("By Charles River? (CHAS)", (0, 1), format_func=lambda x: "Yes" if x == 1 else "No", key='CHAS')
        NOX = st.number_input("Nitric Oxides Concentration", 0.3, 0.9, step=0.01, key='NOX')
        AGE = st.slider("Age of House (Years)", 0, 100, key='AGE')
        DIS = st.number_input("Dist. to Employment Centers", 1.0, 12.0, step=0.1, key='DIS')
        RAD = st.slider("Highway Access Index (1-24)", 1, 24, key='RAD')
        TAX = st.number_input("Property Tax Rate", 180, 720, step=10, key='TAX')
        B = st.number_input("Black Proportion", 0.0, 400.0, step=10.0, key='B')
    
    data = {
        'CRIM': CRIM, 'ZN': ZN, 'INDUS': INDUS, 'CHAS': CHAS, 'NOX': NOX,
        'RM': RM, 'AGE': AGE, 'DIS': DIS, 'RAD': RAD, 'TAX': TAX,
        'PTRATIO': PTRATIO, 'B': B, 'LSTAT': LSTAT
    }
    return pd.DataFrame(data, index=[0])

input_df = user_input_features()

# --- Main Page ---
st.title("🏡 Boston Real Estate AI Predictor")
st.markdown("Welcome! Configure a house in the sidebar and get an instant market value estimation powered by **XGBoost**.")

# Use a container to apply the 'card' background
with st.container():
    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("📋 Selected Property Specs")
        st.dataframe(input_df.style.format("{:.2f}"))
        st.markdown("<br>", unsafe_allow_html=True)

        # FIXED: Changed 'kind' to 'type'
        if st.button("🚀 Predict Price Now", type="primary"):
            with st.spinner("Calculating..."):
                prediction = model.predict(input_df)
                price = prediction[0] * 1000
            
            st.success("🎉 Prediction Successful!")
            st.metric(label="Estimated Market Value", value=f"${price:,.2f}", delta="AI Estimate")
            
            st.subheader("Price Tier")
            if price < 25000:
                st.warning("📉 Budget / Affordable Range")
                st.progress(30)
            elif price < 45000:
                st.info("📊 Mid-Range Market")
                st.progress(60)
            else:
                st.success("💎 Luxury / High-End")
                st.progress(90)

    with col2:
        st.info("💡 **How It Works**")
        st.markdown("""
        This application uses a machine learning model trained on historical housing data.
        
        **Key factors influencing the price:**
        * **Rooms (RM):** The most significant positive factor. More rooms generally equal higher value.
        * **Neighborhood Status (LSTAT):** A strong negative indicator.
        * **Location & Services:** Crime rate, school quality (PTRATIO), and distance to employment centers all play a role.
        """)
        
    st.markdown('</div>', unsafe_allow_html=True) # End of main-card div

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>Built with ❤️ by Rishav Kumar Shrivastava.</div>", unsafe_allow_html=True)
