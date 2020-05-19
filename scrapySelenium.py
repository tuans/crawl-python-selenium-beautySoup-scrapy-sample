import scrapy
from selenium import webdriver


class ProductSpider(scrapy.Spider):
    search = "Lavender"
    name = 'lazada_crawler'
    allowed_domains = ['www.lazada.vn']
    BASE_URL = r"http://www.lazada.vn/catalog/?q=lavender&price=1000000-99000000"
    start_urls = [BASE_URL.format(search=search)]
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='./libs/chromedriver')  

    def parse(self, response):
        self.driver.get(response.url)
        while True:
            next = self.driver.find_element_by_xpath("//li[contains(@class,'ant-pagination-next')]//a[@class='ant-pagination-item-link']")
            try:
                next.click()
                # get the data and write it to scrapy items
            except:
                break
        self.driver.close()