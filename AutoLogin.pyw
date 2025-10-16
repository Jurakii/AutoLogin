import os
import sys
import time
from playwright.sync_api import sync_playwright

# --- Path and Credential Setup ---

# Use os.getcwd() which reliably gets the directory where the user launched the .exe from.
base_dir = os.getcwd() 
credentials_filename = "login.txt"
credentials_file = os.path.join(base_dir, credentials_filename)

def read_credentials(file_path):
    # This function is now silent, but uses the same robust error handling
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            email = lines[0].strip().split('=', 1)[1].strip()
            password = lines[1].strip().split('=', 1)[1].strip()
        return email, password
    except Exception:
        # If any error occurs (file not found, malformed, etc.), the script exits silently.
        sys.exit(1)


# Check if the credentials file exists and load it
try:
    email, password = read_credentials(credentials_file)
except Exception:
    sys.exit(1)


# --- Brave Browser Configuration ---

BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

try:
    with sync_playwright() as p:
        # Launch the Brave Browser executable
        browser = p.chromium.launch(
            executable_path=BRAVE_PATH,
            headless=False,
            slow_mo=50
        )

        page = browser.new_page()
        page.goto("https://online.gnomon.edu")

        # --- Automation Steps ---
        page.wait_for_selector("#email")
        page.fill("#email", email)
        page.fill("#password", password)

        try:
            page.check("#remember", timeout=2000)
        except:
            pass

        page.click("[name='commit']")

        # Wait for the page to load after login
        page.wait_for_timeout(5000)

        # --- KEEP ALIVE: Set to 24 hours (24 * 60 * 60 = 86400 seconds) ---
        # The browser will remain open until this timer expires OR the user manually closes the window.
        time.sleep(86400) 

except Exception:
    # Fail silently if the automation fails
    sys.exit(1)

# The browser will close when the time.sleep() expires or the script finishes.
