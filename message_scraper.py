from selenium.webdriver.common.by import By

# Function to return scraped messages
def scrape_messages(driver,msg_arg):
    print("Starting message scraping...")
    
    try:
        messages = driver.find_elements(By.XPATH, msg_arg)
        print(f"Found {len(messages)} messages")
        
        if not messages:
            print("No messages found using the provided XPath.")
        else:
            for idx, msg in enumerate(messages):
                print(f"Message {idx+1}: {msg.text}")  # Print the message text to see the content
        return messages

    except Exception as e:
        print(f"Error occurred while scraping messages: {str(e)}")
        return []

