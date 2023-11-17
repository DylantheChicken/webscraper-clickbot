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
    random_mac_address
)

from Python_Automatic_Login_and_Call_Logger import (
    randomize_resolution_time
    )


