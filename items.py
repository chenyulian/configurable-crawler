# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import os
from scrapytutorial.util.read_properties import Properties

class ItemMetaClass(type):
    def __new__(cls, name, base, fields):
        # 获取配置文件路径
        prop_path = os.path.abspath(os.path.join(os.path.dirname(__file__))) + '/conf/conf.properties'

        # 获取conf.properties配置文件属性
        prop = Properties(prop_path).getProperties()

        fields = prop['fields'].split(',')
        fields_dict = {}
        # 创建Item类时，读取配置文件中的字段名，根据字段名创建Item
        for field in fields:
            fields_dict[field] = scrapy.Field()
        return type('GeneralItem', base, fields_dict)

class MyItemMetaClass(ItemMetaClass, scrapy.Item.__class__):
    pass

class GeneralItem(scrapy.Item, metaclass=MyItemMetaClass):
    def __init__(self):
        super(GeneralItem, self).__init__()


