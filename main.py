from driver_setup import setup_driver, load_website, browserRunning
from chat import locateChat, scrape_messages, waitLocateElement, scroll_to_yesterday
from message_parser import parseOrganicMessages
import traceback
import time

def main():

    # Variables containing different XPath and classes
    x_arg_chat = '//span[@title]'
    msg_arg = '//div[@class = "_akbu"]/span[@class = "_ao3e selectable-text copyable-text"]'
    chat_xpath = "//div[contains(@class, 'copyable-area')]/div[@class = '_ajyl']//div[@class = 'x3psx0u xwib8y2 xkhd6sd xrmvbpv']"
    class_name = "_akbu"
    
    # Setup driver 
    driver = setup_driver()

    try:

        print("Script Begins")

        # Load required website
        load_website(driver) 

        # Wait for chat element to load
        waitLocateElement(driver, "XPath", 600, x_arg_chat)

        # Wait for chats to load
        time.sleep(10)
        
        # Locate Chat
        locateChat(driver, "AMRITGRAM - Vegetable_Data Testing group")

        # Wait for search Box to load
        waitLocateElement(driver, "XPath", 15, chat_xpath)

        # Scroll to yesterday
        scroll_to_yesterday(driver)

        # Wait for class to load
        waitLocateElement(driver, "Class", 25, class_name)

        # Scrape Messages
        messages = scrape_messages(driver, msg_arg)

        if messages : 
            print("Scraped Successfully")
        else :
            print("No messages Found")

        # Parse Messages for Consolidated and EVAPMC
        parseOrganicMessages(driver, messages)

        # End of Script
        print("Script Ends")
        
        # Keep the browser running indefinitely until interrrupted
        browserRunning(driver)

    except KeyboardInterrupt:
        # Handle manual interruption (Ctrl+C)
        print("Script interrupted by user.")

    except Exception as e:
        # Log any unexpected exceptions
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()  # Print the stack trace for debugging

    finally:
        # Ensure the browser is closed properly
        driver.quit()


if __name__ == "__main__":
    main()


