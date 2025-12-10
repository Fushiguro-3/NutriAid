# train_diet_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# 1. Load your dataset (you will create this CSV)
# Columns example:
# age,gender,height,weight,activity,goal,bmi,calories,diet_label
df = pd.read_csv("data/user_diet_profiles.csv")

# 2. Features & label
X = df[["age", "gender", "height", "weight", "activity", "goal", "bmi", "calories"]]
y = df["diet_label"]   # e.g. "loss_low_carb", "gain_high_protein", …

# 3. Column types
numeric_features = ["age", "height", "weight", "bmi", "calories"]
categorical_features = ["gender", "activity", "goal"]

numeric_transformer = "passthrough"
categorical_transformer = OneHotEncoder(handle_unknown="ignore")

preprocess = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ]
)

# 4. Build pipeline (preprocess + model)
clf = Pipeline(
    steps=[
        ("preprocess", preprocess),
        ("model", RandomForestClassifier(
            n_estimators=150,
            random_state=42
        ))
    ]
)

# 5. Train / test split (for you to check accuracy if you want)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

clf.fit(X_train, y_train)
print("Training done!")
print("Train accuracy:", clf.score(X_train, y_train))
print("Test  accuracy:", clf.score(X_test, y_test))

# 6. Save the trained model
os.makedirs("models", exist_ok=True)
joblib.dump(clf, "models/diet_model.pkl")
print("✅ Model saved to models/diet_model.pkl")
