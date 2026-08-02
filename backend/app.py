# Flask allows you to create API server for your model

# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application, initiating the API server
product_revenue_predictor_api = Flask("Product Revenue Predictor")

# Load the trained machine learning model into the API server
model = joblib.load("SuperKart_Rev_prediction_model_v1_0.joblib")

# Define a route for the home page (GET request) of the API server hosting the model
@product_revenue_predictor_api.get('/') # endpoint 1
def home(): # function 1
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Product Revenue Prediction API!"

# Define an endpoint for single property prediction (POST request)
@product_revenue_predictor_api.post('/v1/revnue')# endpoint 2
def predict_product_revenue(): # function 2
    """
    This function handles POST requests to the '/v1/revenue' endpoint.
    It expects a JSON payload containing property details and returns
    the predicted product revenue as a JSON response.
    """
    # Get the JSON data from the request body, the endpoint expects a JSON coming from the UI in this case. JSON contains the data about prediction
    property_data = request.get_json()

    # Extract all relevant features from the JSON data about the request coming from the UI with the input values
    sample = {
        'Store_Id': property_data['StoreID'],
        'Store_Size': property_data['StoreSize'],
        'Store_Location_City_Type': property_data['StoreLocationCityType'],
        'Store_Type': property_data['StoreType'],
        'Store_Establishment_Year': property_data['StoreYear'],
        'Product_Id': property_data['ProductID'],
        'Product_Type': property_data['Product_Type'],
        'Product_Sugar_Content': property_data['Product_Sugar_Content'],
        'Product_Weight': property_data['ProductWeight'],
        'Product_Allocated_Area': property_data['ProductAllocatedArea'],
        'Product_MRP': property_data['ProductMRP'],
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction (get product revenue)
    predicted_product_revenue = model.predict(input_data)[0]

    # Calculate actual price
    #predicted_price = np.exp(predicted_log_price)

    # Convert predicted_price to Python float
    predicted_product_revenue = round(float(predicted_price), 2)
    # The conversion above is needed as we convert the model prediction (log price) to actual price using np.exp, which returns predictions as NumPy float32 values.
    # When we send this value directly within a JSON response, Flask's jsonify function encounters a datatype error

    # Return the actual price
    return jsonify({'Predicted Product Revenue (in dollars)':  predicted_product_revenue})


# Define an endpoint for batch prediction (POST request)
@product_revenue_predictor_api.post('/v1/revenuebatch') # endpoint 3
def product_revuenue__batch(): # function 3
    """
    This function handles POST requests to the '/v1/revenuebatch' endpoint.
    It expects a CSV file containing property details for multiple properties
    and returns the predicted rental prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all properties in the DataFrame (get log_prices)
    predicted_product_revenue = model.predict(input_data).tolist()

    # Calculate actual prices
    #predicted_prices = [round(float(np.exp(log_price)), 2) for log_price in predicted_log_prices]
    predicted_product_revenue = [round(float((revenue)), 2) for revenue in predicted_product_revenue]

    # Create a dictionary of predictions with property IDs as keys
    product_ids = input_data['id'].tolist()  # Assuming 'id' is the property ID column
    output_dict = dict(zip(product_ids, predicted_product_revenue))  # Use actual prices

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    rental_price_predictor_api.run(debug=True)
