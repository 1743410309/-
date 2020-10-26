import scrapy
from urllib.parse import quote
from lxml import etree
import urllib3

from tianyancha.items import PdfspiderItem


class Pdfspider(scrapy.Spider):
    name='pdfspider'

    def start_requests(self):

        for i in range(1, 50):
            urls = f'http://www.hngp.gov.cn/henan/list2?channelCode=&bz=1&pageSize=16&gglx=0&gglb=&pageNo={i}'
            # urls='https://www.tianyancha.com/search/p{i}?key='+quote(keyword)
            yield scrapy.Request(urls, callback=self.parse, dont_filter=False)

    def parse(self, response):
        text = response.text
        html = etree.HTML(text)
        list_url = html.xpath('//div[@class="List2"]//ul/li/a/@href')
        for i in list_url:
            yield scrapy.Request(i,callback=self.detail)

    def detail(self,response):
        text=response.text
        html = etree.HTML(text)
        try:
            detail_url=html.xpath("//div[@class='List1 Top5']/ul/li/a/@href")
            detail_url=detail_url[0]
            feil_name=html.xpath("//h1/text()")
            item = PdfspiderItem()
            item['file_url'] = detail_url
            item['file_name'] = feil_name
            yield item
        except Exception as p:
            print("没有pdf的格式")