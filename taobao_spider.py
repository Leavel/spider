import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
def search():
    browser.get('https://www.taobao.com/')
    _input = wait.until(EC.presence_of_element_located((By.ID,'q')))
    _input.send_keys('美食')#J_SearchForm > button
    _input.send_keys(Keys.ENTER)

def main():
    search()

if __name__ == '__main__':
    main()