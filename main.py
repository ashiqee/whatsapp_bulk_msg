import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote
from selenium.webdriver.chrome.options import Options

# Load contacts from CSV
def load_contacts(file_path):
    return pd.read_csv(file_path, dtype=str)  # Read all data as strings to avoid float issues

# Initialize WebDriver with options to suppress TensorFlow errors
chrome_options = Options()
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open WhatsApp Web
driver.get('https://web.whatsapp.com')
print("Scan the QR code on WhatsApp Web to log in.")
time.sleep(20)  # Allow time for manual QR code scan

# Send messages dynamically
def send_message(number, personalized_message):
    try:
        encoded_message = quote(personalized_message)
        link = f'https://web.whatsapp.com/send/?phone={number}&text={encoded_message}'
        driver.get(link)
        time.sleep(10)

        action = ActionChains(driver)
        action.send_keys(Keys.ENTER)
        action.perform()

        print(f"Message sent to {number}")
        time.sleep(5)
    except Exception as e:
        print(f"Failed to send message to {number}: {e}")

# Main function to read CSV and send messages
def main():
    contacts = load_contacts('contacts.csv')

    for _, row in contacts.iterrows():
        number = row['number']
        user_name = row['user_name']
        msg_template = row['msg']

        # Ensure msg_template is not empty
        if pd.isna(msg_template) or not msg_template.strip():
            print(f"Skipping message for {user_name} due to missing template.")
            continue

        personalized_message = msg_template.format(user_name=user_name)
        send_message(number, personalized_message)

    driver.quit()

if __name__ == "__main__":
    main()
