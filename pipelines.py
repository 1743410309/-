# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
import scrapy
from os.path import basename,dirname,join
class TianyanchaPipeline(object):
    def open_spider(self, spider):
        """  当 目标 spider 实例化的时候， 调用此方法

                一般用于一些资源的初始化

        :param spider:   对应的 spider 实例
        :return:
        """

        # mongo_config = spider.settings['MONGO_CONFIG']
        # self.client = MongoClient(host=mongo_config['host'], port=mongo_config['port'])
        # self.db = self.client[mongo_config['db']]
        # self.coll = self.db[mongo_config['coll']]

        mysql_config = spider.settings['MYSQL_CONFIG']
        import pymysql
        self.conn = pymysql.connect(**mysql_config)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        """ 当 spider 实例销毁时，调用

                一般用于一些资源的释放
        :param spider:   spider 的实例
        :return:
        """
        # self.client.close()

        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def process_item(self, item, spider):
        """ 将 item 数据尽心持久化操作

        :param item:  item结构化的数据
        :param spider: 传递的 spider 对象实例
        :return:
        """

        #  数据保存到mongodb
        # self.coll.insert(dict(item))
        result = self.insert_mysql(item)
        # print('mysql写入结果：', result)

        # 如果进行了 return，那么 会在 控制台 查看到 item 的输出
        # 最后一个 pipeline 的 return 是在 控制台进行 print 输出
        return item

    def insert_mysql(self, item):
        sql = 'insert into jialefu(gsname, state, perpon, money,riqi) values(%s,%s,%s,%s,%s)'
        result = self.cursor.execute(sql, (item['gsname'], item['state'], item['perpon'], item['money'],item['riqi']))
        return result


class SpiderpdfPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['file_url'],meta={'title':item["file_name"]})
    def file_path(self, request, response=None, info=None):
        pdf_url=urlparse(request.url).path
        pdf_name=request.meta.get("title")+'.pdf'
        return join(basename(dirname(pdf_url)),basename(pdf_name))