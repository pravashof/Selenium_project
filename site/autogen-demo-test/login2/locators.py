import os
import logging
from selenium.webdriver.common.by import By

def get_element_locator(row):
    """
    Generate the locator strategy and locator string based on the data in the CSV file.
    Also, print the element information to a file.
    """
    x = float(row['bbox'].split(',')[0])
    y = float(row['bbox'].split(',')[1])
    width = float(row['bbox'].split(',')[2]) - x
    height = float(row['bbox'].split(',')[3]) - y
    element_type = row['type']
    interactivity = row['interactivity']
    content = row['content']
    identifier = row['ID']

    xpath = f"//div[contains(@class, '{element_type}') and @x='{x}' and @y='{y}' and @width='{width}' and @height='{height}']"

    # Create the output directory if it doesn't exist
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f'Created output directory: {output_dir}')

    # Print the element information to a file
    with open(os.path.join(output_dir, 'element_info.txt'), 'a') as file:
        file.write(f"Element Type: {element_type}\n")
        file.write(f"Coordinates: x={x}, y={y}, width={width}, height={height}\n")
        file.write(f"Interactivity: {interactivity}\n")
        file.write(f"Content: {content}\n")
        file.write(f"Identifier: {identifier}\n")
        file.write('---\n')
        logging.info(f'Wrote element information to file: {element_type}, {identifier}')

    return By.XPATH, xpath