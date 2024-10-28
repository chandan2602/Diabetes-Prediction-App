# Import necessary libraries
import streamlit as st
import numpy as np
import pickle

# Load the model from the pickle file
with open('final_lr.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

# Define the mean and standard deviation of the training data
mean_values = [41.885856, 0.07485, 0.03942, 27.320767, 5.527507, 138.058060]
std_values = [22.516840, 0.26315, 0.194593, 6.636783, 1.070672, 40.708136]

# Set custom CSS for background color, slider, and prediction result styling
page_bg_img = '''
<style>
    /* Main Background Color for Main Page */
    body,.stApp {
        background-color:#ffff; /* Light grey background */
    }

    /* Sidebar Styling */
    .css-1d391kg {  /* Sidebar background */
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    .css-1d391kg h2, .css-1d391kg p, .css-1d391kg label {  /* Sidebar text color */
        color: #202124;
    }

    /* Main Page Text Styling */
    h1 {
        color: #1a73e8;  /* Google blue for title */
    }
    p, div, label {
        color: #5f6368;  /* Updated paragraph color */
    }

    /* Button Styling */
    .stButton>button {
        background-color: #1a73e8;  /* Google blue for buttons */
        color: white;
        border-radius: 8px;
        font-size: 16px;
        padding: 8px 20px;
    }
    .stButton>button:hover {
        background-color: #f1f3f4;  /* Darker blue on hover */
    }

    /* Result Display with Conditional Coloring */
    .prediction-result {
        padding: 20px;
        border-radius: 10px;
        font-size: 18px;
    }
    .prediction-result-diabetic {
        background-color: rgba(234, 67, 53, 0.2);  /* Light red background */
        color: #ea4335;  /* Red text for "Diabetic" */
    }
    .prediction-result-non-diabetic {
        background-color: rgba(52, 168, 83, 0.2);  /* Light green background */
        color: #34a853;  /* Green text for "Not Diabetic" */
    }
</style>
'''

# Apply the CSS style in Streamlit
st.markdown(page_bg_img, unsafe_allow_html=True)

# App title and description
st.title('Diabetes Prediction')
st.write("Use this tool to assess your likelihood of having diabetes based on health indicators.")

# Define sidebar with input fields for user input
st.sidebar.header("Input Your Health Data")
age = st.sidebar.slider('Age', min_value=0, max_value=100, value=50, help="Enter your age in years")
hypertension = st.sidebar.selectbox('Hypertension', [0, 1], index=0, help="Select '1' if you have hypertension, else '0'")
heart_disease = st.sidebar.selectbox('Heart Disease', [0, 1], index=0, help="Select '1' if you have heart disease, else '0'")
bmi = st.sidebar.slider('BMI', min_value=10.0, max_value=50.0, value=25.0, step=0.1, help="Enter your BMI value")
HbA1c_level = st.sidebar.slider('HbA1c Level', min_value=4.0, max_value=15.0, value=7.0, step=0.1, help="Enter your HbA1c level")
blood_glucose_level = st.sidebar.slider('Blood Glucose Level', min_value=50, max_value=400, value=100, help="Enter your blood glucose level")

# Function to scale the input features
def scale_features(age, hypertension, heart_disease, bmi, HbA1c_level, blood_glucose_level):
    scaled_features = [(x - mean) / std for x, mean, std in zip(
        [age, hypertension, heart_disease, bmi, HbA1c_level, blood_glucose_level],
        mean_values, std_values
    )]
    return scaled_features

# Function to make predictions
def make_prediction(scaled_features):
    prediction = loaded_model.predict([scaled_features])
    return prediction

# Prediction button
if st.sidebar.button('Predict'):
    # Scale the input features and make the prediction
    scaled_features = scale_features(age, hypertension, heart_disease, bmi, HbA1c_level, blood_glucose_level)
    prediction = make_prediction(scaled_features)
    
    # Conditional styling for result display
    if prediction[0] == 1:
        result_message = "The model predicts that you are **Diabetic**."
        result_class = "prediction-result prediction-result-diabetic"
    else:
        result_message = "The model predicts that you are **Not Diabetic**."
        result_class = "prediction-result prediction-result-non-diabetic"
        
    # Display the result with custom style
    st.markdown(f"<div class='{result_class}'>{result_message}</div>", unsafe_allow_html=True)
    st.write("Note: This prediction is based on machine learning, and should not replace medical advice.")
