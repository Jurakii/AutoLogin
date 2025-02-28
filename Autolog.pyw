import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def read_login_file():
    
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.realpath(__file__))
    
    login_file_path = os.path.join(base_dir, 'login.txt')
    
    # login.exe check
    if not os.path.exists(login_file_path):
        print(f"Error: login.txt file not found in {base_dir}")
        sys.exit(1)
    
    # Read login.txt
    with open(login_file_path, 'r') as file:
        email = file.readline().strip()
        password = file.readline().strip()
    
    return base_dir, email, password

def login_to_gnomon(base_dir, email, password):
    chromedriver_path = os.path.join(base_dir, 'chromedriver.exe')  # Path to chromedriver.exe
    chrome_binary_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Path to Chrome executable

    # Set Chrome options
    chrome_options = Options()
    chrome_options.binary_location = chrome_binary_path  # Set the path to the Chrome binary
    chrome_options.add_experimental_option("detach", True)  # Keep browser open after completion

    # Initialize the WebDriver with the Service object and Chrome options
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://online.gnomon.edu")

    # Input Email
    email_field = driver.find_element(By.NAME, "email")
    email_field.send_keys(email)

    # Input Password
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(password)

    # Login Button
    login_button = driver.find_element(By.NAME, "commit")  # Locate by 'name' attribute
    login_button.click()

    # Wait for the login process to complete
    time.sleep(5)

    print("Login successful. The browser will remain open.")

# Main execution
if __name__ == "__main__":
    base_dir, email, password = read_login_file()  # Now returns base_dir along with email and password
    login_to_gnomon(base_dir, email, password)  # Pass base_dir to the login function
