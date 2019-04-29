from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
import time
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains


class hangUp():
    browser = webdriver.Chrome()
    browser.get('http://192.168.9.12/npels/')
    wait = WebDriverWait(browser, 10)

    def __init__(self, username, passwd):
        self.username = username
        self.password = passwd
        self.time = 0
        self.login()
        self.intopage()

    def login(self):
        hangUp.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tbName'))).send_keys(self.username)
        hangUp.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tbPwd'))).send_keys(self.password)
        hangUp.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#btnLogin'))).click()

    def intopage(self):

        try:
            hangUp.browser.switch_to.frame('mainFrame')
            start = hangUp.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 '#aspnetForm > div.content > div.main_right > div:nth-child(2) > div > div.class_container > div > ul:nth-child(2) > a')))

            start.click()
            sleep(1)
            hangUp.wait.until(EC.presence_of_element_located((By.LINK_TEXT,
                                                              '继续学习'))).click()
            sleep(1)
            self.testCompletion()
        except TimeoutError:
            return self.intopage()

    def testCompletion(self):
        print('开始学习了哦~')
        self.time = int(time.time())
        self.closeMessage()
        while True:
            sleep(5)
            print('当前时间', int(time.time()) - self.time)
            if int(time.time()) - self.time > 5:
                try:
                    hangUp.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#frameless > div.tcontent > div > input[type="button"]')))
                except:
                    print('没有检测到弹窗')
                print('时间到了, 切换下一课')
                break
        self.aNext()

    def aNext(self):

        nextP = hangUp.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#aNext')))
        try :
            nextP.click()
        except:
            return self.aNext()
        print('切换成功了~')
        self.testCompletion()

    def closeMessage(self):
        js = '''
                 function CheckActive() {

                if (!isMaterialStudy && !isAssistStudy)
                    return;

                var d = new Date();
                if (d.getTime() - latestMoveTime > 2800 * 1000) 
                {         
                    clearInterval(actTimerID);       
                    clearInterval(secTimerID);
                    EndStatTime();            
                    Leave();
                }
            }
            var actTimerID = window.setInterval("CheckActive();", 5000);
        function Leave()
            {
                var msg = GetRandomWord();
                var loadingInfo = '<div class="leaveMsg" ><div>提示：</div><br/>'+"到點了，該切換到下一課啦"+'<input type="button" value="OK" onclick="TINY.box.hide();"/></div>';
                TINY.box.show({html:loadingInfo,mask:true,animate:false,close:true,boxid:'frameless',closejs:function(){LeaveBack()}});
            }
                '''

        self.browser.execute_script(js)


if __name__ == '__main__':
    hangUp('x', 'x')
