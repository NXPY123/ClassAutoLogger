import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Replace with your LMS username and password
USERNAME = os.getenv("LMS_USERNAME", "")
PASSWORD = os.getenv("LMS_PASSWORD", "")

course_mapping = {
    "ICS 423": 12997,
    "ICS 422": 12996,
    "IOE 421": 13000
}

# Path to your timetable file (update this as needed)
TIMETABLE_FILE = "timetable.txt"

def load_timetable():
    """Load the timetable from a text file."""
    timetable = {}
    with open(TIMETABLE_FILE, "r") as f:
        # First line will be Day,First Hour,Second Hour,Third Hour,Fourth Hour,Fifth Hour,...
        hours = next(f).strip().split(',')[1:]
        for line in f:
            day, *classes = line.strip().split(',')
            timetable[day.strip()] = classes
    return timetable,hours

def get_current_class(timetable,hours):
    """Check the current class based on the timetable and time."""
    now = datetime.datetime.now()
    current_day = now.strftime("%A")
    current_hour = str(now.hour)
    
    if current_day in timetable:
        classes = timetable[current_day]

        if current_hour in hours and classes[hours.index(current_hour)].strip():
            return classes[hours.index(current_hour)].strip()
    return None

def login_to_lms(driver):
    """Log in to the LMS."""
    driver.get("https://lms.iiitkottayam.ac.in/login/logout.php")
    try:
        # Wait for redirection and continue if necessary
        WebDriverWait(driver, 10).until(
            EC.url_contains("https://lms.iiitkottayam.ac.in/")
        )
    except:
        # Click 'Continue' if redirected to logout page
        continue_button = driver.find_element(By.ID, "single_button678a2be8b590214")
        continue_button.click()
    
    # Ensure we're on the login page
    driver.get("https://lms.iiitkottayam.ac.in/login/index.php")

    # Fill in username and password
    driver.find_element(By.ID, "username").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)

    # Click login button
    driver.find_element(By.ID, "loginbtn").click()

def join_class(driver, course_id):
    """Join the class for the given course ID in a new tab."""
    # Open a new tab
    driver.execute_script("window.open('');")
    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[-1])
    # Navigate to the course link
    driver.get(f"https://lms.iiitkottayam.ac.in/mod/bigbluebuttonbn/view.php?id={course_id}")

    # Click on 'Join session' button
    join_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "join_button_input"))
    )
    join_button.click()

    # Switch to the newly opened tab for the session
    driver.switch_to.window(driver.window_handles[-1])
    listen_only_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='listenOnlyBtn']"))
    )
    listen_only_button.click()

def check_logged_in(driver):
    """Check if the user is logged in to the LMS in a separate tab."""
    try:
        # Open a new tab to check login status
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get("https://lms.iiitkottayam.ac.in/my/")
        WebDriverWait(driver, 10).until(
            EC.url_contains("https://lms.iiitkottayam.ac.in/my/")
        )
        # Close the check tab and return to the main tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return True
    except:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return False

def main():
    timetable,hours = load_timetable()
    driver = webdriver.Chrome()  # Replace with your preferred WebDriver
    try:
        while True:
            current_class = get_current_class(timetable,hours)
            
            if current_class:
                if current_class not in course_mapping:
                    print(f"Class {current_class} not found in course mapping.")
                    time.sleep(60)
                    continue
                while True:
                    try:
                        current_class = course_mapping[current_class]
                        print(f"Current class: {current_class}")
                        if not check_logged_in(driver):
                            login_to_lms(driver)
                        join_class(driver, current_class)
                        break
                    except Exception as e:
                        print(f"Error joining class: {e}")
                        time.sleep(60)

            else:
                print("No class at this time.")

            # Check current time. If minutes is 0, sleep for an hour else sleep for (60-minutes)*60 seconds
            now = datetime.datetime.now()
            minutes = now.minute
            print(f"Waiting for {60-minutes} minutes")  
            if minutes == 0:
                time.sleep(3600)
            else:
                time.sleep((60-minutes)*60)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
