from django.test import TestCase, Client
from django.urls import reverse

class HomePageTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_displays_all_models(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # Check that all expected model names appear on the home page
        expected_models = ["Naive Bayes", "Random Forest", "Logistic Regression", "SVM"]
        for model in expected_models:
            self.assertContains(response, model)

class SelectModelTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_select_model_page_heading(self):
        # Test for each model that the heading includes the model name.
        models = ["Naive Bayes", "Random Forest", "Logistic Regression", "SVM"]
        for model in models:
            response = self.client.get(reverse('select_model', args=[model]))
            self.assertEqual(response.status_code, 200)
            # Your updated template should have heading "Enter Your Details for <model>"
            self.assertContains(response, f"Enter Your Details for {model}")

class PredictViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_predict_valid_data_for_all_models(self):
        # Test valid input for each model
        models = ["Naive Bayes", "Random Forest", "Logistic Regression", "SVM"]
        for model in models:
            post_data = {
                "model_name": model,
                "age": "30",
                "income": "6000",
                "credit_score": "720",
                "employment_status": "employed",
                "education_level": "bachelor",
                "savings": "5000"
            }
            response = self.client.post(reverse('predict'), post_data)
            self.assertEqual(response.status_code, 200)
            content = response.content.decode("utf-8")
            # Check that the result page contains either "Eligible" or "Not Eligible"
            self.assertTrue("Eligible" in content or "Not Eligible" in content,
                            f"Model {model} did not return expected prediction text.")

    def test_predict_invalid_age(self):
        # Test invalid input for age (e.g., less than 18)
        post_data = {
            "model_name": "Naive Bayes",
            "age": "15",  # invalid age
            "income": "6000",
            "credit_score": "720",
            "employment_status": "employed",
            "education_level": "bachelor",
            "savings": "5000"
        }
        response = self.client.post(reverse('predict'), post_data)
        self.assertEqual(response.status_code, 200)
        # The error message "Age must be between 18 and 100." should appear
        self.assertContains(response, "Age must be between 18 and 100.")

    # You can add more tests for other invalid cases similarly.
