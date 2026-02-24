# 💪 FitPlan AI – Milestone 2: Core AI Model Integration

## 📌 Objective

The objective of Milestone 2 is to integrate a pre-trained Large Language Model (LLM) from Hugging Face into the FitPlan AI application.  
The system dynamically generates personalized workout plans based on user fitness inputs collected through the Streamlit interface.

This milestone enhances the application by enabling intelligent AI-driven workout generation.

---

## 🤖 Model Used

**Model Name:** google/flan-t5-small  
**Source:** Hugging Face Transformers Library  

The model is a lightweight instruction-tuned transformer model suitable for text generation tasks and optimized for deployment on CPU-based environments like Hugging Face Spaces (Free Tier).

---

## 🧠 Prompt Design Explanation

A structured dynamic prompt is generated using the following user inputs:

- Name
- Age
- BMI Category
- Fitness Goal
- Fitness Level
- Available Equipment

The prompt instructs the model to:

- Generate a structured 5-day workout plan
- Include warm-up exercises
- Include workout exercises with sets and reps
- Include rest periods
- Provide safety instructions
- Maintain professional structure and formatting

The prompt is dynamically built using a separate module (`prompt_builder.py`) to ensure modular and clean code architecture.

---

## ⚙️ Steps Performed

### 1️⃣ Model Integration
- Imported `AutoTokenizer` and `AutoModelForSeq2SeqLM` from Hugging Face.
- Loaded the pre-trained model (`google/flan-t5-small`).
- Implemented model caching using `@st.cache_resource` for efficiency.

### 2️⃣ Prompt Construction
- Created `prompt_builder.py`.
- Dynamically constructed prompts using user fitness data.
- Ensured structured instructions for consistent output.

### 3️⃣ Inference Implementation
- Tokenized the prompt.
- Generated text using `model.generate()`.
- Controlled output using:
  - max_length
  - temperature
  - num_beams
- Decoded and displayed the generated workout plan.

### 4️⃣ Error Handling
- Wrapped model loading inside try-except block.
- Wrapped inference logic inside try-except block.
- Displayed user-friendly error messages using Streamlit.

### 5️⃣ Testing Scenarios

The application was tested with three different user scenarios:

#### Scenario 1
- Age: 22
- BMI Category: Overweight
- Goal: Weight Loss
- Level: Beginner
- Equipment: No Equipment

#### Scenario 2
- Age: 30
- BMI Category: Normal Weight
- Goal: Build Muscle
- Level: Intermediate
- Equipment: Dumbbells

#### Scenario 3
- Age: 40
- BMI Category: Obese
- Goal: Strength Gain
- Level: Beginner
- Equipment: Resistance Band


