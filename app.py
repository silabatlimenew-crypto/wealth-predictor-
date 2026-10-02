import streamlit as st
import joblib
import pandas as pd

# Load model and columns
model = joblib.load('model.pkl')
model_columns = joblib.load('model_columns.pkl')

st.title("Household Wealth Index Predictor")
st.write("Enter household characteristics to predict wealth category.")

drinking_water = st.text_input("Drinking Water Source (hv201)")
toilet_type = st.text_input("Toilet Type (hv205)")
electricity = st.text_input("Electricity Available (hv206)")
radio = st.text_input("Radio Available (hv207)")
television = st.text_input("Television Available (hv208)")
urban_rural = st.text_input("Place of Residence (hv025)")

if st.button("Predict"):
    input_data = pd.DataFrame([{
        'hv201': drinking_water,
        'hv205': toilet_type,
        'hv206': electricity,
        'hv207': radio,
        'hv208': television,
        'hv025': urban_rural
    }])
    
    input_encoded = pd.get_dummies(input_data)
    input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)
    
    prediction = model.predict(input_encoded)[0]
    st.success(f"Predicted Household Wealth Index: {prediction}")
