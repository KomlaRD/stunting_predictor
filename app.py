import streamlit as st
import joblib
import numpy as np
from datetime import date

# Load the trained model
model = joblib.load('model.joblib')

# Reset functionality
if 'reset' not in st.session_state:
    st.session_state['reset'] = False

logo = "logo.webp"
st.image(logo, width=300)

# Title of the web app
st.title('Child Stunting Prediction Tool')

# Author information
st.markdown('**Author:** Eric Anku')
st.markdown('**Email:** ankueric1@gmail.com')

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
    st.write(f"Calculated Age in Days: {age}")
else:
    # Allow the user to manually enter the age in months
    age = st.number_input('Enter the Age in Days', min_value=0.0, format="%.2f", step=0.01)
# Validate age range
if age is not None and age > 1825:  # 5 years * 365 days
    st.error("Child is more than 5 years old.")
    
# Collect other necessary data for prediction
weight = st.number_input('Weight in kg', min_value=0.01, step=0.01)
lenhei = st.number_input('Height in cm', min_value=0.01, step=0.01)

# Reset button
if st.button('Reset'):
    st.session_state['reset'] = True
    st.experimental_rerun()

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
