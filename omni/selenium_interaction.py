from selenium import webdriver
from selenium.webdriver.common.by import By
from parse_csv import parse_csv
import time
import logging

def setup_logger(log_file):
    """
    Sets up a logger for logging Selenium interactions.
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger()

def interact_with_elements(driver, mappings, logger):
    """
    Locates and interacts with webpage elements based on mappings.
    """
    for mapping in mappings:
        try:
            if mapping["type"] == "edit_box":
                element = driver.find_element(By.XPATH, f'//*[@id="{mapping["id"]}"]')
                element.send_keys("Test Input")
                logger.info(f"Input text into edit box {mapping['id']}")

            elif mapping["type"] == "combo_box":
                element = driver.find_element(By.XPATH, f'//*[@id="{mapping["id"]}"]')
                element.click()
                logger.info(f"Opened combo box {mapping['id']}")
            else:
                logger.warning(f"Unhandled type: {mapping['type']} for {mapping['id']}")
        except Exception as e:
            logger.error(f"Failed to interact with {mapping['id']}: {e}")

if __name__ == "__main__":
    csv_path = "data/New_document_2.csv"
    log_file = "output/logs/interaction_logs.txt"
    logger = setup_logger(log_file)

    all_mappings, interactive_mappings = parse_csv(csv_path)
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5500/site/autogen-demo/index.html")
    driver.maximize_window()
    time.sleep(2)

    try:
        # Process all mappings
        interact_with_elements(driver, all_mappings, logger)
        # Process interactive mappings only
        interact_with_elements(driver, interactive_mappings, logger)
    finally:
        driver.quit()
