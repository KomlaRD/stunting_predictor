import streamlit as st
import joblib
import numpy as np
from datetime import date

# Load the trained model
model = joblib.load('model.joblib')

# Logo
logo = "logo.webp"
st.image(logo, width=300)

# Title of the web app
st.title('Child Stunting Prediction Tool')
st.write("Tool for predicting stunting among children under five years in Ghana")

# Author information
st.markdown('**Author:** Eric Anku')
st.markdown('**Email:** ankueric1@gmail.com')

# Toggle for the user to choose between date-based age calculation or a manual option
age_input_method = st.radio("Select Age Input Method", ['Automatic Age Calculation', 'Manual Entry'])

# Initialize an age in days variable
age = None

# Function to calculate the age in days
def calculate_age_in_days(dob, current_date):
    return (current_date - dob).days

if age_input_method == 'Automatic Age Calculation':
    # Get birth date and date of visit from user
    date_of_birth = st.date_input("Date of Birth")
    date_of_assessment = st.date_input("Date of Visit", min_value=date_of_birth, value=date.today())
    
    if date_of_assessment < date_of_birth:
        st.error("Date of Visit cannot be before Date of Birth. Please check the dates.")   
    else:
        # Compute and show the computed age in days
        age = calculate_age_in_days(date_of_birth, date_of_assessment)
        st.write(f"Calculated Age in Days: {age}")
else:
    # Allow the user to manually enter the age in months
    age = st.number_input('Enter the Age in Days', min_value=0)
    
# Validate age range
if age is not None and age > 1825:  # 5 years * 365 days
    st.error("Child is more than 5 years old.")
    
# Collect other necessary data for prediction
weight = st.number_input('Weight in kg', min_value=0.01, step=0.01)
lenhei = st.number_input('Height in cm', min_value=0.01, step=0.01)

# Button for the user to click to perform the prediction
predict_button = st.button('Predict Stunting')

if predict_button:
    # Make sure the age in days is not None, weight and lenehi is greater than 0
    if age is not None and weight > 0 and lenhei > 0:
        # Employ the loaded model for the stunting prediction
        prediction = model.predict(np.array([[age, lenhei, weight]]))
        # Conditionally display the result of the stunting prediction
        if prediction == 1:
            st.success('The child is stunted. Refer to a nutrition professional for further assessment')
        else:
            st.success('The child is not stunted. Monitor according to facility protocol')
    else:
        st.error('Please ensure all details are provided correctly.')
