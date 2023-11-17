from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
from selenium.common.exceptions import NoSuchElementException
import automation_methods
import element_manipulation_methods
import navigation_methods
import random
import time
import json
import os

from automation_methods import (
    initialize_web_driver_and_ignore_ssl_warnings, 
    load_problems_json_file, 
    load_sitesList_json_file, 
    random_mac_address
)

#from element_manipulation_methods import (
#    close_popup_if_exists, 
#    input_call_description_data,
#    bypass_new_device, 
#    restart_and_resync_pms_interface_on_GUI

#)

#from navigation_methods import (
#    navigate_to_clickup_site,
#    login_to_site_server,
#    navigate_to_pms_url,
#    navigate_to_walled_garden_url

#)
def create_task(driver, random_minutes):
    # Click the create task button
    click_button(driver, ".cu-draft-view__bottom-create")
    print("Task created!")
    # Wait and click the new task created button
    time.sleep(1.5)
    click_button(driver, ".toast__view-button-link")
    print("Task created button clicked")
    # Click the time dropdown
    click_button(driver, ".cu-task-hero-section__time-tracking-arrow")
    print("Clicked Time Dropdown")
    # Choose manual time entry
    time.sleep(0.5)
    click_button(driver, "div.cu-time-tracking-dropdown__option:nth-child(2)")
    print("Clicked Manual Time Dropdown")
    # Input time and submit
    random_minutes_str = f"{random_minutes} m"
    input_and_submit(driver, "/html/body/div[9]/div[2]/div/div/div/div[2]/cu-time-tracker-create-manual/div/div[1]/cu-time-estimates-input/div[1]/input", random_minutes_str)

def fill_field(driver, selector, value, field_type="input"):
    field = WebDriverWait(driver, 10 if field_type == "input" else 1).until(
        EC.presence_of_element_located((By.CSS_SELECTOR if field_type == "input" else By.XPATH, selector))
    )
    if field_type == "input":
        field.clear()
    field.click()
    field.send_keys(value)

def fill_dropdown_field(driver, dropdown_selector, option_selector, value):
    WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, dropdown_selector))).click()
    time.sleep(1.5)
    option_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, option_selector)))
    option_field.click()
    option_field.send_keys(value)
    time.sleep(1.5)
    option_field.send_keys(Keys.RETURN)
    if option_selector == ".cu-date-nlp-input__input":
        option_field.send_keys(Keys.ESCAPE)

def input_call_description_data(driver, site, problem):
    resolution_time = randomize_resolution_time()
    ticket_type = problem['type']  # Changed to problem['type']
    ticket_status = "Complete"
    time_logged = "now"
    progress = "resolved"
    fill_field(driver, '[cupendoid="quick-create-task-name-field"]', f"{site['name']} - {problem['task-title']}")
    fill_field(driver, "/html/body/app-root/cu-modal-keeper/cu-modal/div/div[2]/div[2]/div[2]/cu-quick-create/cu-create-task/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div/div[3]/div/cu-task-editor/div[1]/div[2]/div[3]/div[1]/div", 
               problem['description'], field_type="textarea")
    
    fill_dropdown_field(driver, "/html/body/app-root/cu-modal-keeper/cu-modal/div/div[2]/div[2]/div[2]/cu-quick-create/cu-create-task/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div/div[5]/cu-task-custom-fields/div/section/div[1]/div[3]/div[2]/cu-custom-field/cu-edit-task-custom-field-value/cu-edit-task-dropdown-custom-field-value/div/div", 
                        ".cu-select__search", problem['category'])
    fill_dropdown_field(driver, "/html/body/app-root/cu-modal-keeper/cu-modal/div/div[2]/div[2]/div[2]/cu-quick-create/cu-create-task/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div/div[5]/cu-task-custom-fields/div/section/div[1]/div[1]/div[2]/cu-custom-field/cu-edit-task-custom-field-value", ".cu-date-nlp-input__input", time_logged)
    fill_dropdown_field(driver, "/html/body/app-root/cu-modal-keeper/cu-modal/div/div[2]/div[2]/div[2]/cu-quick-create/cu-create-task/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div/div[5]/cu-task-custom-fields/div/section/div[1]/div[2]/div[2]/cu-custom-field/cu-edit-task-custom-field-value", ".cu-date-nlp-input__input", resolution_time)
    fill_dropdown_field(driver, "/html/body/app-root/cu-modal-keeper/cu-modal/div/div[2]/div[2]/div[2]/cu-quick-create/cu-create-task/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div/div[5]/cu-task-custom-fields/div/section/div[1]/div[4]/div[2]/cu-custom-field/cu-edit-task-custom-field-value/cu-edit-task-dropdown-custom-field-value/div/div", ".cu-select__search", site['name'])
    fill_dropdown_field(driver, "/html/body/app-root/cu-modal-keeper/cu-modal/div/div[2]/div[2]/div[2]/cu-quick-create/cu-create-task/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div/div[5]/cu-task-custom-fields/div/section/div[1]/div[5]/div[2]/cu-custom-field/cu-edit-task-custom-field-value/cu-edit-task-dropdown-custom-field-value/div/div", ".cu-select__search", problem['type'])
    fill_dropdown_field(driver, "/html/body/app-root/cu-modal-keeper/cu-modal/div/div[2]/div[2]/div[2]/cu-quick-create/cu-create-task/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div/div[5]/cu-task-custom-fields/div/section/div[1]/div[6]/div[2]/cu-custom-field/cu-edit-task-custom-field-value/cu-edit-task-dropdown-custom-field-value/div/div", ".cu-select__search", progress)
    fill_dropdown_field(driver, "/html/body/app-root/cu-modal-keeper/cu-modal/div/div[2]/div[2]/div[2]/cu-quick-create/cu-create-task/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div/div[5]/cu-task-custom-fields/div/section/div[1]/div[7]/div[2]/cu-custom-field/cu-edit-task-custom-field-value", ".cu-date-nlp-input__input", time_logged)
    fill_dropdown_field(driver, "/html/body/app-root/cu-modal-keeper/cu-modal/div/div[2]/div[2]/div[2]/cu-quick-create/cu-create-task/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div/div[5]/cu-task-custom-fields/div/section/div[1]/div[9]/div[2]/cu-custom-field/cu-edit-task-custom-field-value/cu-edit-task-dropdown-custom-field-value/div/div", ".cu-select__search", ticket_status)
    enter_text_and_press_enter(driver, "/html/body/app-root/cu-modal-keeper/cu-modal/div/div[2]/div[2]/div[2]/cu-quick-create/cu-create-task/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div/div[4]/div[1]", "/html/body/div[9]/div[2]/div/div/cu-status-list/div/div[1]/input", "CLOSED")
    #create_task(driver, random_minutes)

def close_popup_if_exists(driver):
    try:
        # Locate the close button of the popup
        close_button =WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/cu-modal-keeper/cu-modal/div/div[2]/div[2]/div[1]/div/button")))
        # Click the close button
        close_button.click()
    except NoSuchElementException:
        # If the close button is not found, continue without doing anything
        pass
def click_button(driver, selector, wait_time=1):
    button = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
    )
    button.click()

def input_and_submit(driver, selector, text, wait_time=10):
    try:
        input_field = WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located((By.XPATH, selector))
        )
        input_field.send_keys(text)
        input_field.send_keys(Keys.RETURN)
    except TimeoutException:
        print(f"Timeout: Unable to find element with selector {selector}")
    except Exception as e:
        print(f"An error occurred: {e}")

        
##This is for a specific element that interacts differently from all others. 
def enter_text_and_press_enter(driver, xpath, xpath2, text):
    try:
        print("you are about to start")
        input("Press Enter to continue...")
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        element.click()
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath2))
        )
        element.click()
        input("Press Enter to continue...")
        element.send_keys(text)
        input("Press Enter to continue...")
        element.send_keys(Keys.RETURN)
        input("Press Enter to continue...")
    except Exception as e:
        print(f"An error occurred with the call master status close dropdown: {e}")

def bypass_new_device(driver):
    mac_address_field = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[contains(@name, '[mac]') or substring(@name, string-length(@name) - string-length('[mac]') +1) = '[mac]']"))
    )
    mac_address_field.click()
    mac_address_field.send_keys(random_mac_address())
    upload_speed = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[contains(@name, '[upload_speed]') or substring(@name, string-length(@name) - string-length('[upload_speed]') +1) = '[upload_speed]']"))
    )
    upload_speed.click()
    upload_speed.send_keys("5120")
    download_speed = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[contains(@name, '[download_speed]') or substring(@name, string-length(@name) - string-length('[download_speed]') +1) = '[download_speed]']"))
    )
    download_speed.click()
    download_speed.send_keys("5120")    
    description = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[contains(@name, '[description]') or substring(@name, string-length(@name) - string-length('[description]') +1) = '[description]']"))
    )
    description.click()
    description.send_keys("Guest device")  
    save_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[@value='Save']"))
    )
    save_button.click()

def restart_and_resync_pms_interface_on_GUI(driver):
    # Wait for the 'Restart' button to be clickable
    restart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@value='Restart']"))
    )
    restart_button.click()
    time.sleep(2)  # Wait for 0.25 minute

    # Check for the 'Resync' button
    resync_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@value='Resync']"))
    )
    resync_button.click()

#NAVIGATION METHODS BELOW

def navigate_to_clickup_site():
    url = "https://app.clickup.com/37285326/v/l/6-900501424529-1"
    username = os.environ.get('CLICKUP_USERNAME')  # Assuming you've set these in your environment
    password = os.environ.get('CLICKUP_PASSWORD')

    # Initialize the WebDriver
    driver.get(url)

    # Perform login (update these selectors to match the actual login form elements)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "login-email-input"))).send_keys(username)
    time.sleep(5) 
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "login-password-input"))).send_keys(password + Keys.RETURN)
    time.sleep(10) 

def login_to_site_server(driver, site):
    # Use the provided CSS selectors
    username_selector = "#login-box-inner > form:nth-child(5) > input:nth-child(2)"
    password_selector = "#login-box-inner > form:nth-child(5) > input:nth-child(7)"
    
    # Retrieve username and password from environment variables
    username = os.environ.get('SITE_USERNAME')  
    password = os.environ.get('SITE_PASSWORD')

    # Wait for the username field to be present and locate it
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, username_selector))
    )

    # Wait for the password field to be present and locate it
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, password_selector))
    )

    # Enter the credentials and click the login button
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)



def navigate_to_pms_url(driver, base_url):
    pms_url = base_url.rstrip('/') + '/pmscom_ops.php'
    driver.get(pms_url)

def navigate_to_walled_garden_url(driver, base_url):
    walled_garden_url = base_url.rstrip('/') + '/netconfig_macwg.php'
    driver.get(walled_garden_url)

list_of_problems = load_problems_json_file()
list_of_sites = load_sitesList_json_file()

random_site = random.choice(list_of_sites)
random_problem = random.choice(list_of_problems)

driver = initialize_web_driver_and_ignore_ssl_warnings()
print("Opening URL:", random_site['url'])
try:
    driver.get(random_site['url'])
    print("Page loaded")
except Exception as e:
    print("Error loading page:", e)

def randomize_resolution_time():
    current_datetime = datetime.now().replace(second=0, microsecond=0)
    global random_minutes
    random_minutes = random.randint(14, 37)
    total_minutes = current_datetime.minute + random_minutes
    if total_minutes >= 60:
        additional_hours = total_minutes // 60
        total_minutes %= 60
        current_datetime += timedelta(hours=additional_hours)
    random_date_now = current_datetime.replace(minute=total_minutes)
    return random_date_now.strftime('%d/%m/%Y %H:%M:%S')




def create_a_new_ticket():
    time.sleep(5)
    close_popup_if_exists(driver)
    try:
        print("Trying to click button")
    # Trying to locate the element with visibility check
        quick_create_task_button = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/cu-app-shell/cu-manager/div[1]/div/div[2]/main/cu-dashboard/div/cu-views-bar-container/cu2-views-bar/cu-page-header-lazy-wrapper/cu-page-header/div/cu-create-cu-object-button/cu-create-cu-object-button-view/cu-create-task-menu/div/button"))
        )
    except Exception as e:
        print("Timed out waiting for the task name field to load.")
        raise 
    try:
        quick_create_task_button.click()
        print("Button clicked")
    except Exception as e:
        print("Error loading page:", e)
    
    
    input_call_description_data(driver, random_site, random_problem)

def handle_pms_issue():
    login_to_site_server(driver, random_site)
    #navigate_to_pms_url(driver, random_site['url'])
    #restart_and_resync_pms_interface_on_GUI(driver)
    navigate_to_clickup_site()
    create_a_new_ticket()

def bypass_a_device():
    login_to_site_server(driver, random_site)
    navigate_to_walled_garden_url(driver, random_site['url'])
    bypass_new_device(driver)
    navigate_to_clickup_site()
    create_a_new_ticket()

def login_to_site():
    login_to_site_server(driver, random_site)
    navigate_to_clickup_site()
    create_a_new_ticket()


def perform_action(problem):
    action = action_map.get(problem['name'])
    if action:
        action()
    else:
        print(f"No action defined for {problem['name']}")


# Action map
action_map = {
    "PMS": handle_pms_issue,
    "Server" : login_to_site,
    "Landing Page" : login_to_site,
    "General Query" : login_to_site,
    "Bypass" : bypass_a_device
}

perform_action(random_problem)




