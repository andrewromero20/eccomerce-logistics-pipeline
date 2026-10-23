import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import joblib
import os

#Page configuration
st.set_page_config(
    page_title="E-Commerce Logistics Analytics & AI",
    layout="wide"
)

#Data paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "olist.db")
MODEL_PATH = os.path.join(BASE_DIR, "data", "model_rf.joblib")

@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

model = load_model()

st.title("Logistics panel E-Commerce & Delays Risk Predictor")
st.markdown("Real-time delivery metric visualization and risk simulation using machine learning.")

st.sidebar.header("Predictor configuration")

tab1, tab2 = st.tabs(["KPIs & Operational analysis", "Risk Simulator"])

with tab1:
    st.header("Global Delivery metrics")
    
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        df_kpi = pd.read_sql_query("""
            SELECT 
                COUNT(*) as total_orders,
                AVG(CASE WHEN order_delivered_customer_date > order_estimated_delivery_date THEN 1 ELSE 0 END) * 100 as pct_delayed
            FROM orders 
            WHERE order_status = 'delivered'
        """, conn)
        conn.close()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Orders Processed", f"{int(df_kpi['total_orders'].iloc[0]):,}")
        col2.metric("Global Delay Rate", f"{df_kpi['pct_delayed'].iloc[0]:.2f}%")
        col3.metric("Service Level (On-Time)", f"{100 - df_kpi['pct_delayed'].iloc[0]:.2f}%")
    else:
        st.error("Database `olist.db` not found.")

with tab2:
    st.header("Risk Simulator for New Orders")
    st.markdown("Enter the order characteristics to calculate the probability of delay:")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        price = st.number_input("Product Price ($ BRL)", min_value=1.0, value=100.0, step=10.0)
        freight_value = st.number_input("Freight Cost ($ BRL)", min_value=1.0, value=20.0, step=2.0)
        estimated_days = st.slider("Estimated Days Promised", min_value=1, max_value=60, value=15)
        is_same_state = st.selectbox("Are the customer and seller in the same state?", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No")
        
    with col_b:
        weight_g = st.number_input("Product weight (grams)", min_value=10.0, value=1000.0, step=100.0)
        length_cm = st.number_input("Length (cm)", min_value=1.0, value=20.0, step=1.0)
        height_cm = st.number_input("Height (cm)", min_value=1.0, value=10.0, step=1.0)
        width_cm = st.number_input("Width (cm)", min_value=1.0, value=15.0, step=1.0)
        purchase_hour = st.slider("Purchase Hour (0-23 hrs)", min_value=0, max_value=23, value=14)
        purchase_dayofweek = st.selectbox("Day of the Week", list(range(7)), format_func=lambda x: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][x])


    freight_ratio = freight_value / (price + freight_value)
    product_volume_cm3 = length_cm * height_cm * width_cm
    
    if st.button("Evaluate Delivery Risk", type="primary"):
        if model is not None:
            # Build input vector with the same columns as training data
            input_data = pd.DataFrame([{
                'price': price,
                'freight_value': freight_value,
                'freight_ratio': freight_ratio,
                'is_same_state': is_same_state,
                'estimated_days_promised': estimated_days,
                'product_weight_g': weight_g,
                'product_volume_cm3': product_volume_cm3,
                'purchase_dayofweek': purchase_dayofweek,
                'purchase_hour': purchase_hour
            }])
            
            prob_delay = model.predict_proba(input_data)[0][1] * 100
            
            st.divider()
            st.subheader("Prediction Result")
            
            if prob_delay >= 50.0:
                st.error(f"**HIGH DELAY RISK:** Probability of **{prob_delay:.1f}%**")
                st.warning("Recommendation: Assign priority logistics or adjust the estimated delivery date.")
            else:
                st.success(f"**LOW DELAY RISK:** Probability of **{prob_delay:.1f}%**")
                st.info("The order is within the normal parameters for on-time delivery.")
        else:
            st.error("No binary model file found: `model_rf.joblib`.")