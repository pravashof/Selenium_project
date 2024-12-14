#This code runs the unittest discovery process to find and execute all test cases in the 'tests' directory that match the pattern 'custom_pattern*.py'. This is a common way to run a test suite in a Python project.
#python -m unittest discover -s tests -p "custom_pattern*.py"
#python -m unittest discover tests
import unittest
import time  # Import time for sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import HtmlTestRunner
#from config.config import CHROME_DRIVER_PATH, URL

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        ##Original below
        # self.driver = webdriver.Chrome(CHROME_DRIVER_PATH)
        #self.driver.get(URL)
        self.driver.get("http://127.0.0.1:5500/site/autogen-demo/index.html" )
        time.sleep(2)  # Pause for 2 seconds after the browser launches

    def test_valid_login_admin(self):
        driver = self.driver
        # Locate fields
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        role_dropdown = driver.find_element(By.NAME, "role")
        #Adding the "Login" button is an <input> element with the type="submit" attribute. 
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

    #  Verify redirection to the role-specific page
        expected_url = "http://127.0.0.1:5500/site/admin.html"  # Replace with actual Admin URL
        if driver.current_url == expected_url:
            print("Successfully redirected to the Admin page.")
        else:
            print("Redirection failed. Current URL:", driver.current_url)

    #  Verify the personalized message
        lbl_username = driver.find_element(By.ID, "lbl_username").text
        expected_message = "Hello, lbl_username! This is the landing page for the Admin!"
        if lbl_username == expected_message:
            print("Role-based message verified successfully.")
        else:
         print("Role-based message mismatch. Actual message:", lbl_username)

    #  Verify the logout functionality



    def tearDown(self):
        self.driver.quit()
        time.sleep(3)

if __name__ == "__main__":
    unittest.main(
            testRunner=HtmlTestRunner.HTMLTestRunner(
            output="reports",  # Folder where the reports will be generated
            report_name="Login_Test_Report",
            combine_reports=True  # Combines all test case results into a single file
            )
    )
## Additional Tests
# 1. Test for Invalid Login
# 2. Test for Empty Fields
# 3. Test for Invalid Role Selection
# 4. Test for Invalid Credentials
# 5. Test for Invalid Username
# 6. Test for Invalid Password
# 7. Test for Invalid Role
# 8. Test for Invalid Username and Password
# 9. Test for Invalid Username and Role
# 10. Test for Invalid Password and Role
# 11. Test for Invalid Username, Password, and Role
# 12. Test for Valid Login with Different Roles
# 13. Test for Logout Functionality
# 14. Test for Invalid Logout
# 15. Test for Invalid Logout with Different Roles
# 16. Test for Invalid Logout with Different Roles and Invalid Credentials
# 17. Test for Invalid Logout with Different Roles and Invalid Username
# 18. Test for Invalid Logout with Different Roles and Invalid Password
# 19. Test for Invalid Logout with Different Roles and Invalid Role
# 20. Test for Invalid Logout with Different Roles and Invalid Username and Password
    # 21. Test for Invalid Logout with Different Roles and Invalid Username and Role
# 22. Test for Invalid Logout with Different Roles and Invalid Password and Role
# 23. Test for Invalid Logout with Different Roles and Invalid Username, Password, and Role
# 24. Test for Invalid Logout with Different Roles and Valid Username, Password, and Role
# 25. Test for Invalid Logout with Different Roles and Invalid Username, Password, and Role





