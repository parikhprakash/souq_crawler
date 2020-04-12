# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from souq.settings import MONGODB_COLLECTION,MONGODB_DB,MONGODB_PORT,MONGODB_SERVER
import logging
from scrapy.exceptions import DropItem 
import pymongo
log = logging.Logger("MONGOPIPELINE")
class SouqPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            MONGODB_SERVER,
            MONGODB_PORT
        )
        db = connection[MONGODB_DB]
        self.collection = db[MONGODB_COLLECTION]

    def process_item(self, item, spider):
        valid = True
        if valid:
            self.collection.insert(dict(item))
            log.debug("Item inserted to MongoDB")
        return item
