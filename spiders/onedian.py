import scrapy
from urllib.parse import quote
class OneScrapy(scrapy.Spider):
    name='one'

    def start_requests(self):
        canshu = '女装'
        url='https://www.yhd.com/c0-0/k'+ quote(canshu)
        yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        text=response.text
        print(text)