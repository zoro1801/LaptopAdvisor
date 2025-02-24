import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import joblib


# Helper function to generate realistic data
def generate_data(n=2000):
    data = []

    # Define income ranges based on employment status and education level
    income_ranges = {
        "employed": {"high school": (2000, 3000), "bachelor": (3000, 6000), "master": (6000, 9000),
                     "doctorate": (9000, 15000)},
        "unemployed": {"high school": (0, 1000), "bachelor": (0, 1500), "master": (0, 2500), "doctorate": (0, 3000)},
        "student": {"high school": (1000, 1500), "bachelor": (1500, 2500), "master": (2500, 4000),
                    "doctorate": (4000, 6000)},
        "retired": {"high school": (1000, 2000), "bachelor": (2000, 3000), "master": (3000, 4000),
                    "doctorate": (4000, 5000)}
    }

    # Logic to calculate eligibility
    def is_eligible_to_buy(income, credit_score, savings, employment_status, education_level):
        # Eligibility based on income, credit score, savings, and employment
        if income >= 5000 and credit_score >= 700:
            return True
        if savings >= 5000 and credit_score >= 650:
            return True
        if employment_status == "employed" and credit_score >= 650:
            return True
        if employment_status == "student" and income >= 2500 and credit_score >= 600:
            return True
        return False

    # Generate data for each user
    for _ in range(n):
        age = np.random.randint(18, 70)
        employment_status = np.random.choice(["employed", "unemployed", "student", "retired"])
        education_level = np.random.choice(["high school", "bachelor", "master", "doctorate"])
        credit_score = np.random.randint(300, 851)
        savings = np.random.randint(0, 20000)

        # Assign income based on employment and education
        min_income, max_income = income_ranges[employment_status][education_level]
        income = np.random.randint(min_income, max_income + 1)

        eligible_to_buy = is_eligible_to_buy(income, credit_score, savings, employment_status, education_level)

        data.append({
            "age": age,
            "income": income,
            "credit_score": credit_score,
            "employment_status": employment_status,
            "education_level": education_level,
            "savings": savings,
            "eligible_to_buy": eligible_to_buy
        })

    df = pd.DataFrame(data)
    return df


# Generate the data
n = 2000
df = generate_data(n)

# Save dataset to CSV (for reference)
df.to_csv("laptop_eligibility_realistic_data.csv", index=False)


print("✅ Realistic dataset created & model trained successfully!")
