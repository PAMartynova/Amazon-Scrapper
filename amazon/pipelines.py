# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class AmazonPipeline:

    def __init__(self):
        self.conn = sqlite3.connect('amazon.db')
        self.curr = self.conn.cursor()
        self.curr.execute("""CREATE TABLE IF NOT EXISTS new_office (name TEXT, price INTEGER, purchases INTEGER, country TEXT, UNIQUE(name))""")
        self.curr.execute("""CREATE TABLE IF NOT EXISTS mobiles (name TEXT, price INTEGER, brand TEXT, rating TEXT, OS TEXT, UNIQUE(name))""")



    def process_item(self, item, spider):
        if spider.name == 'amazon':
            self.curr.execute("""INSERT INTO new_office VALUES (?, ?, ?, ?)""", (item['name'], item['price'], item['ratings'], item['country']))
            self.conn.commit()
            return item
        if spider.name == 'mobile':
            self.curr.execute("""INSERT INTO mobiles VALUES (?, ?, ?, ?, ?)""", (item['name'], item['price'], item['brand'], item['rating'], item['OS']))
            self.conn.commit()
            return item
