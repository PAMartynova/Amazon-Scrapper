import scrapy
from scrapy import Request
from ..items import AmazonItem
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options



class AmazonScraper(scrapy.Spider):
    """Spider for scrapy Amazon. Section with new releases in office section"""
    # define the spider's name
    name = 'amazon'

    def start_requests(self):
        # list of URLs to scrape
        urls = [
        'https://www.amazon.in/gp/new-releases/office/ref=zg_bsnr_pg_2?ie=UTF8&pg=1',
        'https://www.amazon.in/gp/new-releases/office/ref=zg_bsnr_pg_2?ie=UTF8&pg=2']

        # set options for the Firefox webdriver
        options = Options()
        options.headless = True
        options.binary = FirefoxBinary("C:/Program Files/Mozilla Firefox/firefox.exe")

        # create a service for the Firefox webdriver
        service = FirefoxService(executable_path="../geckodriver.exe")

        # create a Firefox webdriver instance
        driver = webdriver.Firefox(service=service, options=options)

        # iterate over the URLs
        for url in urls:

            # navigate to the URL
            driver.get(url)

            # scroll down the page and wait
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)

            # find the product elements on the page
            items = driver.find_elements(By.ID, "gridItemRoot")

            # iterate over the products
            for item in items:

                # find the link element for the each product
                path = item.find_element(By.CSS_SELECTOR, ".a-link-normal").get_attribute('href')

                # yield a request to the link with a callback to the page_parse method
                yield Request(path, callback=self.page_parse)
        

    # define the method for parse each product page
    def page_parse(self, response):
        
        # create an instance of the AmazonItem class
        item = AmazonItem()

        # extract product specifications
        item['name'] = response.css("#productTitle::text").get().strip()
        item['price'] = response.css(".a-price-whole::text").get(default='Unknown')

        purch = response.css("#acrCustomerReviewText::text").get()
        item['ratings'] = purch.split()[0] if purch else 0

        table = response.css("#productDetails_techSpec_section_1 .a-size-base::text").getall()
        dic = dict(zip(table[::2], table[1::2]))
        item['country'] = dic.get(' Country of Origin ', 'Unknown')


        yield item


        