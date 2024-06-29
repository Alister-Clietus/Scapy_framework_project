# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2

class BhhsambScraperPipeline:
 def open_spider(self, spider):
        self.connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='Alister123@',
            dbname='properties',
            port=5432
        )
        self.cursor = self.connection.cursor()

 def close_spider(self, spider):
        self.connection.close()

 def process_item(self, item, spider):
        self.cursor.execute("""
            INSERT INTO properties (title, address, price, details, url)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            item['title'],
            item['address'],
            item['price'],
            item['details'],
            item['url']
        ))
        self.connection.commit()
        return item
