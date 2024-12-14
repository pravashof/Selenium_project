import unittest
import time
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import HtmlTestRunner

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('test_log.txt'),
                        logging.StreamHandler()
                    ])

class ScreenshotTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create screenshots directory with full path and logging
        cls.screenshot_dir = os.path.abspath(os.path.join(os.getcwd(), 'test_screenshots'))
        try:
            os.makedirs(cls.screenshot_dir, exist_ok=True)
            logging.info(f"Screenshot directory created/verified at: {cls.screenshot_dir}")
        except Exception as e:
            logging.error(f"Failed to create screenshot directory: {e}")

    def setUp(self):
        # Set up Chrome WebDriver with additional options for reliability
        chrome_options = webdriver.ChromeOptions()
        # Uncomment if running headless
        # chrome_options.add_argument("--headless")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Maximize window to ensure full page visibility
        self.driver.maximize_window()
        
        # Navigate to login page
        self.driver.get("http://127.0.0.1:5500/site/autogen-demo/index.html")
        
        # Wait for page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

    def _save_screenshot(self, test_name):
        """
        Save screenshot with comprehensive error handling and logging
        
        Args:
            test_name (str): Name of the test method
        """
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        
        try:
            # Verify directory exists and is writable
            if not os.path.exists(self.screenshot_dir):
                logging.error(f"Screenshot directory does not exist: {self.screenshot_dir}")
                return
            
            if not os.access(self.screenshot_dir, os.W_OK):
                logging.error(f"No write permissions for directory: {self.screenshot_dir}")
                return
            
            # Attempt to save screenshot
            self.driver.save_screenshot(filepath)
            
            # Verify screenshot was created
            if os.path.exists(filepath):
                logging.info(f"Screenshot saved successfully: {filename}")
                print(f"Screenshot saved: {filename}")
            else:
                logging.error(f"Screenshot save failed: {filename}")
        
        except Exception as e:
            logging.error(f"Screenshot save error: {e}")
            # Additional debug information
            logging.error(f"Current working directory: {os.getcwd()}")
            logging.error(f"Absolute screenshot directory path: {self.screenshot_dir}")
            logging.error(f"Full file path attempted: {filepath}")

    def run(self, result=None):
        """
        Override run method to capture screenshot on test failure
        """
        result = super().run(result)
        
        # Check if the test failed
        if result and (len(result.failures) > 0 or len(result.errors) > 0):
            # Get the last test method name that failed
            if result.failures:
                test_method_name = result.failures[-1][0].shortDescription() or str(result.failures[-1][0])
            else:
                test_method_name = result.errors[-1][0].shortDescription() or str(result.errors[-1][0])
            
            # Save screenshot
            self._save_screenshot(test_method_name)
        
        return result

class TestLogin(ScreenshotTestCase):
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

            logging.info("Login test completed successfully!")

        except Exception as e:
            logging.error(f"Test failed: {str(e)}")
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
                # Wait for error message element
                error_message = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "error_message"))
                )
                
                # Assert that error message is displayed
                self.assertTrue(error_message.is_displayed(), "Error message not shown")
                logging.info("Invalid login test: Error message displayed successfully")
                print("Invalid login test: Error message displayed successfully")

            except Exception as e:
                # If no specific error message, verify no URL change
                self.assertIn("autogen-demo/index.html", driver.current_url, 
                              "Unexpected page navigation occurred")
                logging.info("Invalid login test: No redirection occurred")
                print("Invalid login test: No redirection occurred")

        except Exception as e:
            logging.error(f"Invalid login test failed: {str(e)}")
            raise

    def tearDown(self):
        # Close browser
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            output="reports",
            report_name="Login_Test_Report",
            combine_reports=True
        )
    )