# Interacts with webpage elements using Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from parse_csv import parse_csv

# Function to interact with elements on the webpage
def interact_with_elements(driver, mappings):
    """
    Locates and interacts with elements on the webpage based on mappings.

    Args:
        driver (webdriver): Selenium WebDriver instance.
        mappings (list): List of mappings containing element properties.
    """
    for mapping in mappings:
        try:
            # Handle different types of graphical objects
            if mapping["type"] == "edit_box":
                # Locate the element by its ID and input text
                element = driver.find_element(By.XPATH, f'//*[@id="{mapping["id"]}"]')
                element.send_keys("Test Input")
                print(f"Input text into edit box with ID {mapping['id']}")
            
            elif mapping["type"] == "combo_box":
                # Locate the dropdown and interact with its options
                element = driver.find_element(By.XPATH, f'//*[@id="{mapping["id"]}"]')
                element.click()  # Open the dropdown
                print(f"Opened combo box with ID {mapping['id']}")
                options = element.find_elements(By.TAG_NAME, "option")
                if options:
                    options[0].click()  # Select the first option
                    print(f"Selected the first option in combo box {mapping['id']}")
            
            # Additional interaction cases can be added here as needed
            
        except Exception as e:
            print(f"Error interacting with element ID {mapping['id']}: {e}")

if __name__ == "__main__":
    # File path for the CSV file
    csv_path = "data/New_document_2.csv"
    # Parse the CSV file to extract mappings
    mappings = parse_csv(csv_path)
    
    # Initialize Selenium WebDriver (make sure ChromeDriver is installed)
    driver = webdriver.Chrome()
    # Open the webpage to interact with
    driver.get("http://127.0.0.1:5500/site/autogen-demo/index.html")
    time.sleep(2)  # Allow the page to load

    # Interact with the elements based on mappings
    interact_with_elements(driver, mappings)

    # Pause to observe interactions and then close the browser
    time.sleep(5)
    driver.quit()
