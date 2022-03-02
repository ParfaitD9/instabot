import json
import os
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random as rd
from bs4 import BeautifulSoup
import sqlite3
from utils.orm import insert_followers, update_user


class Crawler:
    def __init__(self, auth= False) -> None:
        if auth:
            opts = webdriver.ChromeOptions()
            #opts.add_argument('--headless')
            opts.add_argument('--disable-dev-shm-usage')
            opts.add_argument('--no-sandbox')
            opts.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
            s = Service(executable_path= os.environ.get('CHROMEDRIVER_PATH'))
            self.browser = webdriver.Chrome(executable_path= os.environ.get('CHROMEDRIVER_PATH'), chrome_options= opts)
            self.auth('canurap1@gmail.com', 'Test12345')
            self.connected = True
        else:
            with open('session.json') as r:
                d : dict = json.load(r)
                self.browser = webdriver.Remote(command_executor= d.get('url'), desired_capabilities= {})
                self.browser.session_id = d.get('session')
            
            self.connected = True
        
    def auth(self, user, pwd):
        try:
            self.browser.get('https://instagram.com')
            time.sleep(rd.randrange(2,4))

            input_username = self.browser.find_element(By.NAME, 'username')
            input_password = self.browser.find_element(By.NAME, 'password')

            input_username.send_keys(user)
            time.sleep(rd.randrange(1,2))
            input_password.send_keys(pwd)
            time.sleep(rd.randrange(1,2))
            input_password.send_keys(Keys.ENTER)
            
        except Exception as err:
            print(err)
            self.browser.quit()
        else:
            try:
                self.current_url, self.session_id = self.browser.command_executor._url, self.browser.session_id
            except Exception as e:
                print(e)
            else:
                with open('session.json', 'w') as w:
                    d = {
                        'url' : self.current_url,
                        'session' : self.session_id
                    }
                    json.dump(d, w)
                try:
                    m = WebDriverWait(self.browser, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a'))
                    )
                    try:
                        accept_cookies = self.browser.find_element(By.XPATH, '/html/body/div[4]/div/div/button[2]')
                    except NoSuchElementException as e:
                        print('Not cookies asking found')
                    else:
                        accept_cookies.click()
                    finally:
                        m.click()
                except TimeoutException as e:
                    print('Timeout ...')
                except Exception as e:
                    print(e.args[0])
                else:
                    try:
                        deny_notif = WebDriverWait(self.browser, 5).until(
                            EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div/div[3]/button[2]'))
                        )
                    except TimeoutException as e:
                        print('Notifications not asked')
                    except Exception as e:
                        print(f'{e.__class__} : {e.args[0]}')
                    else:
                        deny_notif.click()

                    print('SUCCESS')
    
    def followers_size(self, qte : str):
        re.match('?P<qte>[\d+,]')
        pass
    
    def send_message(self, user, message):
        try:
            print(self.browser.session_id)
            
            
            time.sleep(rd.randrange(1,2))
            self.browser.find_element(By.XPATH, '/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[1]/div/div[3]/button').click()
            
            time.sleep(rd.randrange(1,2))
            self.browser.find_element(By.XPATH, '/html/body/div[6]/div/div/div[2]/div[1]/div/div[2]/input').send_keys(user)
            time.sleep(rd.randrange(2,3))
            
            self.browser.find_element(By.XPATH, '/html/body/div[6]/div/div/div[2]/div[2]/div/div')
            
            self.browser.find_element(By.XPATH, '/html/body/div[6]/div/div/div[2]/div[2]').find_element(By.TAG_NAME, 'button').click()
            
            print('Click executed')
            
            time.sleep(rd.randrange(3,4))
            self.browser.find_element(By.XPATH, '/html/body/div[6]/div/div/div[1]/div/div[2]/div/button').click()
            time.sleep(rd.randrange(3,4))
            text_area = self.browser.find_element(By.XPATH, '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
            text_area.send_keys(message)
            time.sleep(rd.randrange(2,4))
            text_area.send_keys(Keys.ENTER)
            update_user(user)
            print(f'Message successfully sent to {user}')
            time.sleep(1)
        except Exception as e:
            print(e)
            return {'status' : False, 'message' : e.args[0]}
        else:
            return {'status' : True, 'message' : f'Message successfully sent to {user}'}

    def send_mass_message(self, users : list, message):
        self.browser.get('https://www.instagram.com/direct/inbox')
        try:
            WebDriverWait(self.browser, 7).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[1]/div/div[3]/button'))
            )
        except TimeoutException as e:
            print(e.args[0])
            return {
                'status' : False,
                'message' : e.args[0]
            }
        except Exception as e:
            print(e.args[0])
            return {
                'status' : False,
                'message' : e.args[0]
            }
        else:
            for i, user in enumerate(users[:5]):
                try:
                    self.send_message(user, message)
                except Exception as e:
                    print(f'{e.__class__} : {e}')
                    break
                else:
                    time.sleep(3)
            
            return {
                'status' : True,
                'message' : f'{i} users pinned'
            }
    
    def get_followers(self, username):
        self.browser.get('https://www.instagram.com/{}/'.format(username))
        time.sleep(3)
        
        self.browser.find_element(By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[2]').click()

        div = WebDriverWait(self.browser, 15).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div/div[2]/ul/div/li[1]'))
        )

        for j in range(2):
            self.browser.execute_script(
                f'''
                let ul = document.querySelector('div.isgrP');
                
                ul.scroll({j}*ul.scrollHeight, {j}*ul.scrollHeight + ul.scrollHeight);
                '''
            )
            print('Scroll', j)
            
            time.sleep(2)
        
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        follow = soup.find_all('li')
        data : list[str] = [fol.get_text() for fol in follow if follow][3:]
        data = [fol.strip("S'abonner").split(maxsplit= 1)[0] for fol in data if fol]
        self.browser.find_element(By.XPATH, '/html/body/div[6]/div/div/div/div[1]/div/div[2]/button').click()

        self.browser.find_element(By.XPATH, '/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a').click()
        try:
            WebDriverWait(self.browser, 15).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div/div[3]/div/button'))
            )
        except TimeoutException:
            print('Timeout')

        print(len(data), 'followers found')

        r = insert_followers(data)

        return {'status' : True, 'data' : data, 'message' : r.get('message')}

    def send_messages(self):
        msg_btn = self.browser.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a/svg/polygon')
        msg_btn.click()
    
    def logout(self):
        try:
            pro = self.browser.find_element(By.XPATH, '/html/body/div[1]/section/div/div[1]/div/div[3]/div/div[6]/span')
        except NoSuchElementException as e:
            print('Profile not found')
            return False
        else:
            pro.click()
            try:
                deconnect = self.browser.find_element(By.XPATH, '/html/body/div[1]/section/div/div[1]/div/div[3]/div/div[6]/div[2]/div[2]/div[2]/div[2]')
            except NoSuchElementException as e:
                print('Deconnexion button not found')
                return False
            else:
                deconnect.click()
                self.connected = False
        
        return True
    
    def deinit(self):
        self.browser.close()

if __name__ == '__main__':
    c = Crawler(auth= True)
