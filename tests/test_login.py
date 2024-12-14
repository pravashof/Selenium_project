import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import HtmlTestRunner

class TestLogin(unittest.TestCase):
    def setUp(self):
        # Set up Chrome WebDriver
        self.driver = webdriver.Chrome()
        
        # Navigate to login page
        self.driver.get("http://127.0.0.1:5500/site/autogen-demo/index.html")
        
        # Wait for page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

    def test_valid_login_admin(self):
        driver = self.driver
        
        try:
            # Locate login elements
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = driver.find_element(By.NAME, "password")
            role_dropdown = driver.find_element(By.NAME, "role")
            login_button = driver.find_element(By.XPATH, "//input[@type='submit']")

            # Input login credentials
            username_field.send_keys("pravash")
            password_field.send_keys("password")
            role_dropdown.send_keys("Admin")
            
            # Click login and wait for page transition
            login_button.click()

            # Wait for URL change and verify redirection
            WebDriverWait(driver, 10).until(
                EC.url_contains("admin.html")
            )

            # Verify correct URL
            self.assertIn("admin.html", driver.current_url, 
                          "Failed to redirect to admin page")
            
            # Verify personalized message
            lbl_username = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "lbl_username"))
            )
            
            expected_message = f"Hello, pravash! This is the landing page for the Admin!"
            self.assertEqual(
                lbl_username.text, 
                expected_message, 
                "Personalized message does not match expected format"
            )

            print("Login test completed successfully!")

        except Exception as e:
            # Capture screenshot on failure
            driver.save_screenshot(f"login_test_failure_{time.time()}.png")
            print(f"Test failed: {str(e)}")
            raise

    def test_invalid_login(self):
        driver = self.driver
        
        try:
            # Locate login elements
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = driver.find_element(By.NAME, "password")
            role_dropdown = driver.find_element(By.NAME, "role")
            login_button = driver.find_element(By.XPATH, "//input[@type='submit']")

            # Input invalid credentials
            username_field.send_keys("invalid_user")
            password_field.send_keys("wrong_password")
            role_dropdown.send_keys("Admin")
            
            # Click login
            login_button.click()

            # Wait and verify error message or no redirection
            try:
                error_message = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "error_message"))
                )
                self.assertTrue(error_message.is_displayed(), "Error message not shown")
                print("Invalid login test: Error message displayed successfully")
            except:
                # Verify no URL change
                self.assertIn("autogen-demo/index.html", driver.current_url, 
                              "Unexpected page navigation occurred")
                print("Invalid login test: No redirection occurred")

        except Exception as e:
            # Capture screenshot on failure
            driver.save_screenshot(f"invalid_login_test_failure_{time.time()}.png")
            print(f"Invalid login test failed: {str(e)}")
            raise

    def tearDown(self):
        # Close browser
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            output="reports",
            report_name="Login_Test_Report",
            combine_reports=True
        )
    )