from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import UnexpectedAlertPresentException


class hangUp():

    def __init__(self, username, passwd, needtime):

        self.username = username
        self.password = passwd
        self.needtime = int(needtime)
        self.chrome_options = Options()
        self.browser = webdriver.Chrome(options=self.chrome_options)
        self.browser.get('http://192.168.9.12/npels/')
        self.wait = WebDriverWait(self.browser, 60)
        self.n = 1
        self.time = 0
        self.num = 1
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

        except TimeoutError:
            return self.intopage()
        except UnexpectedAlertPresentException:
            print('用户或密码错误')
            self.browser.quit()
            quit(-1)
        else:
            print('登陆成功~')

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

            print('当前时间', int(time.time()) - self.time , '\t当前已经挂了',self.num,'节课了')
            try:
                mess = self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '#frameless > div.tcontent > div > input[type="button"]'))).click()
                if mess != None:
                    self.action.move_to_element_with_offset(mess, 2, 1).click().perform()  # 点击按钮偏移量, 防检测
            except:
                pass
            else:
                print('检测到弹窗')
            if int(time.time()) - self.time > self.needtime:
                print('时间到了, 切换下一课')
                self.num += 1
                break

if __name__ == '__main__':

    hangUp(input('username: '), input('passwd: '), input('time: '))
