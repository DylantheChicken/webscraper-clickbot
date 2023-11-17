import random
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

def random_mac_address():
    # List of allowed hexadecimal characters for MAC address
    hex_chars = "0123456789ABCDEF"

    # Generate each pair of the MAC address and join them with ':'
    mac_address = ":".join(
        "".join(random.choice(hex_chars) for _ in range(2)) for _ in range(6)
    )

    return mac_address

def load_sitesList_json_file():
    with open('C:\\Users\\Dylan\\source\\repos\\Python-Automatic-Login-and-Call-Logger\\sitesList.json', 'r') as file:
        data = json.load(file)
        return data['sites']

def load_problems_json_file():
    with open('C:\\Users\\Dylan\\source\\repos\\Python-Automatic-Login-and-Call-Logger\\reactive-problems.json', 'r') as file:
        data = json.load(file)
        return data['reactive-problems']


