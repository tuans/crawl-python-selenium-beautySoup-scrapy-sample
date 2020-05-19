TIME_OUT = 20
NUMBER_OF_PAGE = 3
from selenium import webdriver
import getpass
import requests
import time
from selenium.webdriver.common.keys import Keys
import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains


chrome_path = './libs/chromedriver'
driver = None
wait = None
actions = None


def withChrome(headless):
    global driver
    global wait
    global actions
    chrome_options = Options()  
    if(headless):
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--headless")
    else:
        chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(executable_path=chrome_path,   chrome_options=chrome_options)  
    wait = WebDriverWait(driver,TIME_OUT)
    actions = ActionChains(driver)
	
def gotoURL(url):
    global driver
    driver.get(url)
    
def myGetAttrFromXPath(xPath, attributeName):
    return waitVisible(xPath).get_attribute(attributeName)

def myGetAttrFromElement(element, attributeName):
    return element.get_attribute(attributeName)
	
def myGetText(xPath):
    return waitVisible(xPath).text

def waitVisible(xPath):
    return wait.until(EC.presence_of_element_located((By.XPATH, xPath)))

def mySendKey(xPath, key):
    waitVisible(xPath).send_keys(key)

def myClick(xPath):
    try:
        waitVisible(xPath).click()
    finally:
        return

def myScrollToElement(xPath):
    driver.execute_script("arguments[0].scrollIntoView();", waitVisible(xPath))

def pause(seconds):
    time.sleep(seconds)

def switchToIframe(xPath):
    driver.switch_to.frame(waitVisible(xPath))

def mySlider(xPathSliderBar, xPathSlider, percent):
    global actions
    slidebar = waitVisible(xPathSliderBar)
    height = 38
    width = 298
    slider = waitVisible(xPathSlider)
    if width > height:
        #highly likely a horizontal slider
        actions.click_and_hold(slider).move_by_offset(percent * width / 100, 0).release().perform()
    else:
        #highly likely a vertical slider
       actions.click_and_hold(slider).move_by_offset(percent * height / 100, 0).release().perform()

try:
    withChrome(True)

    gotoURL("https://lazada.vn")
    # pause(2)
    mySendKey("//input[@id='q']", "lavender")
    myClick("//button[@class='search-box__button--1oH7']")
    # pause(2)
    #//div[@class='c1_t2i']//div[@class='c5TXIP']
    products = driver.find_elements_by_xpath("//div[@class='c1_t2i']//div[@class='c5TXIP']//div[@class='c16H9d']//a[@title]")
    # print(products)
    for product in products:
        print(product.get_attribute("title"))



finally:
    if (driver != None):
      driver.quit()