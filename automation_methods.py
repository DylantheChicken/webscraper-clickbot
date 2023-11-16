from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.service import Service
import os
import time
import json



def initialize_web_driver_and_ignore_ssl_warnings():
    chrome_options = Options()
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')
    return webdriver.Chrome(options=chrome_options)

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

def restart_and_resync_pms_interface_on_GUI(driver):
    # Wait for the 'Restart' button to be clickable
    restart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@value='Restart']"))
    )
    restart_button.click()
    time.sleep(15)  # Wait for 0.25 minute

    # Check for the 'Resync' button
    resync_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@value='Resync']"))
    )
    resync_button.click()

def load_sitesList_json_file():
    with open('C:\\Users\\Dylan\\source\\repos\\Python-Automatic-Login-and-Call-Logger\\sitesList.json', 'r') as file:
        data = json.load(file)
        return data['sites']

def load_problems_json_file():
    with open('C:\\Users\\Dylan\\source\\repos\\Python-Automatic-Login-and-Call-Logger\\reactive-problems.json', 'r') as file:
        data = json.load(file)
        return data['reactive-problems']


