import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time


class TestModelsE2E(unittest.TestCase):
    def setUp(self):
        # Initialize the Chrome WebDriver (ensure chromedriver is installed and in your PATH)
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)  # seconds
        self.base_url = "http://127.0.0.1:8000"  # Adjust if your server runs on a different port

        # List of models to test
        self.models = ["Naive Bayes", "Random Forest", "Logistic Regression", "SVM"]

        # Define test data for both outcomes:
        self.test_data = {
            "eligible": {
                "age": "30",
                "income": "6000",
                "credit_score": "720",
                "employment_status": "employed",
                "education_level": "bachelor",
                "savings": "5000"
            },
            "not_eligible": {
                "age": "40",
                "income": "3000",
                "credit_score": "400",
                "employment_status": "unemployed",
                "education_level": "high school",
                "savings": "1000"
            }
        }

    def test_e2e_models(self):
        driver = self.driver

        # Loop over each model and each outcome ("eligible" and "not_eligible")
        for model in self.models:
            for outcome in ["eligible", "not_eligible"]:
                with self.subTest(model=model, outcome=outcome):
                    # 1. Navigate to the home page
                    driver.get(self.base_url + "/")

                    # 2. Wait for the home page to load by checking for the main header
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.TAG_NAME, "h1"))
                    )

                    # 3. Click on the link for the model. Link text should be like "Select Naive Bayes"
                    link_text = f"Select {model}"
                    model_link = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.LINK_TEXT, link_text))
                    )
                    time.sleep(2)
                    model_link.click()

                    # 4. Wait for the input form page to load.
                    # The heading should include "Enter Your Details for [Model Name]"
                    heading_text = f"Enter Your Details for {model}"
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, f"//h3[contains(text(), '{heading_text}')]"))
                    )

                    # 5. Fill in the form fields using the test data
                    driver.find_element(By.ID, "age").clear()
                    driver.find_element(By.ID, "age").send_keys(self.test_data[outcome]["age"])

                    driver.find_element(By.ID, "income").clear()
                    driver.find_element(By.ID, "income").send_keys(self.test_data[outcome]["income"])

                    driver.find_element(By.ID, "credit_score").clear()
                    driver.find_element(By.ID, "credit_score").send_keys(self.test_data[outcome]["credit_score"])

                    # Select employment status from dropdown
                    employment_dropdown = Select(driver.find_element(By.ID, "employment_status"))
                    employment_dropdown.select_by_value(self.test_data[outcome]["employment_status"])

                    # Select education level from dropdown
                    education_dropdown = Select(driver.find_element(By.ID, "education_level"))
                    education_dropdown.select_by_value(self.test_data[outcome]["education_level"])

                    driver.find_element(By.ID, "savings").clear()
                    driver.find_element(By.ID, "savings").send_keys(self.test_data[outcome]["savings"])

                    # 6. Submit the form
                    time.sleep(2)
                    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

                    # 7. Wait for the result page to load
                    result_heading = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.TAG_NAME, "h2"))
                    )

                    # 8. Verify that the result page displays the expected outcome
                    page_text = driver.page_source
                    expected_text = "Eligible" if outcome == "eligible" else "Not Eligible"
                    self.assertIn(expected_text, page_text,
                                  f"Model {model} expected '{expected_text}' but not found in the response.")

                    # Optional: pause briefly for observation (remove in CI)
                    time.sleep(2)

                    # Return to home page for next test iteration
                    driver.get(self.base_url + "/")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
