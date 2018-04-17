# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import os
import json
from scrapytutorial import items
from scrapytutorial.util.read_properties import Properties

class ScrapytutorialPipeline(object):
    pass

class MongoDBPipelineMetaclass(type):
    def __new__(cls, name, base, fields):
       pass

class MongoDBPipeline(object):
    #collection_name = 'QuoteItem'
    # 获取配置文件路径
    prop_path = os.path.abspath(os.path.join(os.path.dirname(__file__))) + '/conf/conf.properties'

    # 获取conf.properties配置文件属性
    prop = Properties(prop_path).getProperties()

    db_name = prop['name']
    def __init__(self):
        client = pymongo.MongoClient("localhost",27017)
        db = client["Spider"]
        self.MyDB = db[self.db_name]

    def process_item(self, item, spider):
        # 将item加入数据库
        try:
           self.MyDB.insert(dict(item))
        except Exception:
            pass

        return item