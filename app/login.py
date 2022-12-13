from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote


def open_whatsapp(profile_number):
    global driver
    global action
    global wait
    options = webdriver.ChromeOptions()
    options.add_argument(
        f"user-data-dir=C:\\Users\\user\\AppData\\Local\\Google\\Chrome\\User Data\\Profile {profile_number}"
    )
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    action = ActionChains(driver)
    driver.get(f"https://web.whatsapp.com")

def main():
   profile_number = input('insert the number of login you want to sync')
   open_whatsapp(profile_number)
   input("press enter when its logged")
   driver.close()

main()