import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Config
st.set_page_config(page_title="House Price Predictor", layout="wide")

# 2. Custom CSS for "Attractive" UI
st.markdown("""
<style>
    /* Card Styling for Results */
    .result-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 8px solid #4CAF50; /* Green accent */
        transition: transform 0.2s;
    }
    .result-card:hover {
        transform: scale(1.02);
    }
    .price-tag {
        font-size: 24px;
        font-weight: bold;
        color: #2E7D32;
    }
    .feature-tag {
        background-color: #f1f3f4;
        border-radius: 15px;
        padding: 4px 10px;
        font-size: 12px;
        margin-right: 5px;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# 3. Initialize Session State for History
if 'history' not in st.session_state:
    st.session_state.history = []

# --- MAIN LAYOUT ---
st.title("🏡 Real Estate Value Estimator")
st.markdown("Predict Boston House Prices based on key features.")
st.markdown("---")

left_col, right_col = st.columns([1, 2.5], gap="large")

# ==========================================
# LEFT COLUMN: INPUTS (SCROLLABLE)
# ==========================================
with left_col:
    st.subheader("⚙️ Configure Features")
    
    # !!! SCROLLER IS HERE !!!
    with st.container(height=650, border=True):
        st.info("Adjust the parameters below to predict price.")
        
        # Simulating standard Boston Housing Dataset features
        crim = st.number_input("CRIM (Per capita crime rate)", value=0.006, format="%.4f")
        zn = st.slider("ZN (Res. land zoned > 25k sq.ft)", 0, 100, 18)
        indus = st.number_input("INDUS (Non-retail business acres)", value=2.31)
        chas = st.selectbox("CHAS (Charles River dummy)", [0, 1], help="1 if tract bounds river; 0 otherwise")
        nox = st.slider("NOX (Nitric oxides conc.)", 0.3, 0.9, 0.53, step=0.01)
        
        st.markdown("---")
        rm = st.slider("RM (Avg rooms per dwelling)", 3.0, 9.0, 6.5, step=0.1)
        age = st.slider("AGE (Units built prior to 1940)", 0.0, 100.0, 65.2)
        dis = st.number_input("DIS (Distance to employment centres)", value=4.09)
        
        st.markdown("---")
        rad = st.slider("RAD (Index of highway accessibility)", 1, 24, 1)
        tax = st.number_input("TAX (Property-tax rate per $10k)", value=296.0)
        ptratio = st.slider("PTRATIO (Pupil-teacher ratio)", 12.0, 22.0, 15.3)
        lstat = st.slider("LSTAT (% Lower status of population)", 1.0, 40.0, 4.98)

        st.write("") # Spacer
        
        # PREDICT BUTTON
        if st.button("🚀 Predict Price", use_container_width=True, type="primary"):
            # --- SIMULATION LOGIC (Replace with model.predict() later) ---
            # Simple dummy formula for demonstration
            # Price increases with Rooms, decreases with Crime and LSTAT
            base_price = 22.0
            pred_price = base_price + (rm * 3.5) - (lstat * 0.5) - (crim * 0.2) + (chas * 2)
            pred_price = max(5.0, pred_price) # Ensure no negative prices
            
            # Save to history
            new_record = {
                "id": len(st.session_state.history) + 1,
                "Rooms": rm,
                "LSTAT": lstat,
                "Crime": crim,
                "Price": pred_price,
                "River View": "Yes" if chas == 1 else "No"
            }
            # Insert at top of list
            st.session_state.history.insert(0, new_record)
            st.success("Prediction Generated!")

# ==========================================
# RIGHT COLUMN: RESULTS (NO SCROLLER)
# ==========================================
with right_col:
    st.subheader("📊 Prediction Results")

    # Metrics Row
    if st.session_state.history:
        df_hist = pd.DataFrame(st.session_state.history)
        avg_price = df_hist['Price'].mean()
        highest_price = df_hist['Price'].max()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Predictions Made", len(df_hist))
        m2.metric("Avg Predicted Price", f"${avg_price:,.2f}k")
        m3.metric("Highest Estimate", f"${highest_price:,.2f}k")
    else:
        st.info("👈 Use the panel on the left to generate your first prediction.")

    st.markdown("---")

    # Display Cards (Grid System)
    if st.session_state.history:
        grid_cols = st.columns(2)
        
        for i, record in enumerate(st.session_state.history):
            with grid_cols[i % 2]:
                
                # Dynamic Border Color based on Price
                border_color = "#4CAF50" # Green
                if record['Price'] > 40: border_color = "#FFD700" # Gold for luxury
                if record['Price'] < 15: border_color = "#FF5722" # Orange/Red for cheap
                
                st.markdown(f"""
                <div class="result-card" style="border-left: 8px solid {border_color};">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:14px; color:#888;">ID: #{record['id']}</span>
                        <span class="price-tag">${record['Price']:,.2f}k</span>
                    </div>
                    <hr style="margin: 10px 0;">
                    <div style="margin-bottom:8px;">
                        <span class="feature-tag">🛏️ {record['Rooms']} Rooms</span>
                        <span class="feature-tag">📉 {record['LSTAT']}% LSTAT</span>
                    </div>
                    <div>
                        <span class="feature-tag">🚓 {record['Crime']:.4f} CRIM</span>
                        <span class="feature-tag">🌊 River: {record['River View']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Clear Button
                if st.button(f"Delete #{record['id']}", key=f"del_{record['id']}"):
                    st.session_state.history.pop(i)
                    st.rerun()
