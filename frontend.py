import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"

# Page configuration
st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🏥",
    layout="centered"
)

# Simple CSS for clean styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #2E86AB;
        margin-bottom: 30px;
    }
    .stButton > button {
        background-color: #2E86AB;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #1F5F8B;
    }
    .input-section {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

API_URL = "http://localhost:8000/predict" 

# Title
st.markdown('<h1 class="main-title">🏥 Insurance Premium Category Predictor</h1>', unsafe_allow_html=True)
st.markdown("---")

# Input section
st.markdown("### Enter your details below:")

# Organize inputs in columns for better layout
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=1, max_value=119, value=25)
    weight = st.number_input("Weight (kg)", min_value=1.0, value=70.0)
    height = st.number_input("Height (m)", min_value=0.5, value=1.7, step=0.01)

with col2:
    income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=5.0)
    smoker = st.selectbox("Are you a smoker?", options=[False, True], format_func=lambda x: "No" if not x else "Yes")
    city = st.text_input("City", placeholder="Enter your city")

# Full width for occupation
occupation = st.selectbox(
    "Occupation",
    ['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job']
)

st.markdown("---")

# Predict button
if st.button("🔮 Predict Premium Category"):
    # Input validation
    if not city.strip():
        st.error("⚠️ Please enter your city name.")
    else:
        input_data = {
            "age": age,
            "weight": weight,
            "height": height,
            "income_lpa": income_lpa,
            "smoker": smoker,
            "city": city,
            "occupation": occupation
        }

        try:
            with st.spinner('Analyzing your profile...'):
                response = requests.post(API_URL, json=input_data)
                
            if response.status_code == 200:
                result = response.json()['response']  # Access nested 'response' object
                category = result['predicted_category']
                confidence = result['confidence']
                probabilities = result['class_probabilities']
                
                # Display result with appropriate styling
                st.write("")  # Add some space
                st.write("")

                if str(category).lower() == 'low':
                    st.success(f"## ✅ **Predicted Premium Category: {category.upper()}**")
                    st.success(f"### 🎯 Confidence: {confidence:.0%}")
                    st.write("")
                    st.info("### 💡 Great! You qualify for lower premium rates.")
                elif str(category).lower() == 'medium':
                    st.warning(f"## ⚠️ **Predicted Premium Category: {category.upper()}**")
                    st.warning(f"### 🎯 Confidence: {confidence:.0%}")
                    st.write("")
                    st.info("### 💡 You fall into the standard premium range.")
                else:
                    st.error(f"## 🔴 **Predicted Premium Category: {category.upper()}**")
                    st.error(f"### 🎯 Confidence: {confidence:.0%}")
                    st.write("")
                    st.info("### 💡 Your profile indicates higher premium rates.")

                st.write("")  # Add space after
                st.write("")
                
                # Display additional probability information
                st.write("### 📊 Detailed Probability Breakdown")
                st.write("**Class Probabilities:**")
                for class_name, prob in probabilities.items():
                    st.progress(prob, text=f"{class_name}: {prob:.1%}")
                    
            else:
                st.error(f"❌ API Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("🔌 Could not connect to the FastAPI server. Make sure it's running on port 8000.")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "<small>This tool provides estimates for informational purposes only.</small>"
    "</div>", 
    unsafe_allow_html=True
)


# streamlit run frontend.py