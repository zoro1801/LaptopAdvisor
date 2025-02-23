from django.shortcuts import render, redirect
import joblib
import json
import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PERFORMANCE_PATH = os.path.join(BASE_DIR, "advisor/models", "performance.json")
with open(PERFORMANCE_PATH, "r") as f:
    model_performance = json.load(f)

LABEL_ENCODERS_PATH = os.path.join(BASE_DIR, "advisor/models", "label_encoders.pkl")
label_encoders = joblib.load(LABEL_ENCODERS_PATH)

def home(request):
    return render(request, "home.html", {"models": model_performance})

def select_model(request, model_name):
    return render(request, "input_form.html", {"model_name": model_name})

def predict(request):
    if request.method == "POST":
        model_name = request.POST.get("model_name")
        model_path = os.path.join(BASE_DIR, "advisor/models", f"{model_name.replace(' ', '_')}.pkl")
        model = joblib.load(model_path)

        try:
            age = int(request.POST.get("age"))
            income = float(request.POST.get("income"))
            credit_score = int(request.POST.get("credit_score"))
            employment_status = request.POST.get("employment_status")
            education_level = request.POST.get("education_level")
            savings = float(request.POST.get("savings"))

            # Backend Validations
            if not (18 <= age <= 100):
                return render(request, "result.html", {"error": "Age must be between 18 and 100."})

            if income < 0:
                return render(request, "result.html", {"error": "Income cannot be negative."})

            if not (300 <= credit_score <= 850):
                return render(request, "result.html", {"error": "Credit Score must be between 300 and 850."})

            if employment_status not in ["employed", "unemployed", "student", "retired"]:
                return render(request, "result.html", {"error": "Invalid Employment Status."})

            if education_level not in ["high school", "bachelor", "master", "doctorate"]:
                return render(request, "result.html", {"error": "Invalid Education Level."})

            if savings < 0:
                return render(request, "result.html", {"error": "Savings cannot be negative."})

        except ValueError:
            return render(request, "result.html", {"error": "Invalid input format. Please enter valid numeric values."})

        try:
            employment_encoded = label_encoders["employment_status"].transform([employment_status])[0]
            education_encoded = label_encoders["education_level"].transform([education_level])[0]
        except Exception as e:
            return render(request, "result.html", {"error": "Encoding error: " + str(e)})

        features = pd.DataFrame([[age, income, credit_score, employment_encoded, education_encoded, savings]],
                                columns=["age", "income", "credit_score", "employment_status", "education_level", "savings"])

        pred = model.predict(features)[0]
        result = "Eligible" if pred == 1 else "Not Eligible"

        return render(request, "result.html", {"prediction": result, "model_name": model_name})

    return redirect("home")
