import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

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
    """Join the class for the given course ID."""
    driver.get(f"https://lms.iiitkottayam.ac.in/mod/bigbluebuttonbn/view.php?id={course_id}")
    # Click on 'Join session' button
    join_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "join_button_input"))
    )
    join_button.click()

    # Switch to the new tab and click 'Listen only'
    driver.switch_to.window(driver.window_handles[-1])
    listen_only_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='listenOnlyBtn']"))
    )
    listen_only_button.click()

def main():
    timetable,hours = load_timetable()
    driver = webdriver.Chrome()  # Replace with your preferred WebDriver
    try:
        while True:
            current_class = get_current_class(timetable,hours)
            
            if current_class:
                current_class = course_mapping[current_class]
                print(f"Current class: {current_class}")
                login_to_lms(driver)
                join_class(driver, current_class)
            else:
                print("No class at this time.")

            # Wait for the next hour
            time.sleep(3600)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
