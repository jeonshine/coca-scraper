import undetected_chromedriver as driver
from selenium.webdriver.common.by import By
import time

from googlesheet import connect, write 

def init_browser(url, version):
    # option for browser
    browser = driver.Chrome(version_main=version, suppress_welcome=False)
    browser.maximize_window()
    browser.implicitly_wait(10)

    # init
    browser.get(url)

    return browser

def break_into_frame(frame):
    time.sleep(1)
    frame = browser.find_element(By.XPATH, f'//frame[@name="{frame}"]')
    browser.switch_to.frame(frame)

def login():
    break_into_frame( "controller")
    browser.find_element(By.XPATH, '//a[@title="Log in"]').click()
    
    # different frame depth
    browser.switch_to.parent_frame()
    break_into_frame("x4")

    email_input = browser.find_element(By.XPATH, '//input[@name="email"]')
    email_input.send_keys(EMAIL)
    
    pw_input = browser.find_element(By.XPATH, '//input[@name="password"]')
    pw_input.send_keys(PW)

    browser.find_element(By.XPATH, '//input[@value="Log in"]').click()

def logout():
    browser.switch_to.parent_frame()
    break_into_frame( "controller")

    browser.find_element(By.XPATH, '//a[@title="Log in"]').click()

    # different frame depth
    browser.switch_to.parent_frame()
    break_into_frame("x4")

    browser.find_element(By.XPATH, '//span[@id="w_logout"]').click()

def move_to_search_tap():
    browser.switch_to.parent_frame()
    break_into_frame("controller")

    browser.find_element(By.XPATH, '//td[@id="mycell1"]').click()

def search(keyword):
    browser.switch_to.parent_frame()
    break_into_frame("x1")

    search_input = browser.find_element(By.XPATH, '//td[@id="doCell2"]//input')
    search_input.clear()
    search_input.send_keys(keyword)

    browser.find_element(By.XPATH, '//input[@name="submit1"]').click()

    # need to wait for 5 sec (minimun waiting)
    time.sleep(5) 

def scrap(keyword):
    browser.switch_to.parent_frame()
    break_into_frame("x2")

    result = []
    trs = browser.find_elements(By.XPATH, '//table[@class="auto-style1"]//tr')
    for tr in trs[1:]:
        form = tr.find_elements(By.XPATH, './/td')[3].text.strip()
        freq = tr.find_elements(By.XPATH, './/td')[4].text.strip()
        result.append([keyword, form, freq])
    
    return result

        
if  __name__  ==  "__main__" :

    # constant
    CHROME_VERSION = 106
    SPREADSHEET = "COCA"
    WORKSHEET = "collocation"

    URL = "https://www.english-corpora.org/coca/"
    EMAIL = "hojongjeon@lxper.com"
    PW = "lxper1266!"

    # google sheet
    sheets = connect(SPREADSHEET)
    worksheet = sheets.worksheet(WORKSHEET)

    # get browser
    browser = init_browser(URL, CHROME_VERSION)

    # login
    login()

    # search loop example
    counter = 1
    examples = ["allow * to", "take * for"]
    for idx, keyword in enumerate(examples):
        move_to_search_tap()
        search(keyword)
        result = scrap(keyword)
        write(worksheet, counter, result)
        
        counter += len(result)

    # logout
    logout()

    print("debug")
    browser.quit()