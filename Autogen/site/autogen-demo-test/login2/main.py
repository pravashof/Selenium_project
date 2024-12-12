import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
from locators import get_element_locator

# Set up logging
logging.basicConfig(
    filename='output/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Initialize the web driver (e.g., Chrome, Firefox)
driver = webdriver.Chrome()
logging.info('WebDriver initialized')

# Navigate to the webpage
driver.get("http://127.0.0.1:5500/site/autogen-demo/index.html")
logging.info('Navigated to the webpage')

# Read the CSV file
with open('data/new_document_2.csv', 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        # Get the element locator strategy and locator string
        locator_strategy, locator = get_element_locator(row)

        # Use Selenium to locate the element
        element = driver.find_element(locator_strategy, locator)
        logging.info(f'Found element: {locator}')

        # Interact with the element if it's interactive
        if row['interactivity'] == 'true':
            element.click()  # or any other appropriate action
            logging.info(f'Interacted with element: {locator}')

# Close the web driver
driver.quit()
logging.info('WebDriver closed')