import os
import sys
import time
from playwright.sync_api import sync_playwright

# --- Path and Credential Setup ---

# This standard PyInstaller check is used to determine if the script is running
# from the bundled executable or from source.
if getattr(sys, 'frozen', False):
    # Running from the executable (.exe)
    # Get the directory of the executable file
    base_dir = os.path.dirname(sys.executable)
else:
    # Running from the source file (.pyw)
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Set the path to the external login.txt (same directory as the .exe or .pyw)
credentials_file = os.path.join(base_dir, "login.txt")

# Function to read the credentials from the external text file
def read_credentials(file_path):
    # Added error handling in case the file is missing or malformed
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            # Split only on the first '=' to handle passwords containing '='
            email = lines[0].strip().split('=', 1)[1].strip()
            password = lines[1].strip().split('=', 1)[1].strip()
        return email, password
    except FileNotFoundError:
        # Since this is a silent script, we raise an exception which will close the app
        raise Exception(f"FATAL ERROR: Credentials file not found at {file_path}")
    except IndexError:
        raise Exception("FATAL ERROR: Credentials file is malformed. Expected 'email=' and 'password=' lines.")


# Check if the credentials file exists and load it
try:
    email, password = read_credentials(credentials_file)
except Exception as e:
    # In a silent app, we can't show a message, but logging/raising ensures it fails safely
    sys.exit(1)


# --- Brave Browser Configuration ---

# Specify the path to the Brave Browser executable
# This path should work for standard Windows installations
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

try:
    with sync_playwright() as p:
        # Launch the Brave Browser executable
        browser = p.chromium.launch(
            executable_path=BRAVE_PATH,
            headless=False,
            slow_mo=50  # Slow down execution slightly for reliability
        )

        # Create a new page (tab)
        page = browser.new_page()

        # Navigate to the website
        page.goto("https://online.gnomon.edu")

        # --- Automation Steps ---

        # Find the email input field and enter the email
        # Use page.wait_for_selector for robustness
        page.wait_for_selector("#email")
        page.fill("#email", email)

        # Find the password input field and enter the password
        page.fill("#password", password)

        # Locate and check the 'Remember Me' checkbox (using a short timeout)
        try:
            page.check("#remember", timeout=2000)
        except:
            # Continue if the checkbox is not found
            pass

        # Find the submit button and click it to log in
        page.click("[name='commit']")

        # Wait for the login and page load to complete (wait for URL change is robust)
        # Note: If the login fails, this step might hang. Adjust wait time as needed.
        page.wait_for_timeout(5000)

        # Keep the browser open briefly after logging in
        # For a truly automated script, you might remove this line
        time.sleep(3)

        # The 'with' block ensures the browser closes cleanly when the script exits

except Exception:
    # Silent failure if Playwright or Brave launch fails
    sys.exit(1)

