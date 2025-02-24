import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import os

# Ensure models directory exists
os.makedirs("models", exist_ok=True)

# Load dataset
df = pd.read_csv("laptopdata.csv")
print("3")
# Encode categorical features
label_encoders = {}
categorical_cols = ["employment_status", "education_level"]
for col in categorical_cols:
    label_encoders[col] = LabelEncoder()
    df[col] = label_encoders[col].fit_transform(df[col])

# Define features and target (convert Boolean to 1/0)
X = df.drop(columns=["eligible_to_buy"])
y = df["eligible_to_buy"].astype(int)
print("2")
# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("4")
# Train SVM model with linear kernel and probability enabled
model = LinearSVC(dual=False)  # Use dual=False for large datasets
model.fit(X_train, y_train)
print("4")
y_pred = model.predict(X_test)
print("1")
# Evaluate performance
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, output_dict=True)
print("SVM Accuracy:", accuracy)
print("Classification Report:", report)

model_performance = {
    "accuracy": accuracy,
    "precision": report["1"]["precision"],
    "recall": report["1"]["recall"],
    "f1-score": report["1"]["f1-score"]
}
print(model_performance)
# Save model and label encoders
joblib.dump(model, "models/SVM.pkl")

