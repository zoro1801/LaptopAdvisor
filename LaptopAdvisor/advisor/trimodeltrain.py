import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import json
import os

# Load dataset
df = pd.read_csv("laptopdata.csv")

# Encode categorical features
label_encoders = {}
categorical_cols = ["employment_status", "education_level"]
for col in categorical_cols:
    label_encoders[col] = LabelEncoder()
    df[col] = label_encoders[col].fit_transform(df[col])

# Define features and target
X = df.drop(columns=["eligible_to_buy"])
y = df["eligible_to_buy"].astype(int)  # Convert True/False to 1/0

# Split into train & test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize models
models = {
    "Naive Bayes": GaussianNB(),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=1000),  # increased max_iter
}

model_performance = {}

# Ensure models directory exists
os.makedirs("models", exist_ok=True)

# Train, evaluate & save models
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(name)
    report = classification_report(y_test, y_pred, output_dict=True)

    model_performance[name] = {
        "accuracy": accuracy,
        "precision": report["1"]["precision"],
        "recall": report["1"]["recall"],
        "f1-score": report["1"]["f1-score"]
    }

    joblib.dump(model, f"models/{name.replace(' ', '_')}.pkl")
    print("reach1")

# Save model performance as JSON
with open("models/performance.json", "w") as f:
    json.dump(model_performance, f, indent=4)

# Save label encoders
joblib.dump(label_encoders, "models/label_encoders.pkl")

print("✅ Models trained and saved successfully!")
