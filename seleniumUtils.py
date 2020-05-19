
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
from selenium.common.exceptions import NoSuchElementException

from dotenv import load_dotenv
load_dotenv(dotenv_path='properties.env')
import os
import traceback


osName = os.getenv("OS")
TIME_OUT = 30
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
    
    if(osName and osName == "mac"):
        chrome_path = './libs/chromedriver_mac64'
    elif(osName and osName == "linux"):
        chrome_path = './libs/chromedriver_linux64'
    else:
        chrome_path = './libs/chromedriver'

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
    value = waitVisible(xPath).text
    if(value):
        return value.strip()
    else:
        return ""

def waitVisible(xPath):
    try:
        return wait.until(EC.presence_of_element_located((By.XPATH, xPath)))
    except:
        print("xPath", xPath)
        traceback.print_exc()

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

def isExist(xPath):
    try:
        driver.find_element_by_xpath(xPath)
    except NoSuchElementException:
        return False
    return True

def getElements(xPath):
    try:
        datas = driver.find_elements_by_xpath(xPath)
    except NoSuchElementException:
        return []
    return datas