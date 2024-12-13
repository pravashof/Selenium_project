import pandas as pd

# Load the CSV file to understand its structure and content
csv_file_path = '/mnt/data/New document 2.csv'
csv_data = pd.read_csv(csv_file_path)

# Display the first few rows to analyze the structure
csv_data.head()


#============
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# Utility function to map bounding boxes and interactive elements
def create_selenium_script(data):
    """
    Generates Selenium code based on identified objects and their mappings to text.
    """
    selenium_script = """
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

# Set up Selenium WebDriver (Ensure ChromeDriver is installed and PATH is set)
driver = webdriver.Chrome()

# Navigate to the webpage
driver.get("http://127.0.0.1:5500/site/autogen-demo/index.html")

# Maximize the browser window
driver.maximize_window()

"""
    for _, row in data.iterrows():
        element_type = row['type']
        content = row['content']
        if row['interactivity']:
            # Generate code for interactive elements (input, button, etc.)
            if "input" in element_type.lower():
                selenium_script += f"""
# Locate input field associated with: {content}
input_element = driver.find_element(By.XPATH, "//*[contains(text(), '{content}')]/following-sibling::input")
input_element.send_keys("Sample Data")  # Example action: Typing into input field
"""
            elif "button" in element_type.lower() or "login" in content.lower():
                selenium_script += f"""
# Locate button with text: {content}
button_element = driver.find_element(By.XPATH, "//*[contains(text(), '{content}')]")
button_element.click()  # Example action: Clicking the button
"""
            elif "dropdown" in element_type.lower():
                selenium_script += f"""
# Locate dropdown menu associated with: {content}
dropdown_element = driver.find_element(By.XPATH, "//*[contains(text(), '{content}')]/following-sibling::select")
select = Select(dropdown_element)
select.select_by_visible_text("Admin")  # Example action: Selecting an option
"""
    selenium_script += """
# Close the driver after actions
driver.quit()
"""
    return selenium_script


# Create the Selenium script based on parsed data
interactive_elements = csv_data[csv_data['interactivity'] == True]  # Filter for interactive elements
script = create_selenium_script(interactive_elements)

# Save the script for reference
script_path = "/mnt/data/selenium_script.py"
with open(script_path, "w") as file:
    file.write(script)

script_path  # Returning the path of the generated script

#===========
#Final #

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

# Set up Selenium WebDriver (Ensure ChromeDriver is installed and PATH is set)
driver = webdriver.Chrome()

# Navigate to the webpage
driver.get("http://127.0.0.1:5500/site/autogen-demo/index.html")

# Maximize the browser window
driver.maximize_window()

# Locate input field associated with: Username
username_input = driver.find_element(By.XPATH, "//*[contains(text(), 'Username')]/following-sibling::input")
username_input.send_keys("SampleUsername")  # Example action: Typing into input field

# Locate input field associated with: Password
password_input = driver.find_element(By.XPATH, "//*[contains(text(), 'Password')]/following-sibling::input")
password_input.send_keys("SamplePassword")  # Example action: Typing into input field

# Locate dropdown menu associated with: Role
dropdown_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Role')]/following-sibling::select")
select = Select(dropdown_element)
select.select_by_visible_text("Admin")  # Example action: Selecting an option

# Locate button with text: Login
login_button = driver.find_element(By.XPATH, "//*[contains(text(), 'Login')]")
login_button.click()  # Example action: Clicking the button

# Close the driver after actions
driver.quit()
