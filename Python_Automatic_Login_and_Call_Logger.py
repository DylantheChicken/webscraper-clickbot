from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
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

def randomise_resolution_time():
    # Store the current datetime, setting seconds and microseconds to zero
    current_datetime = datetime.now().replace(second=0, microsecond=0)

    # Generate a random number of minutes between 14 and 37
    global random_minutes 
    
    random_minutes = random.randint(14, 37)

    # Add random minutes to the current datetime, ensuring the minute field doesn't exceed 59
    total_minutes = current_datetime.minute + random_minutes
    if total_minutes >= 60:
    # Adjust for the overflow in minutes
        additional_hours = total_minutes // 60
        total_minutes = total_minutes % 60
        current_datetime += timedelta(hours=additional_hours)

    # Update the datetime with the new minute value
    random_date_now = current_datetime.replace(minute=total_minutes)

    # Format the datetime
    formatted_random_date_now = random_date_now.strftime('%d/%m/%Y %H:%M:%S')

    return formatted_random_date_now

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
    
def input_call_description_data(driver, site, problem):
    # Prepare the task name
    task_name = f"{site['name']} - {problem['task-title']}"
    task_description = f"{problem['description']}"
    task_category = f"{problem['category']}"
    site_name = f"{site['name']}"
    ticket_type = "phone call"
    ticket_status = "in progress"
    time_logged = "now"
    resolution = ""
    progress = "busy"

    #TASK TITLE
    task_name_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[cupendoid="quick-create-task-name-field"]'))
    )
    time.sleep(1) 
    task_name_field.clear()
    task_name_field.send_keys(task_name)

    #TASK DESCRIPTION
    task_description_field = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.XPATH, "html/body/app-root/cu-app-shell/cu-manager/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div[2]/div[2]/div/div[2]/cu-task-editor/div[1]/div[2]/div[3]/div[1]"))
    )
    task_description_field.clear()
    task_description_field.send_keys(task_description)

    modal = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/cu-app-shell/cu-manager/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div[2]/div[2]/div")))
    driver.execute_script("arguments[0].scrollTop = 175;", modal)

    #RESPONSE TIME
    response_time_field = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/cu-app-shell/cu-manager/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div[2]/div[2]/div/cu-task-custom-fields/div/section/div[1]/div[1]/div[2]/cu-custom-field/cu-edit-task-custom-field-value/cu-custom-field-type-date/div/div"))
    )
    response_time_field.click()
    time.sleep(2)
    response_time_field_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cu-date-nlp-input__input"))
    )
    response_time_field_2.click()
    response_time_field_2.send_keys(time_logged)
    time.sleep(2.5) #Needs to be atleast 2 to provide drop down time to pupulate. 
    response_time_field_2.send_keys(Keys.RETURN)
    response_time_field_2.send_keys(Keys.ESCAPE)

    #TASK CATEGORY
    task_category_field = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/cu-app-shell/cu-manager/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div[2]/div[2]/div/cu-task-custom-fields/div/section/div[1]/div[3]/div[2]/cu-custom-field/cu-edit-task-custom-field-value/cu-edit-task-dropdown-custom-field-value/div/div"))
    )
    task_category_field.click()
    time.sleep(1.5)
    task_category_field_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cu-select__search"))
    )
    task_category_field_2.click()
    task_category_field_2.send_keys(task_category)
    time.sleep(0.5)
    task_category_field_2.send_keys(Keys.RETURN)
    
    #SITE NAME
    site_name_field = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/cu-app-shell/cu-manager/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div[2]/div[2]/div/cu-task-custom-fields/div/section/div[1]/div[4]/div[2]/cu-custom-field/cu-edit-task-custom-field-value/cu-edit-task-dropdown-custom-field-value/div/div"))
    )
    site_name_field.click()
    time.sleep(1.5)
    site_name_field_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cu-select__search"))
    )
    site_name_field_2.click()
    site_name_field_2.send_keys(site_name)
    time.sleep(0.5)
    site_name_field_2.send_keys(Keys.RETURN)

    #TYPE
    type_field = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/cu-app-shell/cu-manager/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div[2]/div[2]/div/cu-task-custom-fields/div/section/div[1]/div[5]/div[2]/cu-custom-field/cu-edit-task-custom-field-value/cu-edit-task-dropdown-custom-field-value/div/div"))
    )
    type_field.click()

    time.sleep(1.5)
    type_field_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cu-select__search"))
    )
    type_field_2.click()
    type_field_2.send_keys(ticket_type)
    time.sleep(0.5)
    type_field_2.send_keys(Keys.RETURN)

    #LOGGED TIME
    logged_time_field = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/cu-app-shell/cu-manager/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div[2]/div[2]/div/cu-task-custom-fields/div/section/div[1]/div[7]/div[2]/cu-custom-field/cu-edit-task-custom-field-value"))
    )
    logged_time_field.click()

    time.sleep(2)
    logged_time_field_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cu-date-nlp-input__input"))
    )
    logged_time_field_2.click()
    logged_time_field_2.send_keys(time_logged)
    time.sleep(2.5)
    logged_time_field_2.send_keys(Keys.RETURN)
    logged_time_field_2.send_keys(Keys.ESCAPE)

    #STATUS
    status_field = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/cu-app-shell/cu-manager/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div[2]/div[2]/div/cu-task-custom-fields/div/section/div[1]/div[9]/div[2]/cu-custom-field/cu-edit-task-custom-field-value/cu-edit-task-dropdown-custom-field-value/div/div"))
    )
    status_field.click()

    time.sleep(1.5)
    status_field_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cu-select__search"))
    )
    status_field_2.click()
    status_field_2.send_keys(ticket_status)
    time.sleep(0.5)
    status_field_2.send_keys(Keys.RETURN)

    #PROGRESS
    progress_field = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/cu-app-shell/cu-manager/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div[2]/div[2]/div/cu-task-custom-fields/div/section/div[1]/div[6]/div[2]/cu-custom-field/cu-edit-task-custom-field-value/cu-edit-task-dropdown-custom-field-value/div/div"))
    )
    progress_field.click()

    time.sleep(1.5)
    progress_field_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cu-select__search"))
    )
    progress_field_2.click()
    progress_field_2.send_keys(progress)
    time.sleep(0.5)
    progress_field_2.send_keys(Keys.RETURN)

    #RESOLUTION TIME
    resolution_time_field = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/cu-app-shell/cu-manager/cu-create-task-draft/cu-create-task-draft-lazy/cu-draft-view/div[2]/div[2]/div/cu-task-custom-fields/div/section/div[1]/div[2]/div[2]/cu-custom-field/cu-edit-task-custom-field-value/cu-custom-field-type-date/div/div"))
    )
    resolution_time_field.click()

    time.sleep(2)
    resolution_time_field_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cu-date-nlp-input__input"))
    )
    resolution_time_field_2.click()
    resolution_time = randomise_resolution_time()
    
    resolution_time_field_2.send_keys(resolution_time)
    time.sleep(2.5)
    resolution_time_field_2.send_keys(Keys.RETURN)
    resolution_time_field_2.send_keys(Keys.ESCAPE)

    


    #CREATE TASK
    create_task_button = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cu-draft-view__submit"))
    )
    create_task_button.click()

    #time.sleep(5)
    #element = WebDriverWait(driver, 10).until(
    #        EC.presence_of_element_located((By.XPATH, f"//span[text()='{task_name}']"))
    #    )
    #element.click()
    time.sleep(1.5)
    new_task_created_button = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".toast__view-button-link"))
    )
    new_task_created_button.click()
    time.sleep(1.5)
    new_dropdown_time = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/cu-task-keeper/cu-manager-view-task/div[2]/div/div/aside/div[2]/div[2]/div[2]/div[2]/div[2]/cu-time-tracking-dropdown"))
    )
    new_dropdown_time.click()
    
    time.sleep(0.5)
    new_dropdown_time_manual = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.cu-time-tracking-dropdown__option:nth-child(2)"))
    )
    new_dropdown_time_manual.click()
    random_minutes_str = str(random_minutes) + " m"
    timespent_inptut = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[9]/div[2]/div/div/div/div[2]/cu-time-tracker-create-manual/div/div[1]/cu-time-estimates-input/div[1]/input"))
    )
    timespent_inptut.click()
    timespent_inptut.send_keys(random_minutes_str)
    timespent_inptut.send_keys(Keys.RETURN)

    
    new_task_close_button = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/cu-task-keeper/cu-manager-view-task/div[2]/div/div/aside/div[1]/div[1]/div[1]/div"))
    )
    new_task_close_button.click()
    new_task_close_button_input = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[9]/div[2]/div/div/cu-status-list/div/div[1]/input"))
    )
    new_task_close_button_input.click()
    new_task_close_button_input.send_keys("Closed")
    
    input("Press Enter to continue...")
    
    
def log_a_PMS_ticket():
     
    try:
    # Trying to locate the element with visibility check
        quick_create_task_button = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/cu-app-shell/cu-manager/cu-float-button/div/div[2]/div[1]"))
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
    navigate_to_pms_url(driver, random_site['url'])
    restart_and_resync_pms_interface_on_GUI(driver)
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




