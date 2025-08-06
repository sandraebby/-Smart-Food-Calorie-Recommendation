import streamlit as st
import pandas as pd
import numpy as np
import pickle 
import pandas as pd
model = pd.read_pickle("food_calorie_model.pkl")

with open('food_calorie_model.pkl', 'rb') as file:
    model = pickle.load(file)

# -------------------------------
# 🎨 Streamlit Page Configuration
# -------------------------------
st.set_page_config(
    page_title="🍏 Smart Food Calorie Recommender",
    page_icon="🥗",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("🥗 Smart Food & Calorie Recommendation")
st.markdown("""
Welcome to your **personal AI Nutritionist**!  
Log your food choices, and get **calorie estimates & recommendations** instantly.  
""")

# -------------------------------
# 📥 Load Model
# -------------------------------
MODEL_PATH = "food_calorie_model.pkl"

try:
    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error("❌ Trained model not found. Please upload `food_calorie_model.pkl`.")
    st.stop()
import pickle
import streamlit as st

MODEL_PATH = "food_calorie_model.pkl"

try:
    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error("❌ Trained model not found. Please upload `food_calorie_model.pkl`.")
    st.stop()
except ModuleNotFoundError as e:
    st.error(f"⚠️ Module required for deserializing the model is missing: {e}. "
             "Check your `requirements.txt` and make sure all dependencies are installed.")
    st.stop()
if not hasattr(model, "predict"):
    st.error("🚫 Loaded object is not a valid model. Please check the contents of the pickle file.")
    st.stop()

# -------------------------------
# 🎛️ Sidebar for User Input
# -------------------------------
st.sidebar.header("🍽️ Enter Your Meal Details")

meal_type = st.sidebar.selectbox(
    "Meal Type",
    ["Breakfast", "Lunch", "Dinner", "Snack"]
)

food_category = st.sidebar.selectbox(
    "Food Category",
    ["Fruits", "Vegetables", "Meat", "Fish", "Grains", "Dairy", "Fast Food", "Beverages"]
)

quantity = st.sidebar.slider(
    "Quantity (servings)",
    min_value=0.5,
    max_value=5.0,
    value=1.0,
    step=0.5
)

activity_level = st.sidebar.selectbox(
    "Activity Level Today",
    ["Low", "Moderate", "High"]
)

# Encode categorical features (example encoding)
activity_map = {"Low": 0, "Moderate": 1, "High": 2}
food_map = {
    "Fruits": 0, "Vegetables": 1, "Meat": 2, "Fish": 3,
    "Grains": 4, "Dairy": 5, "Fast Food": 6, "Beverages": 7
}

# -------------------------------
# 📊 Prepare Data for Prediction
# -------------------------------
features = np.array([
    food_map[food_category],
    quantity,
    activity_map[activity_level]
]).reshape(1, -1)

# -------------------------------
# 🔮 Predict Calories
# -------------------------------
if st.sidebar.button("🔥 Predict Calories"):
    prediction = model.predict(features)[0]
    
    st.subheader("🍽️ Meal Summary")
    st.write(f"- **Meal Type:** {meal_type}")
    st.write(f"- **Food Category:** {food_category}")
    st.write(f"- **Quantity:** {quantity} servings")
    st.write(f"- **Activity Level:** {activity_level}")
    
    st.success(f"**Estimated Calories:** {prediction:.2f} kcal 🔥")
    
    # Fun Recommendation
    if prediction > 700:
        st.warning("⚠️ This is a high-calorie meal. Consider a light workout today!")
    elif prediction < 300:
        st.info("✅ Low calorie! Great for weight management.")
    else:
        st.info("🍎 Balanced meal. Keep it up!")

# -------------------------------
# 📥 Downloadable Log
# -------------------------------
st.markdown("---")
st.subheader("📥 Download Your Food Log")

if st.button("Generate Sample Log"):
    df_log = pd.DataFrame({
        "Meal": [meal_type],
        "Food Category": [food_category],
        "Quantity": [quantity],
        "Activity Level": [activity_level],
        "Estimated Calories": [prediction if 'prediction' in locals() else None]
    })
    
    csv = df_log.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download My Food Log",
        data=csv,
        file_name="food_log.csv",
        mime="text/csv"
    )

# -------------------------------
# 🎨 Footer
# -------------------------------
st.markdown("""
---
💡 *Tip: Try different meals and track your daily intake for better weight management.*
""")
import joblib

model = joblib.load("food_calorie_model.joblib")
