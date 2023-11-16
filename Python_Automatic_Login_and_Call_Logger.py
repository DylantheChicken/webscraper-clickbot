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
import random
import time
import json
import os

from automation_methods import (
    initialize_web_driver_and_ignore_ssl_warnings, 
    load_problems_json_file, 
    load_sitesList_json_file, 
    login_to_site_server, 
    navigate_to_pms_url, 
    restart_and_resync_pms_interface_on_GUI
)


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
    
#def input_call_description_data(driver, site, problem):
#    # Prepare the task name
#    task_name = f"{site['name']} - {problem['task-title']}"
#    task_description = problem['description']
#    task_category = problem['category']
#    site_name = site['name']
#    ticket_type = problem['type']  # Changed to problem['type']
#    ticket_status = "in progress"
#    time_logged = "now"
#    progress = "resolved"

#    #TASK TITLE
#    task_name_field = WebDriverWait(driver, 10).until(
#        EC.presence_of_element_located((By.CSS_SELECTOR, '[cupendoid="quick-create-task-name-field"]'))
#    )
#    time.sleep(1) 
#    task_name_field.clear()
#    task_name_field.send_keys(task_name)

#    #TASK DESCRIPTION
#    task_description_field = WebDriverWait(driver, 1).until(
#        EC.presence_of_element_located((By.XPATH, "html/body/app-root/cu-app-shell/cu-manager/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div[2]/div[2]/div/div[2]/cu-task-editor/div[1]/div[2]/div[3]/div[1]"))
#    )
#    task_description_field.clear()
#    task_description_field.send_keys(task_description)

#    modal = WebDriverWait(driver, 10).until(
#        EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/cu-app-shell/cu-manager/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div[2]/div[2]/div")))
#    driver.execute_script("arguments[0].scrollTop = 175;", modal)

#    #RESPONSE TIME
#    response_time_field = WebDriverWait(driver, 1).until(
#        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/cu-app-shell/cu-manager/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div[2]/div[2]/div/cu-task-custom-fields/div/section/div[1]/div[1]/div[2]/cu-custom-field/cu-edit-task-custom-field-value/cu-custom-field-type-date/div/div"))
#    )
#    response_time_field.click()
#    time.sleep(2)
#    response_time_field_2 = WebDriverWait(driver, 10).until(
#        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cu-date-nlp-input__input"))
#    )
#    response_time_field_2.click()
#    response_time_field_2.send_keys(time_logged)
#    time.sleep(2.5) #Needs to be atleast 2 to provide drop down time to pupulate. 
#    response_time_field_2.send_keys(Keys.RETURN)
#    response_time_field_2.send_keys(Keys.ESCAPE)

#    #TASK CATEGORY
#    task_category_field = WebDriverWait(driver, 1).until(
#        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/cu-app-shell/cu-manager/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div[2]/div[2]/div/cu-task-custom-fields/div/section/div[1]/div[3]/div[2]/cu-custom-field/cu-edit-task-custom-field-value/cu-edit-task-dropdown-custom-field-value/div/div"))
#    )
#    task_category_field.click()
#    time.sleep(1.5)
#    task_category_field_2 = WebDriverWait(driver, 10).until(
#        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cu-select__search"))
#    )
#    task_category_field_2.click()
#    task_category_field_2.send_keys(task_category)
#    time.sleep(0.5)
#    task_category_field_2.send_keys(Keys.RETURN)
    
#    #SITE NAME
#    site_name_field = WebDriverWait(driver, 1).until(
#        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/cu-app-shell/cu-manager/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div[2]/div[2]/div/cu-task-custom-fields/div/section/div[1]/div[4]/div[2]/cu-custom-field/cu-edit-task-custom-field-value/cu-edit-task-dropdown-custom-field-value/div/div"))
#    )
#    site_name_field.click()
#    time.sleep(1.5)
#    site_name_field_2 = WebDriverWait(driver, 10).until(
#        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cu-select__search"))
#    )
#    site_name_field_2.click()
#    site_name_field_2.send_keys(site_name)
#    time.sleep(0.5)
#    site_name_field_2.send_keys(Keys.RETURN)

#    #TYPE
#    type_field = WebDriverWait(driver, 1).until(
#        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/cu-app-shell/cu-manager/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div[2]/div[2]/div/cu-task-custom-fields/div/section/div[1]/div[5]/div[2]/cu-custom-field/cu-edit-task-custom-field-value/cu-edit-task-dropdown-custom-field-value/div/div"))
#    )
#    type_field.click()

#    time.sleep(1.5)
#    type_field_2 = WebDriverWait(driver, 10).until(
#        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cu-select__search"))
#    )
#    type_field_2.click()
#    type_field_2.send_keys(ticket_type)
#    time.sleep(0.5)
#    type_field_2.send_keys(Keys.RETURN)

#    #LOGGED TIME
#    logged_time_field = WebDriverWait(driver, 1).until(
#        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/cu-app-shell/cu-manager/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div[2]/div[2]/div/cu-task-custom-fields/div/section/div[1]/div[7]/div[2]/cu-custom-field/cu-edit-task-custom-field-value"))
#    )
#    logged_time_field.click()

#    time.sleep(2)
#    logged_time_field_2 = WebDriverWait(driver, 10).until(
#        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cu-date-nlp-input__input"))
#    )
#    logged_time_field_2.click()
#    logged_time_field_2.send_keys(time_logged)
#    time.sleep(2.5)
#    logged_time_field_2.send_keys(Keys.RETURN)
#    logged_time_field_2.send_keys(Keys.ESCAPE)

#    #STATUS
#    status_field = WebDriverWait(driver, 1).until(
#        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/cu-app-shell/cu-manager/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div[2]/div[2]/div/cu-task-custom-fields/div/section/div[1]/div[9]/div[2]/cu-custom-field/cu-edit-task-custom-field-value/cu-edit-task-dropdown-custom-field-value/div/div"))
#    )
#    status_field.click()

#    time.sleep(1.5)
#    status_field_2 = WebDriverWait(driver, 10).until(
#        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cu-select__search"))
#    )
#    status_field_2.click()
#    status_field_2.send_keys(ticket_status)
#    time.sleep(0.5)
#    status_field_2.send_keys(Keys.RETURN)

#    #PROGRESS
#    progress_field = WebDriverWait(driver, 1).until(
#        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/cu-app-shell/cu-manager/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div[2]/div[2]/div/cu-task-custom-fields/div/section/div[1]/div[6]/div[2]/cu-custom-field/cu-edit-task-custom-field-value/cu-edit-task-dropdown-custom-field-value/div/div"))
#    )
#    progress_field.click()

#    time.sleep(1.5)
#    progress_field_2 = WebDriverWait(driver, 10).until(
#        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cu-select__search"))
#    )
#    progress_field_2.click()
#    progress_field_2.send_keys(progress)
#    time.sleep(0.5)
#    progress_field_2.send_keys(Keys.RETURN)

#    #RESOLUTION TIME
#    resolution_time_field = WebDriverWait(driver, 1).until(
#        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/cu-app-shell/cu-manager/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div[2]/div[2]/div/cu-task-custom-fields/div/section/div[1]/div[2]/div[2]/cu-custom-field/cu-edit-task-custom-field-value/cu-custom-field-type-date/div/div"))
#    )
#    resolution_time_field.click()

#    time.sleep(2)
#    resolution_time_field_2 = WebDriverWait(driver, 10).until(
#        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cu-date-nlp-input__input"))
#    )
#    resolution_time_field_2.click()
#    resolution_time = randomize_resolution_time()
    
#    resolution_time_field_2.send_keys(resolution_time)
#    time.sleep(2.5)
#    resolution_time_field_2.send_keys(Keys.RETURN)
#    resolution_time_field_2.send_keys(Keys.ESCAPE)

    


#    #CREATE TASK
#    create_task_button = WebDriverWait(driver, 1).until(
#        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cu-draft-view__submit"))
#    )
#    create_task_button.click()

#    #time.sleep(5)
#    #element = WebDriverWait(driver, 10).until(
#    #        EC.presence_of_element_located((By.XPATH, f"//span[text()='{task_name}']"))
#    #    )
#    #element.click()
#    time.sleep(1.5)
#    new_task_created_button = WebDriverWait(driver, 1).until(
#        EC.element_to_be_clickable((By.CSS_SELECTOR, ".toast__view-button-link"))
#    )
#    new_task_created_button.click()
#    time.sleep(1.5)
#    new_dropdown_time = WebDriverWait(driver, 1).until(
#        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/cu-task-keeper/cu-manager-view-task/div[2]/div/div/aside/div[2]/div[2]/div[2]/div[2]/div[2]/cu-time-tracking-dropdown"))
#    )
#    new_dropdown_time.click()
    
#    time.sleep(0.5)
#    new_dropdown_time_manual = WebDriverWait(driver, 1).until(
#        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.cu-time-tracking-dropdown__option:nth-child(2)"))
#    )
#    new_dropdown_time_manual.click()
#    random_minutes_str = str(random_minutes) + " m"
#    timespent_inptut = WebDriverWait(driver, 1).until(
#        EC.element_to_be_clickable((By.XPATH, "/html/body/div[9]/div[2]/div/div/div/div[2]/cu-time-tracker-create-manual/div/div[1]/cu-time-estimates-input/div[1]/input"))
#    )
#    timespent_inptut.click()
#    timespent_inptut.send_keys(random_minutes_str)
#    timespent_inptut.send_keys(Keys.RETURN)

    
#    new_task_close_button = WebDriverWait(driver, 1).until(
#        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/cu-task-keeper/cu-manager-view-task/div[2]/div/div/aside/div[1]/div[1]/div[1]/div"))
#    )
#    new_task_close_button.click()
#    new_task_close_button_input = WebDriverWait(driver, 1).until(
#        EC.element_to_be_clickable((By.XPATH, "/html/body/div[9]/div[2]/div/div/cu-status-list/div/div[1]/input"))
#    )
#    new_task_close_button_input.click()
#    new_task_close_button_input.send_keys("Closed")
    
#    input("Press Enter to continue...")

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

def log_a_PMS_ticket():
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
    input("Press Enter to continue...")

def handle_pms_issue():
    #navigate_to_pms_url(driver, random_site['url'])
    #restart_and_resync_pms_interface_on_GUI(driver)
    navigate_to_clickup_site()
    log_a_PMS_ticket()


def perform_action(problem):
    action = action_map.get(problem['name'])
    if action:
        action()
    else:
        print(f"No action defined for {problem['name']}")

login_to_site_server(driver, random_site)



# Action map
action_map = {
    "PMS": handle_pms_issue
}

perform_action(random_problem)




