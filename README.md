NutriAid – AI-Based Personalized Diet Recommendation System

NutriAid is a full-stack AI-powered diet recommendation web application that provides personalized daily and weekly meal plans based on user health parameters such as BMI, calorie requirements, activity level, and goals.
The system integrates machine learning, backend APIs, authentication, and a responsive frontend to deliver a smart nutrition assistant experience.

📌 Problem Statement
Many individuals struggle to maintain a healthy diet due to lack of personalized guidance, awareness of nutritional needs, and time constraints. Existing solutions are often generic and do not adapt to individual health parameters such as BMI, activity level, or goals.
NutriAid aims to solve this problem by providing personalized diet plans using data-driven and AI-based approaches.

🎯 Objectives
To calculate BMI and daily calorie requirements
To generate personalized diet plans (1-day and 7-day)
To integrate a machine learning model for diet categorization
To provide secure authentication for users
To include an AI chatbot for nutrition-related queries
To build a scalable full-stack web application

🛠️ Tech Stack Used
🔹 Frontend
HTML
CSS
JavaScript
Fetch API

LocalStorage (for session handling)
🔹 Backend
Python
Flask
Flask-CORS
Flask-JWT-Extended (JWT Authentication)

🔹 Database
SQLite3 (Prototype stage)

🔹 Machine Learning
Random Forest Classifier
Scikit-learn
Pandas
Joblib

🔹 AI Integration
Google Gemini API (Nutrition chatbot)

🧠 Machine Learning Model
Algorithm Used: Random Forest Classifier
Purpose: Predict diet category (e.g., balanced, weight loss, high protein)

Features Used:
Age
Gender
Height
Weight
Activity Level
Goal
BMI
Daily Calories
Accuracy: ~0.6 – 1.0 (dataset-dependent)
Model Saved As: models/diet_model.pkl

📂 Dataset Details
1️⃣ Food Dataset (food_data.csv)

Contains:
Food name
Category (breakfast, lunch, snacks, dinner)
Calories
Carbohydrates
Protein
Fat
Tags (low-carb, high-protein, etc.)

2️⃣ User Diet Profiles (user_diet_profiles.csv)
Used for training the ML model:
User health parameters
Corresponding diet labels

🔐 Authentication
Secure JWT-based authentication
Users must log in to access:
Diet recommendation
Chatbot features
Tokens stored on frontend and sent via Authorization headers

⚙️ Key Features
✅ User Signup & Login
✅ BMI Calculation with Status (Underweight / Normal / Overweight / Obese)
✅ Daily Calorie Requirement Calculation
✅ AI-based Diet Recommendation
✅ 7-Day Meal Plan Generation
✅ Nutrition Chatbot using Gemini AI
✅ Secure APIs using JWT

Frontend (HTML/CSS/JS)
        |
        | REST APIs
        v
Flask Backend
 |        |        |
Auth   ML Model   Chatbot
 |        |
SQLite   Food Dataset

How to Run the Project Locally
1️⃣ Clone the Repository
git clone https://github.com/your-username/NutriAid.git
cd NutriAid

2️⃣ Backend Setup
cd NutriAid_Backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python app.py

Backend runs at:

http://127.0.0.1:5000

3️⃣ Frontend
Open index.html using Live Server or browser

Results
Successfully generated personalized diet plans
ML model improved relevance of recommendations
Weekly plans generated dynamically
Secure user access achieved via JWT
Chatbot provided real-time nutrition guidance

🔮 Future Scope
🔹 Deploy on Firebase / Cloud Platform
🔹 Replace SQLite with PostgreSQL / Firestore
🔹 Personalize diet plans for 4 lifestyle disorders:
Diabetes
Obesity
Hypertension
PCOS
🔹 Improve ML model with larger datasets
🔹 Add progress tracking & reports
🔹 Mobile app integration

📌 Conclusion
NutriAid successfully demonstrates how machine learning, backend APIs, and AI services can be combined to build a real-world personalized health application.
The system provides intelligent diet recommendations, promotes healthier lifestyles, and lays a strong foundation for future enhancements in personalized nutrition.
