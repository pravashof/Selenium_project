from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import logging
from parse_csv import parse_csv

# Function to set up a logger
def setup_logger(log_file):
    """
    Sets up a logger to log Selenium interactions.

    Args:
        log_file (str): Path to the log file.

    Returns:
        Logger: Configured logger instance.
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger()

# Function to interact with elements on the webpage
def interact_with_elements(driver, mappings, logger):
    """
    Locates and interacts with elements on the webpage based on mappings.

    Args:
        driver (webdriver): Selenium WebDriver instance.
        mappings (list): List of mappings containing element properties.
        logger (Logger): Logger instance to log interactions.
    """
    for mapping in mappings:
        try:
            # Handle different types of graphical objects
            if mapping["type"] == "edit_box":
                # Locate the element by its ID and input text
                element = driver.find_element(By.XPATH, f'//*[@id="{mapping["id"]}"]')
                element.send_keys("Test Input")
                logger.info(f"Input text into edit box with ID {mapping['id']}")

            elif mapping["type"] == "combo_box":
                # Locate the dropdown and interact with its options
                element = driver.find_element(By.XPATH, f'//*[@id="{mapping["id"]}"]')
                element.click()  # Open the dropdown
                logger.info(f"Opened combo box with ID {mapping['id']}")
                options = element.find_elements(By.TAG_NAME, "option")
                if options:
                    options[0].click()  # Select the first option
                    logger.info(f"Selected the first option in combo box {mapping['id']}")
                else:
                    logger.warning(f"No options found in combo box {mapping['id']}")

            else:
                logger.warning(f"Unhandled element type: {mapping['type']} for ID {mapping['id']}")

        except Exception as e:
            logger.error(f"Error interacting with element ID {mapping['id']}: {e}")

if __name__ == "__main__":
    # File path for the CSV file
    csv_path = "data/New_document_2.csv"
    # Parse the CSV file to extract mappings
    mappings = parse_csv(csv_path)

    # Set up logging
    log_file = "output/interaction_logs.txt"
    logger = setup_logger(log_file)

    # Initialize Selenium WebDriver (make sure ChromeDriver is installed)
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        # Open the webpage to interact with
        #driver.get("http://127.0.0.1:8000")
        driver.get("http://127.0.0.1:5500/site/autogen-demo/index.html")
        time.sleep(2)  # Allow the page to load

        # Interact with the elements based on mappings
        interact_with_elements(driver, mappings, logger)

    except Exception as e:
        logger.error(f"Failed to load or interact with the webpage: {e}")

    finally:
        # Pause to observe interactions and then close the browser
        time.sleep(5)
        driver.quit()
