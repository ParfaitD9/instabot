import json
import re
import sqlite3
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random as rd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, auth= False) -> None:
        if auth:
            s = Service('/home/parfait/Logs/chromedriver')
            #service_args= ['--proxy=localhost:9150', '--proxy-type=sock5']
            self.browser = webdriver.Chrome()
            self.auth('canurap1@gmail.com', 'Test12345')
        else:
            with open('session.json') as r:
                d : dict = json.load(r)
                self.browser = webdriver.Remote(command_executor= d.get('url'), desired_capabilities= {})
                self.browser.session_id = d.get('session')
        
    
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
                m = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a'))
                )
                m.click()
                print('SUCCESS')
    
    def followers_size(self, qte : str):
        re.match('?P<qte>[\d+,]')
        pass

    def send_message(self, user, message):
        try:
            print(self.browser.session_id)
            
            time.sleep(rd.randrange(1,2))
            self.browser.find_element(By.XPATH, '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div/div[3]/div/button').click()
            
            time.sleep(rd.randrange(1,2))
            self.browser.find_element(By.XPATH, '/html/body/div[6]/div/div/div[2]/div[1]/div/div[2]/input').send_keys(user)
            time.sleep(rd.randrange(2,3))
            self.browser.find_element(By.XPATH, '/html/body/div[6]/div/div/div[2]/div[2]/div[1]').find_element(By.TAG_NAME, 'button').click()
            
            time.sleep(rd.randrange(3,4))
            self.browser.find_element(By.XPATH, '/html/body/div[6]/div/div/div[1]/div/div[2]/div/button').click()
            time.sleep(rd.randrange(3,4))
            text_area = self.browser.find_element(By.XPATH, '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
            text_area.send_keys(message)
            time.sleep(rd.randrange(2,4))
            text_area.send_keys(Keys.ENTER)
            print(f'Message successfully sent to {user}')
            time.sleep(1)
        except Exception as e:
            print(e)
            return {'status' : False, 'message' : e.args[0]}
        else:
            return {'status' : True, 'message' : f'Message successfully sent to {user}'}
        

    def get_followers(self, username):
        self.browser.get('https://www.instagram.com/{}/'.format(username))
        time.sleep(3)
        
        self.browser.find_element(By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/div').click()

        div = WebDriverWait(self.browser, 15).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div/div[2]/ul/div/li[1]'))
        )

        for j in range(10):
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

        print(len(data), 'followers found')

        r = self.insert_followers(data)

        return {'status' : True, 'data' : data, 'message' : r.get('message')}

    def insert_followers(self, followers):
        try:
            con = sqlite3.connect('src/database.db3')
            cur = con.cursor()

            cur.executemany('INSERT INTO users (username) VALUES (?)', [(follower,) for follower in followers])
        except sqlite3.IntegrityError as e:
            print(e)
            r = {'status' : True, 'message' : 'User already exists'}
        except Exception as e:
            print(f'{e.__class__} : {e}')
            con.rollback()
            r = {'status' : False, 'message' : e.args[0]}
        else:
            print('Insertion done')
            con.commit()
            r = {'status' : True, 'message' : 'Insertion done'}
        finally:
            cur.close()
            con.close()

            return r

    def send_messages(self):
        msg_btn = self.browser.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a/svg/polygon')
        msg_btn.click()
        
    def deinit(self):
        self.browser.close()

if __name__ == '__main__':
    c = Crawler(auth= True)
