from profile import Profile
from oven import Oven
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
import time
import os
from datetime import datetime
import random

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
    wait = WebDriverWait(driver, 20)

bases = os.listdir("./bases")

def send_whatsapp(phone_no):
    driver.get(
        f"https://web.whatsapp.com/send?phone=+55{phone_no}"
    )

def comercial_whatsapp():
        for profile_number in range(1, len(bases) + 1):
            
            logged = False
            whats_profile = Profile(profile_number)
            contact_number = whats_profile.contact_number
            contact_name = whats_profile.contact_name
            messages = whats_profile.message
            image = whats_profile.image

            try:
                open_whatsapp(profile_number)
            except:
                break
            
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='chat-list']")))
                logged = True
                
            except:
                print(f"hey, the profile {profile_number} isn't sync. Please, connect it to keep sending messages")

            if logged:
            
                try:
                    send_whatsapp(contact_number)
                
                    try:
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'O número de telefone compartilhado através de url é inválido.')]")))
                        print('O número de telefone compartilhado através de url é inválido.')
                        driver.close()
                        whats_profile.invalid_number()
                        break
                
                    except Exception as e:
                        
                        print("Number accepted")

                        for message in messages:
                            try:
                                message = eval(f'f"""{message}"""')
                                mensagem = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@title, 'Mensagem')]")))
                                mensagem.send_keys(message)
                                send = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-testid='send']")))
                                send.click()
                            except Exception as e:
                                action.send_keys(Keys.ENTER).perform()
                                wait.until(EC.alert_is_present())
                                alert = driver.switch_to.alert
                                alert.accept()
                                action.send_keys(Keys.ENTER).perform()
                    
                except Exception as e:
                    action.send_keys(Keys.ENTER).perform()  
                    print(e)

                if image:
                    clip = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-testid='clip']")))
                    clip.click()
                    media = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input")))
                    time.sleep(1)
                    media.send_keys(image)
                    enviar = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-testid='send']")))
                    enviar.click()

                # whats_profile.increase_index()
                random_time = random.randrange(0,6)
                time.sleep(20+random_time)
                driver.close()
                
                

def oven():
        for profile_number in range(1, len(bases) + 1):
            
            os.system('cls')
                      
            logged = False
            whats_profile = Oven(profile_number)
            contact_number = whats_profile.contact_number
            messages = whats_profile.message
            
            
            try:
                open_whatsapp(profile_number)
            except:
                break
            
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='chat-list']")))
                logged = True
                
            except:
                print(f"hey, the profile {profile_number} isn't sync. Please, connect it to keep sending messages")

            if logged:
            
                try:
                    send_whatsapp(contact_number)
                
                    try:
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'O número de telefone compartilhado através de url é inválido.')]")))
                        print('O número de telefone compartilhado através de url é inválido.')
                        driver.close()
                        whats_profile.invalid_number()
                        break
                
                    except Exception as e:
                        
                        print("Number accepted")

                        for message in messages:
                            try:
                                mensagem = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@title, 'Mensagem')]")))
                                mensagem.send_keys(message)
                                send = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-testid='send']")))
                                send.click()
                            except Exception as e:
                                action.send_keys(Keys.ENTER).perform()
                                wait.until(EC.alert_is_present())
                                alert = driver.switch_to.alert
                                alert.accept()
                                action.send_keys(Keys.ENTER).perform()
                    
                except Exception as e:
                    action.send_keys(Keys.ENTER).perform()  
                    print(e)

                # whats_profile.increase_index()
                random_time = random.randrange(0,6)
                time.sleep(20+random_time)
                driver.close()

def should_run():
    if datetime.now().hour >=8 and datetime.now().hour<= 18 and datetime.now().weekday() <= 4:
        return True
        
while True:
    play = should_run()
    if play:
        print('Horário comercial')
        comercial_whatsapp()
    else:
        print('Aquecimento')
        oven()




