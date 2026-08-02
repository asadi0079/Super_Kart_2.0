
import streamlit as st
import pandas as pd
import joblib
import numpy as np


BACKEND_URL = "hhtp://backend:7860"

# Streamlit UI for Price Prediction
st.title("SuperKart Rev Predictor")
# Section for online prediction
st.subheader("SuperCart Online Predictor")

st.write("This tool predicts the rev per store per product.")


# Load the trained model
@st.cache_resource
def load_model():
    return joblib.load("SuperKart_Rev_prediction_model_v1_0.joblib")

model = load_model()



st.subheader("Enter the store details:")

# Collect user input
StoreID = st.selectbox("Store_ID", ["OUT001", "OUT002", "OUT003", "OUT004"])
StoreSize = st.selectbox("Store Size", ["Small", "Medium", "High"])
StoreLocationCityType = st.selectbox("City Type", ["Tier 1", "Tier 2", "Tier 3"])
StoreType = st.selectbox("Store Type", ["Departmental", "Supermarket Type 1", "Supermarket Type 2"])
StoreYear = st.number_input("Store est year")
ProductID = st.text_input("Product_ID")
ProductType = st.selectbox("Product Type", ["Fruits and Vegetables", "Snack Foods", "Frozen Foods", "Dairy", "Household", "Baking Goods", "Canned", "Health and Hygiene", "Meat", "Soft Drinks", "Bread", "Hard Drinks", "Others", "Starchy Foods","Breakfast","Seafood" ])
Product_Sugar_Content = st.selectbox("Product Sugar Content if applicable", ["Low Sugar", "Regular", "No Sugar"])

ProductWeight = st.number_input("Product Weight")
ProductAllocatedArea = st.number_input("Product Allocated Area")
ProductMRP = st.number_input("Product Price")


# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Store_Id': StoreID,
    'Store_Size': StoreSize,
    'Store_Location_City_Type': StoreLocationCityType,
    'Store_Type': StoreType,
    'Store_Establishment_Year': StoreYear,
    'Product_Id': ProductID,
    'Product_Type': ProductType,
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_Weight': ProductWeight,
    'Product_Allocated_Area': ProductAllocatedArea,
    'Product_MRP': ProductMRP,

}])

# Make a single prediction when the Predict button is clicked
if st.button("Predict", type = "primary"):
    response = requests.post(f"{BACKEND_URL}/v1/revnue", json=input_data.to_dict(orient="records")[0]) # send data HTTP request to Flask API as a POST method and hit the revenue endpoint to get prediction along with a JSON that contains the user data collected for the model to use
    if respnse.status_code == 200:
        prediction = response.json()["Predicted Product Revenue (in dollars)"]
        st.write(f"The predicted revenue for the product at the store is ${prediction:.2f}.")
    else
        st.write("Unable to connect to prediction API")

st.subheader("Batch Prediction")

uploaded_file = st.file_uploader("Upload a CSV file for batch prediction", type=["csv"])

if uploaded_file is not None:
    if st.button("Predict", type = "primary"):
        response = requests.post(f"{BACKEND_URL}/v1/revenuebatch", files={"file": uploaded_file}) # send batch file to Flask API as a HTTP post request
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions is complete")
            st.write(Predictions)
        else:
            st.write("Unable to connect to prediction API")
