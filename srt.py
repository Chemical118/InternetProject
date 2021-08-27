import os
import sys
import telegram
from time import sleep
from selenium import webdriver
import datetime
from selenium.webdriver.common.alert import Alert

try_list = [1, 0, 0, 1, 1, 1, 1, 1] # 시도할 위치를 직접 선택하 수 있습니다. (1이 되면 확인히지 않음)
bot = telegram.Bot(token="") # telegram token을 입력하세요
chat_id = 0  # telegram id를 입력하세요
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
if getattr(sys, 'frozen', False):
    chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
    driver = webdriver.Chrome(chromedriver_path, options=options)
else:
    driver = webdriver.Chrome(options=options)
driver.get('https://etk.srail.co.kr/cmc/01/selectLoginForm.do')
driver.implicitly_wait(15)
print("날짜는 1945-08-15와 같이 입력하시오.")
rd = datetime.datetime.strptime(input("시작 날짜 : "), "%Y-%m-%d")
driver.find_element_by_id('srchDvNm01').send_keys(input("id를 입력하세요 : "))
driver.find_element_by_id('hmpgPwdCphd01').send_keys(input("비밀번호를 입력하세요 : "))
driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[1]/div[1]/div[2]/div/div[2]/input').click()
driver.implicitly_wait(4)
sleep(0.4)
driver.find_element_by_xpath('//*[@id="dptRsStnCd"]/option[6]').click()
driver.implicitly_wait(5)
driver.find_element_by_xpath('//*[@id="arvRsStnCd"]/option[2]').click()
sleep(0.4)
driver.find_element_by_xpath('//*[@id="dptTm"]/option[9]').click()
driver.implicitly_wait(1)
date_ele = driver.find_element_by_xpath('//*[@id="search-form"]/fieldset/div[3]/div/input[1]')
driver.execute_script("arguments[0].setAttribute('value','{}')".format(rd.strftime('%Y-%m-%d')), date_ele)
driver.implicitly_wait(1)
driver.find_element_by_xpath('//*[@id="search-form"]/fieldset/a').click()
t = 1
while True:
    sleep(3)
    t -= 1
    if t == 0:
        t = 200
        bot.sendMessage(chat_id=chat_id, text="현재실행중입니다")
    for i in range(len(try_list)):
        xpath = '//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[' + str(i + 2) + ']/td[7]'
        if driver.find_element_by_xpath(xpath + '/a/span').text != "매진" and not try_list[i]:
            driver.find_element_by_xpath(xpath + '/a').click()
            sleep(2)
            driver.find_element_by_xpath('//*[@id="list-form"]/fieldset/div[11]/a[1]').click()
            bot.sendMessage(chat_id=chat_id, text=(str(i + 1) + "번째 예약성공"))
            try_list[i] = 1
            driver.get("https://etk.srail.kr/main.do")
            sleep(0.6)
            driver.find_element_by_xpath('//*[@id="dptRsStnCd"]/option[6]').click()
            driver.implicitly_wait(5)
            driver.find_element_by_xpath('//*[@id="arvRsStnCd"]/option[2]').click()
            sleep(0.6)
            driver.find_element_by_xpath('//*[@id="dptTm"]/option[9]').click()
            driver.implicitly_wait(1)
            date_ele = driver.find_element_by_xpath('//*[@id="search-form"]/fieldset/div[3]/div/input[1]')
            driver.execute_script("arguments[0].setAttribute('value','{}')".format(rd.strftime('%Y-%m-%d')), date_ele)
            driver.implicitly_wait(1)
            driver.find_element_by_xpath('//*[@id="search-form"]/fieldset/a').click()
            sleep(2)
    sleep(25)
    driver.get("https://etk.srail.kr/main.do")
    sleep(0.6)
    driver.find_element_by_xpath('//*[@id="dptRsStnCd"]/option[6]').click()
    driver.implicitly_wait(5)
    driver.find_element_by_xpath('//*[@id="arvRsStnCd"]/option[2]').click()
    sleep(0.6)
    driver.find_element_by_xpath('//*[@id="dptTm"]/option[9]').click()
    driver.implicitly_wait(1)
    date_ele = driver.find_element_by_xpath('//*[@id="search-form"]/fieldset/div[3]/div/input[1]')
    driver.execute_script("arguments[0].setAttribute('value','{}')".format(rd.strftime('%Y-%m-%d')), date_ele)
    driver.implicitly_wait(1)
    driver.find_element_by_xpath('//*[@id="search-form"]/fieldset/a').click()
