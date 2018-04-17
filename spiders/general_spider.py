import scrapy
import os
import json
from scrapytutorial import items
from scrapytutorial.util.read_properties import Properties
from scrapytutorial.util.common import Common

class DmozSpider(scrapy.Spider):
    # 获取配置文件路径
    prop_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))+  '/conf/conf.properties'
    rules_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))+  '/conf/rule.json'

    # 获取conf.properties配置文件属性
    prop = Properties(prop_path).getProperties()

    # 爬虫名称
    name = prop['name']

    # 允许访问的域
    allowed_domains = [
        prop['allowd_domains']
    ]

    # 起始url
    start_urls = [
        prop['start_url']
    ]

    # 爬取的字段
    fields = prop['fields']
    fields_list = fields.split(',')
    #print(fields_list)

    # 爬取的类型
    type = prop['type']
    # yield 提取规则
    rules = []
    # 从rule.json中读取
    with open(rules_path, encoding='utf-8') as f:
        rules_setting = json.load(f)
        rules = rules_setting['rules']
        next_xpath = rules_setting['next_page']
        if type == '2' :
            link_xpath = rules_setting['link_path']


    # 开始请求
    def start_requests(self):
        if self.type == '1':
            yield scrapy.Request(self.start_urls[0], callback=self.parse_Item)
        elif self.type == '2':
            yield scrapy.Request(self.start_urls[0], callback=self.parse_Link)


    # 直接爬当前页面（需要翻页）
    def parse_Item(self, response):

        item = items.GeneralItem()

        wrap_xpath = Common.find_wrap(self.rules[0]['xpathRule'], self.rules[1]['xpathRule'])
        wraps = response.xpath(wrap_xpath)

        for wrap in wraps:
            for rule in self.rules:
                item[rule['field']] = wrap.xpath(Common.find_sub_of_wrap(wrap_xpath, rule['xpathRule'])).extract()
            yield item
        next_page = response.xpath(self.next_xpath)
        if (next_page):
            for href in next_page:
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, callback=self.parse_Item)

    # 需要从当前页面追踪链接的（需要翻页）
    def parse_Link(self,response):
        links = response.xpath(self.link_xpath)

        for each in links:
            url = response.urljoin(each.extract())
            yield scrapy.Request(url, callback=self.parse_Item_by_Link)

        next_page = response.xpath(self.next_xpath)
        if (next_page):
            for href in next_page:
                url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_Link)

    def parse_Item_by_Link(self, response):
        item = items.GeneralItem()
        for rule in self.rules:
            item[rule['field']] = response.xpath(rule['xpathRule']).extract()
            yield item


