from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def get_chrome_driver(headless=True):
    # define webdrive in chrome
    options = webdriver.ChromeOptions()
    options.headless = headless
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver
