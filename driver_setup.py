from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import traceback
import time

# Setup driver with options and services
def setup_driver():
    # Configure ChromeOptions 
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-extensions")  # Disable extensions
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("--start-maximized")  # Start browser maximized
    # chrome_options.add_argument("--headless") #For headless execution , Whatsapp chrome wont launch a window

    user_data_dir = "D:\RWS\WAweb"  # Replace with your desired directory path

    # Set up Chrome options
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")  # Save session data
    chrome_options.add_argument("--profile-directory=Default")  # Use the default profile

    # Add your chromedriver path here
    chromedriver_path = "chromedriver.exe" 

    service = Service(executable_path=chromedriver_path)

    # Initialize the WebDriver with ChromeOptions
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Failed to start WebDriver: {e}")
        traceback.print_exc()
        exit(1)  # Exit if the WebDriver initialization fails
    
    return driver

# Load required website 
def load_website(driver):
    driver.get("https://web.whatsapp.com")
    time.sleep(5)

# script to keep browser running
def browserRunning(driver):
    while True:
        time.sleep(0.5)

        # Check if the browser is still open
        if len(driver.window_handles) == 0:
            print("Browser closed. Exiting script.")
            break

