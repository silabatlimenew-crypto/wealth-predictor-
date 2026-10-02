%%writefile app.py
import streamlit as st
import pandas as pd
import joblib

# Load trained model and model columns
model = joblib.load('model.pkl')
model_columns = joblib.load('model_columns.pkl')

st.title("Household Wealth Index Predictor")
st.write("Select household characteristics to predict wealth category.")

# 1. Drinking Water Source Options
water_options = {
    "Piped to yard/plot": "hv201_piped to yard/plot",
    "Piped to neighbor": "hv201_piped to neighbor",
    "Public tap/standpipe": "hv201_public tap/standpipe",
    "Tube well or borehole": "hv201_tube well or borehole",
    "Protected well": "hv201_protected well",
    "Unprotected well": "hv201_unprotected well",
    "Protected spring": "hv201_protected spring",
    "Unprotected spring": "hv201_unprotected spring",
    "River/Dam/Lake/Ponds/Stream/Canal": "hv201_river/dam/lake/ponds/stream/canal/irrigation channel",
    "Rainwater": "hv201_rainwater",
    "Bottled water": "hv201_bottled water",
    "Large bottle": "hv201_large bottle",
    "Other": "hv201_other"
}

# 2. Toilet Type Options
toilet_options = {
    "Flush to pit latrine": "hv205_flush to pit latrine",
    "Flush to somewhere else": "hv205_flush to somewhere else",
    "Flush, don't know where": "hv205_flush, don't know where",
    "Ventilated improved pit latrine (VIP)": "hv205_ventilated improved pit latrine (vip)",
    "Pit latrine with slab": "hv205_pit latrine with slab",
    "Pit latrine without slab/open pit": "hv205_pit latrine without slab/open pit",
    "No facility/bush/field": "hv205_no facility/bush/field",
    "Composting toilet": "hv205_composting toilet",
    "Hanging toilet/latrine": "hv205_hanging toilet/latrine",
    "Other": "hv205_other"
}

# Streamlit Selectboxes (UI inputs)
water_choice = st.selectbox("Drinking Water Source (hv201)", list(water_options.keys()))
toilet_choice = st.selectbox("Toilet Type (hv205)", list(toilet_options.keys()))

has_electricity = st.selectbox("Electricity Available (hv206)", ["No", "Yes"])
has_radio = st.selectbox("Radio Available (hv207)", ["No", "Yes"])
has_tv = st.selectbox("Television Available (hv208)", ["No", "Yes"])
residence = st.selectbox("Place of Residence (hv025)", ["Urban", "Rural"])

if st.button("Predict"):
    # Initialize all model columns to 0
    input_data = {col: 0 for col in model_columns}
    
    # Set selected categorical values to 1
    selected_water_col = water_options[water_choice]
    if selected_water_col in input_data:
        input_data[selected_water_col] = 1
        
    selected_toilet_col = toilet_options[toilet_choice]
    if selected_toilet_col in input_data:
        input_data[selected_toilet_col] = 1
        
    # Binary / Residence features
    if has_electricity == "Yes" and 'hv206_yes' in input_data:
        input_data['hv206_yes'] = 1
    if has_radio == "Yes" and 'hv207_yes' in input_data:
        input_data['hv207_yes'] = 1
    if has_tv == "Yes" and 'hv208_yes' in input_data:
        input_data['hv208_yes'] = 1
    if residence == "Rural" and 'hv025_rural' in input_data:
        input_data['hv025_rural'] = 1

    # Convert to DataFrame with correct column order
    df = pd.DataFrame([input_data])[model_columns]
    
    # Make Prediction
    prediction = model.predict(df)[0]
    
    st.success(f"Predicted Household Wealth Index: **{prediction}**")
