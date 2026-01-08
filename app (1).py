import streamlit as st
import pandas as pd
import xgboost
import pickle

# 1. Load the Model
model = pickle.load(open('house_price_model.pkl', 'rb'))

# 2. Page Configuration (Title and Layout)
st.set_page_config(page_title="Boston House Price Predictor", page_icon="🏡", layout="wide")

st.title("🏡 Boston Real Estate AI Predictor")
st.write("Welcome! Configure a house in the sidebar and get an instant market value estimation powered by XGBoost.")

# 3. Sidebar Inputs (Collecting Data)
st.sidebar.header("⚙️ Configure Property")

def user_input_features():
    # These are the standard features for the Boston Housing Dataset
    CRIM = st.sidebar.number_input("Crime Rate (CRIM)", value=0.1)
    ZN = st.sidebar.number_input("Residential Land Zone (ZN)", value=10.0)
    INDUS = st.sidebar.number_input("Non-Retail Business Acres (INDUS)", value=5.0)
    CHAS = st.sidebar.selectbox("Charles River Bound (CHAS)", (0, 1))
    NOX = st.sidebar.number_input("Nitric Oxide Concentration (NOX)", value=0.5)
    RM = st.sidebar.number_input("Average Rooms per Dwelling (RM)", value=6.0)
    AGE = st.sidebar.number_input("Proportion of Owner-Occupied Units Built Prior to 1940 (AGE)", value=50.0)
    DIS = st.sidebar.number_input("Weighted Distances to Employment Centres (DIS)", value=4.0)
    RAD = st.sidebar.number_input("Index of Accessibility to Radial Highways (RAD)", value=5.0)
    TAX = st.sidebar.number_input("Property-Tax Rate (TAX)", value=300.0)
    PTRATIO = st.sidebar.number_input("Pupil-Teacher Ratio (PTRATIO)", value=15.0)
    B = st.sidebar.number_input("Proportion of Blacks (B)", value=390.0)
    LSTAT = st.sidebar.number_input("Lower Status of Population % (LSTAT)", value=5.0)

    data = {
        'CRIM': CRIM, 'ZN': ZN, 'INDUS': INDUS, 'CHAS': CHAS, 'NOX': NOX,
        'RM': RM, 'AGE': AGE, 'DIS': DIS, 'RAD': RAD, 'TAX': TAX,
        'PTRATIO': PTRATIO, 'B': B, 'LSTAT': LSTAT
    }
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

# 4. Main Page - Displaying Selected Specs (The Fix)
st.subheader("📋 Selected Property Specs")

# CHANGE 1: use_container_width=True forces the table to fit the screen width
# hide_index=True removes the ugly '0' column at the start
st.dataframe(input_df, use_container_width=True, hide_index=True)

# 5. Prediction Logic
if st.button("🚀 Predict Price Now", type="primary"):
    prediction = model.predict(input_df)
    st.success(f"💰 Estimated Price: ${prediction[0] * 1000:,.2f}")

# 6. "How It Works" Section (Moved Below)
st.markdown("---") # Adds a divider line
st.subheader("💡 How It Works")

# CHANGE 2: Simple layout (no columns) so it sits at the bottom
st.info("This application uses a machine learning model trained on historical housing data.")

st.markdown("""
**Key factors influencing the price:**
* **Rooms (RM):** The most significant positive factor. More rooms generally equal higher value.
* **Neighborhood Status (LSTAT):** A strong indicator; lower status areas tend to have lower prices.
* **Crime Rate (CRIM):** Higher crime rates negatively impact property value.
""")
