from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


#  Find the search box and search for the contact 
def locateChat(driver,chat_name):
    search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='3']")
    search_box.click()
    search_box.send_keys(Keys.CONTROL + "a") 
    search_box.send_keys(Keys.BACKSPACE)
    search_box.send_keys(chat_name)
    search_box.send_keys(Keys.ENTER)

# Scrolls to the top of the synced chat window
def load_all_messages(driver, chat_window_xpath):
    chat_window = driver.find_element(By.XPATH, chat_window_xpath)
    last_height = driver.execute_script("return arguments[0].scrollHeight", chat_window)
    
    while True:
        chat_window.send_keys(Keys.PAGE_UP)
        time.sleep(1)
        
        new_height = driver.execute_script("return arguments[0].scrollHeight", chat_window)
        if new_height == last_height:
            break  # Stop if no more new messages are loaded
        last_height = new_height
    
# Scrape messages in a particular chat
def scrape_messages(driver,msg_arg):
    messages = driver.find_elements(By.XPATH, msg_arg)
    return messages

# Expands the read more section
def click_read_more(driver, message_element):
    try:
        # Initialize WebDriverWait to wait for elements to be clickable
        wait = WebDriverWait(driver, 5)

        # Scroll the message element into view
        driver.execute_script("arguments[0].scrollIntoView(false);", message_element)
        time.sleep(1)

        # Locate the parent container of the message (div containing both message and 'Read more')
        parent_container = message_element.find_element(By.XPATH, "./..")

        # Try to find and click all "Read more" buttons inside this parent container
        while True:
            try:
                
                # Look for the "Read more" button within the parent container
                read_more_button = parent_container.find_element(By.XPATH, ".//div[contains(@class, 'read-more-button')]")

                # Scroll the button into view and adjust a few pixels down
                driver.execute_script("arguments[0].scrollIntoView(true);", read_more_button)
                driver.execute_script("window.scrollBy(0, 500);")  # Scroll down by 500px to ensure visibility
                time.sleep(1)  # Small delay for scrolling adjustment

                # Check if the button is visible and enabled for clicking
                if read_more_button.is_displayed() and read_more_button.is_enabled():
                    try:
                        # Try using normal WebDriver click
                        read_more_button.click()
                        print("Read more clicked")
                        
                    except Exception:
                        # Try using JavaScript click if normal click fails
                        driver.execute_script("arguments[0].click();", read_more_button)

                    time.sleep(1)  # Wait for the new content to load

                    # Scroll again to the bottom of the message after clicking
                    driver.execute_script("arguments[0].scrollIntoView(false);", message_element)
                else:
                    print("Read more not found")
                    break  # Exit loop if button is not clickable

            except TimeoutException:
                break  # Exit loop if no "Read more" button is found

            except Exception as e:
                print(f"Error clicking 'Read more': {e}")
                break

    except Exception as e:
        print(f"Error expanding 'Read more': {e}")
   
# Waits for an element to load/render
def waitLocateElement(driver, elem, time, arg):
    if(elem == "XPath"):
        WebDriverWait(driver,time).until(
            EC.presence_of_element_located((By.XPATH,arg))
        )
    elif(elem == "Class"):
        WebDriverWait(driver, time).until(
            EC.presence_of_element_located((By.CLASS_NAME, arg))
        )

# Scrolls to find the yesterday tag
def scroll_to_yesterday(driver):
    """
    Scrolls the WhatsApp chat window until it finds the 'Yesterday' marker.
    """
    wait = WebDriverWait(driver, 1)

    # XPath for the 'Yesterday' marker
    yesterday_xpath = "//div[@class = '_amjw _amk1 _aotl  focusable-list-item']/div[@class = '_amk4 _amkb']/span[contains(text(), 'YESTERDAY')]"
    
    scroll_attempts = 0
    max_scroll_attempts = 30

    while scroll_attempts < max_scroll_attempts:
        try:
            # Try to locate the "Yesterday" marker
            yesterday_element = wait.until(EC.presence_of_element_located((By.XPATH, yesterday_xpath)))

            # Scroll the 'Yesterday' marker into view
            driver.execute_script("arguments[0].scrollIntoView(true);", yesterday_element)
            print("Successfully scrolled to the 'Yesterday' marker.")
            return  # Exit the loop once the 'Yesterday' marker is found
        
        except Exception as e:
            print(f"Could not find 'Yesterday' marker yet. Scrolling up. Attempt: {scroll_attempts + 1}")
            
            # If 'Yesterday' is not found, scroll up to load more messages
            chat_box = driver.find_element(By.XPATH, "//div[@class = '_ajyl']")
            chat_box.send_keys(Keys.PAGE_UP)
            chat_box.send_keys(Keys.PAGE_UP)
            scroll_attempts += 1
            time.sleep(1)  # Give some time for messages to load after scrolling

    print("Unable to find the 'Yesterday' marker after maximum scroll attempts.")






