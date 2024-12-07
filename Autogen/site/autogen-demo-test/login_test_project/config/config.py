#import os
################
# Part A
################
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#CHROME_DRIVER_PATH = os.path.join(BASE_DIR, 'resources', 'chromedriver.exe')

##Following is the alternative to ## Part A
#from pathlib import Path
#CHROME_DRIVER_PATH = Path(BASE_DIR) / 'resources' / 'chromedriver.exe'

## Your app URL
#URL = "http://127.0.0.1:5500/site/autogen-demo/index.html"  

## Added post error for the above 
## AttributeError: 'WindowsPath' object has no attribute 'capabilities' 

############################################################
#Part B
############################################################
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# # Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME_DRIVER_PATH = os.path.join(BASE_DIR, 'resources', 'chromedriver.exe')

service = webdriver.ChromeService()
# Create a Service object with the ChromeDriver path
service = Service(CHROME_DRIVER_PATH)

# # Initialize the WebDriver with the Service object
driver = webdriver.Chrome(service=service)

# # Use the WebDriver
#driver.get("http://127.0.0.1:5500/site/autogen-demo/index.html")

URL = "http://127.0.0.1:5500/site/autogen-demo/index.html"



