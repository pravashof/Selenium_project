import unittest
import time  # Import time for sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import HtmlTestRunner
import os

print(os.getcwd())  # Make sure this is your project's root directory


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:5500/site/autogen-demo/index.html")
        time.sleep(2)  # Pause for 2 seconds after the browser launches

    def test_valid_login_admin(self):
        driver = self.driver
        # Locate fields
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        role_dropdown = driver.find_element(By.NAME, "role")
        login_button = driver.find_element(By.XPATH, "//input[@type='submit']")

        # Input valid data
        username_field.send_keys("pravash")
        time.sleep(1)
        password_field.send_keys("password")
        time.sleep(1)
        role_dropdown.send_keys("Admin")  # Select "Admin" from dropdown
        time.sleep(1)
        login_button.click()
        time.sleep(2)

        # Validation: Check for a successful login

        # Verify redirection to the role-specific page
        expected_url = "http://127.0.0.1:5500/site/admin.html"  # Replace with actual Admin URL
        if driver.current_url == expected_url:
            print("Successfully redirected to the Admin page.")
        else:
            print("Redirection failed. Current URL:", driver.current_url)

        # Verify the personalized message
        lbl_username = driver.find_element(By.ID, "lbl_username").text
        expected_message = "Hello, lbl_username! This is the landing page for the Admin!"
        if lbl_username == expected_message:
            print("Role-based message verified successfully.")
        else:
            print("Role-based message mismatch. Actual message:", lbl_username)

    def tearDown(self):
        self.driver.quit()
        time.sleep(3)


if __name__ == "__main__":
    # Specify the report folder path
    report_folder = "reports"

    # Check if the report folder exists
    if not os.path.exists(report_folder):
        # If the folder doesn't exist, create it
        os.makedirs(report_folder)
        print(f"Folder does not exist. Created at the following path - {os.path.abspath(report_folder)}")
    else:
        print(f"Reports folder already exists at: {os.path.abspath(report_folder)}")

    # Run the tests and generate the report
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            output=report_folder,  # Folder where the reports will be generated
            report_name="Login_Test_Report",
            combine_reports=True  # Combines all test case results into a single file
        )
    )
