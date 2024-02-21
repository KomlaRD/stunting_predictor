import streamlit as st
import joblib
import numpy as np
from datetime import date

# Load the trained model
model = joblib.load('model.joblib')

# Title of the web app
st.title('Child Stunting Prediction Tool')

# Toggle for the user to choose between date-based age calculation or a manual option
age_input_method = st.radio("Select Age Input Method", ['Automatic Age Calculation', 'Manual Entry'])

# Initialize an age_in_months variable
age = None

if age_input_method == 'Automatic Age Calculation':
    # Get birth date and date of visit from user
    date_of_birth = st.date_input("Date of Birth")
    date_of_assessment = st.date_input("Date of Visit", min_value=date_of_birth, value=date.today())

    # Function to calculate the age in months
    def calculate_age_in_days(dob, current_date):
        return (current_date - dob).days

    # Compute and show the computed age in days
    age = calculate_age_in_days(date_of_birth, date_of_assessment)
    st.write(f"Calculated Age in Months: {age:.2f}")
else:
    # Allow the user to manually enter the age in months
    age = st.number_input('Enter the Age in Days', min_value=0.0, format="%.2f", step=0.01)

# Collect other necessary data for prediction
weight = st.number_input('Weight in kg', step=0.01)
lenhei = st.number_input('Height in cm', step=0.01)

# Button for the user to click to perform the prediction
predict_button = st.button('Predict Stunting')

if predict_button:
    # Make sure the age_in_months is not None
    if age is not None:
        # Employ the loaded model for the stunting prediction
        prediction = model.predict(np.array([[age, lenhei, weight]]))
        # Conditionally display the result of the stunting prediction
        if prediction == 1:
            st.success('The child is stunted. Refer to a nutrition professional for further assessment')
        else:
            st.success('The child is not stunted. Monitor according to facility protocol')
    else:
        st.error('Please ensure all details are provided correctly.')
