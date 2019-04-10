from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
import time


class hangUp():
    browser = webdriver.Chrome()
    browser.get('http://192.168.9.12/npels/')
    wait = WebDriverWait(browser, 10)

    def __init__(self, username, passwd):
        self.username = username
        self.password = passwd
        self.time = 0

    def login(self):
        hangUp.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tbName'))).send_keys(self.username)
        hangUp.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tbPwd'))).send_keys(self.password)
        hangUp.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#btnLogin'))).click()

    def intopage(self):
        try:
            hangUp.browser.switch_to.frame('mainFrame')
            start = hangUp.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 '#aspnetForm > div.content > div.main_right > div:nth-child(2) > div > div.class_container > div > ul:nth-child(1) > a')))
            start.click()
            sleep(1)
            hangUp.wait.until(EC.presence_of_element_located((By.LINK_TEXT,
                                                              '继续学习'))).click()
            sleep(1)
            self.time = int(time.time())
        except TimeoutError:
            return self.intopage()


    def aNext(self):
        if int(time.time()) - self.time > 2400:
            nextP = hangUp.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#aNext')))
            nextP.click()

    def closeMessage(self):
        try:
            self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#frameless > div.tcontent > div > input[type="button"]'))).click()
        except TimeoutError:
            return self.closeMessage()

if __name__ == '__main__':
    my = hangUp()
    my.login()
    my.intopage()
