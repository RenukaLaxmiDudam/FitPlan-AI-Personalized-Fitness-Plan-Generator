import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(page_title="FitPlan AI", page_icon="🏋️", layout="centered")
st.title("🏋️ FitPlan AI – 5 Day Structured Workout Generator")

# --------------------------------
# LOAD MODEL
# --------------------------------
@st.cache_resource
def load_model():
    model_name = "google/flan-t5-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    return tokenizer, model, device


tokenizer, model, device = load_model()

# --------------------------------
# BMI FUNCTIONS
# --------------------------------
def calculate_bmi(weight, height):
    height_m = height / 100
    return weight / (height_m ** 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal Weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


# --------------------------------
# USER INPUT
# --------------------------------
st.header("👤 Personal Information")

name = st.text_input("Enter Your Name *")
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
height = st.number_input("Height (cm) *", min_value=1.0)
weight = st.number_input("Weight (kg) *", min_value=1.0)

st.header("🏋️ Fitness Details")

goal = st.selectbox(
    "Fitness Goal",
    ["Build Muscle", "Weight Loss", "Strength Gain", "Abs Building", "Flexibility"]
)

fitness_level = st.radio(
    "Fitness Level",
    ["Beginner", "Intermediate", "Advanced"]
)

equipment = st.multiselect(
    "Available Equipment",
    ["Dumbbells", "Resistance Band", "Yoga Mat", "No Equipment"]
)

# --------------------------------
# GENERATE PLAN
# --------------------------------
if st.button("Generate Workout Plan"):

    if not name:
        st.error("Please enter your name.")
    elif height <= 0 or weight <= 0:
        st.error("Enter valid height and weight.")
    else:

        bmi = calculate_bmi(weight, height)
        bmi_status = bmi_category(bmi)
        equipment_list = ", ".join(equipment) if equipment else "No Equipment"

        st.success("Profile Submitted Successfully!")
        st.subheader(f"{name}, your BMI is {bmi:.2f}")
        st.write(f"Category: **{bmi_status}**")

        # STRONG STRUCTURED PROMPT
        prompt = f"""
You are a professional gym trainer.

Create a STRICT 5-day workout plan.

FORMAT MUST BE EXACTLY LIKE THIS:

Day 1:
Warm-up:
- exercise
- exercise
- exercise

Workout:
- exercise – sets x reps
- exercise – sets x reps
- exercise – sets x reps
- exercise – sets x reps

Rest: number seconds

Day 2:
Warm-up:
...
Workout:
...
Rest: ...

Continue until Day 5 only.

Rules:
- Minimum 3 warm-up exercises
- Minimum 4 workout exercises
- Must include sets and reps
- No explanations
- No paragraphs
- No motivational text
- Stop at Day 5

User:
Goal: {goal}
Level: {fitness_level}
Equipment: {equipment_list}
BMI Category: {bmi_status}

Start directly from Day 1:
"""

        with st.spinner("Generating structured workout plan..."):

            inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(device)

            outputs = model.generate(
                **inputs,
                max_new_tokens=900,
                temperature=1.0,
                top_p=0.95,
                do_sample=True,
                repetition_penalty=1.4,
                no_repeat_ngram_size=3
            )

            result = tokenizer.decode(outputs[0], skip_special_tokens=True)

            # --------------------------------
            # FORCE CLEAN STRUCTURE
            # --------------------------------

            # Remove anything before Day 1
            if "Day 1" in result:
                result = result[result.index("Day 1"):]

            # Cut after Day 5
            if "Day 6" in result:
                result = result.split("Day 6")[0]

            # Ensure all 5 days exist
            for i in range(1, 6):
                if f"Day {i}:" not in result:
                    result += f"\n\nDay {i}:\nWarm-up:\n- Jumping Jacks\n- Arm Circles\n- Bodyweight Squats\n\nWorkout:\n- Push-ups – 3x12\n- Squats – 3x15\n- Lunges – 3x12\n- Plank – 3x30 sec\n\nRest: 60 seconds\n"

        st.subheader("🏋️ Your Structured 5-Day Plan")
        st.text(result)
