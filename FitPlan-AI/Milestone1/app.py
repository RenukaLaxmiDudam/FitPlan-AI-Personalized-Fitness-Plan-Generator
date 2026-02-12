import streamlit as st

st.set_page_config(page_title="FitPlan AI", page_icon="🏋️", layout="centered")

st.title("FitPlan AI – User Fitness Profile")

# -----------------------------
# Personal Information
# -----------------------------
st.header("👤 Personal Information")

name = st.text_input("Enter Your Name *")

height = st.number_input("Height (in cm) *", min_value=1.0)
weight = st.number_input("Weight (in kg) *", min_value=1.0)

# -----------------------------
# Fitness Details
# -----------------------------
st.header("🏋️ Fitness Details")

goal = st.selectbox(
    "Fitness Goal",
    ["Build Muscle", "Weight Loss", "Strength Gain", "Abs Building", "Flexible"]
)

equipment = st.multiselect(
    "Available Equipment",
    ["Dumbbells", "Resistance Band", "Yoga Mat", "No Equipment"]
)

fitness_level = st.radio(
    "Fitness Level",
    ["Beginner", "Intermediate", "Advanced"]
)

# -----------------------------
# BMI Calculation
# -----------------------------
if st.button("Submit Profile"):

    if name == "":
        st.error("Name is required.")
    elif height <= 0 or weight <= 0:
        st.error("Height and Weight must be greater than zero.")
    else:
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        bmi = round(bmi, 2)

        # BMI Category
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"

        st.success("Profile Submitted Successfully!")

        st.subheader(f"{name}, your BMI is {bmi}")
        st.write(f"Category: **{category}**")
