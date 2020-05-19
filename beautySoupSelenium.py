from seleniumUtils import *
from bs4 import BeautifulSoup



try:
    withChrome(True)

    gotoURL("https://lazada.vn")
    # pause(2)
    mySendKey("//input[@id='q']", "lavender")
    myClick("//button[@class='search-box__button--1oH7']")
    # pause(2)
    #//div[@class='c1_t2i']//div[@class='c5TXIP']
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    products = soup.find_all('div', class_='c16H9d')
    for product in products:
        a_link = product.find('a', href=True)
        print(a_link)



finally:
    if (driver != None):
      driver.quit()