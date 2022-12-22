import scrapy
from ..items import MobileItem


class MobileAmazonScraper(scrapy.Spider):
    """Spider for scrapy Amazon. Section with Smartphones and Basic Mobiles, sort by Featured"""
    name = 'mobile'
    # create page variable for paggination
    page = 2

    start_urls = [
        "https://www.amazon.in/s?i=electronics&rh=n%3A1389432031%2Cp_72%3A1318476031&page=1&content-id=amzn1.sym.f5d0d3e7-fe8a-4766-96ee-1c39e69d20b3&pd_rd_r=4222e4c1-ad0f-4f56-a47b-cfd87941a0f0&pd_rd_w=zEVAz&pd_rd_wg=Nv3TC&pf_rd_p=f5d0d3e7-fe8a-4766-96ee-1c39e69d20b3&pf_rd_r=8YCV46JXH7KXBJN5TTNN&qid=1671294335&ref=sr_pg_2"
    ]

    def parse(self, response):

        # get all links to each product at the page and yield response 
        links = response.xpath("//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']/@href").getall()
        yield from response.follow_all(links, callback=self.page_parse)

        # create new URL for the next page
        new_url = "https://www.amazon.in/s?i=electronics&rh=n%3A1389432031%2Cp_72%3A1318476031&page="+ str(MobileAmazonScraper.page) +"&content-id=amzn1.sym.f5d0d3e7-fe8a-4766-96ee-1c39e69d20b3&pd_rd_r=4222e4c1-ad0f-4f56-a47b-cfd87941a0f0&pd_rd_w=zEVAz&pd_rd_wg=Nv3TC&pf_rd_p=f5d0d3e7-fe8a-4766-96ee-1c39e69d20b3&pf_rd_r=8YCV46JXH7KXBJN5TTNN&qid=1671294335&ref=sr_pg_2"

        # iterate through each page till last
        if MobileAmazonScraper.page < 78:
            MobileAmazonScraper.page += 1
            yield response.follow(new_url, callback=self.parse) 



    def page_parse(self, response):

        # create an instance of the MobileItem class
        item = MobileItem()

        # extract name and OS. We are not interested in product, which doesn't have name or OS
        name = response.css("#productTitle::text").get()
        OS = response.css(".po-operating_system .a-span9 .a-size-base::text").get()
        if name and OS:
            # extract specifications
            item['name'] = name 
            item['price'] = response.css(".a-price-whole::text").get(default='Unknown')
            item['OS'] = OS
            item['brand'] = response.css(".po-brand .a-span9 .a-size-base::text").get(default='Unknown')
            item['rating'] = response.css("span.a-icon-alt::text").get(default='Unknown').split()[0]
            
            yield item








