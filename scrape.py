from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from funcs import run_app
from consts import LINK

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

run_app(driver, LINK)