# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
import os
from dotenv import load_dotenv


load_dotenv()   # loads .env into os.environ

class MongoPipeline:
    def open_spider(self, spider):
        uri = os.getenv("MONGO_URI")
        # db_name = os.getenv("MONGO_DB", "quotesdb")
        db_name = os.getenv("MONGO_DB", "newsdb")
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db_name]
        # Create index to avoid duplicate quotes
        # self.db["quotes"].create_index("url", unique=True)
        self.db["articles"].create_index("url", unique=True)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            # self.db["quotes"].insert_one(dict(item))
            self.db["articles"].insert_one(dict(item))
        except pymongo.errors.DuplicateKeyError:
            pass # skip if quote already exists
        return item
