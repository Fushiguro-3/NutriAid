from flask import Flask, request, jsonify
from utils.calculations import calculate_bmi, calculate_calories
from utils.recommender import generate_meal_plan
from utils.llm import ask_gemini

from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

from database.db import get_db

app = Flask(__name__)
CORS(app)

# ---------------------------------------------
# BASIC ROUTE
# ---------------------------------------------
@app.route("/")
def home():
    return {"message": "NutriAid Backend Running ✅"}


# ---------------------------------------------
# DIET RECOMMENDER API
# ---------------------------------------------

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json

    age = data["age"]
    gender = data["gender"]
    height = data["height"]
    weight = data["weight"]
    activity = data["activity"]
    goal = data["goal"]

    bmi = calculate_bmi(weight, height)
    calories = calculate_calories(age, gender, height, weight, activity)

    # 1-day plan (backwards compatible)
    meal_plan = generate_meal_plan(calories, days=1)

    # 7-day weekly plan
    weekly_plan = generate_meal_plan(calories, days=7)

    return {
        "bmi": bmi,
        "daily_calories": calories,
        "meal_plan": meal_plan,
        "weekly_plan": weekly_plan,
    }

    data = request.json

    age = data["age"]
    gender = data["gender"]
    height = data["height"]
    weight = data["weight"]
    activity = data["activity"]
    goal = data["goal"]

    bmi = calculate_bmi(weight, height)
    calories = calculate_calories(age, gender, height, weight, activity)

    features = {
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "activity": activity,
        "goal": goal,
        "bmi": bmi,
        "calories": calories
    }

    meal_plan = generate_meal_plan(calories, features)

    return {
        "bmi": bmi,
        "daily_calories": calories,
        "meal_plan": meal_plan
    }

    data = request.json

    age = data["age"]
    gender = data["gender"]
    height = data["height"]
    weight = data["weight"]
    activity = data["activity"]
    goal = data["goal"]

    bmi = calculate_bmi(weight, height)
    calories = calculate_calories(age, gender, height, weight, activity)
    meal_plan = generate_meal_plan(calories)

    return {
        "bmi": bmi,
        "daily_calories": calories,
        "meal_plan": meal_plan
    }


# ---------------------------------------------
# CHAT API
# ---------------------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data["message"]

    prompt = f"You are a nutrition assistant. Reply simply. User asked: {user_message}"
    reply = ask_gemini(prompt)

    return {"reply": reply}


# ---------------------------------------------
# SIGNUP API
# ---------------------------------------------
@app.post("/signup")
def signup():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not (name and email and password):
        return jsonify({"error": "All fields required"}), 400

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, generate_password_hash(password))
        )
        conn.commit()
    except Exception:
        return jsonify({"error": "Email already exists"}), 400

    return jsonify({"message": "Signup successful"}), 200


# ---------------------------------------------
# LOGIN API
# ---------------------------------------------
@app.post("/login")
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    conn = get_db()
    cursor = conn.cursor()

    user = cursor.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Incorrect password"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    }), 200


# ---------------------------------------------
# RUN THE APP (AT THE VERY BOTTOM)
# ---------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
