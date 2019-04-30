from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
from random import randint
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains


class hangUp():

    def __init__(self, username, passwd):

        self.username = username
        self.password = passwd
        self.chrome_options = Options()
        # 设置chrome浏览器无界面模式
        self.chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=self.chrome_options)
        self.browser.get('http://192.168.9.12/npels/')
        self.wait = WebDriverWait(self.browser, 10)
        self.n = 1
        self.time = 0
        self.login()
        self.intopage()
        self.action = ActionChains(self.browser)

    def login(self):

        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tbName'))).send_keys(self.username)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tbPwd'))).send_keys(self.password)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#btnLogin'))).click()

    def intopage(self):

        try:
            self.browser.switch_to.frame('mainFrame')

            try:
                if self.browser.find_element_by_css_selector(
                        'li.progress_' + str(
                            self.n) + '>span').value_of_css_property('width') == '222px':
                    self.n += 1
            except:
                self.browser.quit()

            start = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 '#aspnetForm > div.content > div.main_right > div:nth-child(2) > div > div.class_container > div > ul:nth-child(' + str(
                     self.n) + ') > a')))

            start.click()
            sleep(1)

            self.wait.until(EC.presence_of_element_located((By.LINK_TEXT,
                                                            '继续学习'))).click()
            sleep(1)
            self.testCompletion()
        except TimeoutError:
            return self.intopage()

    def testCompletion(self):
        print('开始学习了哦~')
        self.time = int(time.time())
        self.closeMessage()
        self.aNext()

    def aNext(self):
        self.browser.switch_to.frame('mainFrame')
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#aNext'))).click()

        except:
            print('没了哦~')
            self.browser.quit()
        print('切换成功了~')
        self.testCompletion()

    def closeMessage(self):
        self.browser.switch_to.default_content()  # 切换回主布局
        while True:

            print('当前时间', int(time.time()) - self.time)
            try:
                mess = self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '#frameless > div.tcontent > div > input[type="button"]'))).click()
                if mess != None:
                    self.action.move_to_element_with_offset(mess, 2, 1).click().perform()  # 点击按钮偏移量, 防检测
            except:
                pass
            else:
                print('检测到弹窗')
            if int(time.time()) - self.time > 1080:
                print('时间到了, 切换下一课')
                break


if __name__ == '__main__':
    hangUp('username', 'passwd')
