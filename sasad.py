from selenium import webdriver
from selenium.webdriver.common.alert import Alert
import time
import datetime
import random
# import sys
# import os

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')

# driver = webdriver.Chrome(os.path.join(sys._MEIPASS, "chromedriver.exe"), options=options) # pyinstaller
driver = webdriver.Chrome("chromedriver", options=options)
driver.get("https://sasadomi.hs.kr/account/login.php")
driver.implicitly_wait(3)
driver.find_element_by_id('idInput').send_keys(input("id를 입력하시오 : "))
driver.find_element_by_id('pwInput').send_keys(input("pw를 입력하시오 : "))

print("날짜는 1945-08-15와 같이 입력하시오.")
td = st_date = datetime.datetime.strptime(input("시작 날짜 : "), "%Y-%m-%d")
nd_date = datetime.datetime.strptime(input("끝날 날짜 : "), "%Y-%m-%d")
driver.execute_script("login();")
time.sleep(1)

driver.get("https://sasadomi.hs.kr/study/list.php")
driver.implicitly_wait(20)

for _ in range((nd_date - st_date).days + 1):
    driver.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/button').click()
    time.sleep(0.5)
    date_ele = driver.find_element_by_xpath('//*[@id="dateText"]')
    driver.execute_script("arguments[0].setAttribute('value','{}')".format(td.strftime('%Y-%m-%d')), date_ele)
    driver.find_element_by_xpath('//*[@id="timeSelect"]/option[5]').click()
    driver.find_element_by_xpath('//*[@id="reasonSelect"]/option[2]').click()
    driver.find_element_by_xpath('//*[@id="reasonText"]'). \
        send_keys(random.choice(['생명과학 세미나', '화학 세미나', '수학 세미나', '대학 입시']) + ' ' +
                  random.choice(['공부를 더 하기 위해서', '공부가 밀려서', '보충하기 위해서']))
    driver.execute_script("apply();")
    time.sleep(0.5)
    Alert(driver).accept()
    td += datetime.timedelta(1)
