import scrapy
from urllib.parse import quote
from lxml import etree
import urllib3



urllib3.disable_warnings()

class TianYanChaScrapy(scrapy.Spider):

    name="tianyancha"
    def start_requests(self):
        keyword=self.settings['KEYWORD']
        numbers=self.settings['PAGE_NUM']

        for i in range(1,numbers+1):
            urls=f'https://www.tianyancha.com/search/p{i}?key=%E5%AE%B6%E4%B9%90%E7%A6%8F'
            # urls='https://www.tianyancha.com/search/p{i}?key='+quote(keyword)
            yield scrapy.Request(urls,callback=self.parse,dont_filter=True)


    def parse(self, response):
        text=response.text
        html=etree.HTML(text)
        divs=html.xpath('//*[@id="web-content"]/div/div[1]/div[4]/div[2]/div')
        numbers=len(divs)
        for i in range(1,numbers+1):
            b = html.xpath(f'//*[@id="web-content"]/div/div[1]/div[4]/div[2]/div[{i}]/div/div[3]/div[1]/a/em/text()')
            if b:
                a=html.xpath(f'//*[@id="web-content"]/div/div[1]/div[4]/div[2]/div[{i}]/div/div[3]/div[1]/a/text()')
                if len(a) ==1:
                    gsname=str(b[0])+str(a[0])
                else:
                    gsname=str(a[0])+str(b[0])+str(a[1])
            else:
                a = html.xpath(f'//*[@id="web-content"]/div/div[1]/div[4]/div[2]/div[{i}]/div/div[3]/div[1]/a/text()')[0]
                gsname=a
            # 营业状态
            state=html.xpath(f'//*[@id="web-content"]/div/div[1]/div[4]/div[2]/div[{i}]/div/div[3]/div[1]/div/text()')[0]
            # 法定代表人
            p=html.xpath(f'//*[@id="web-content"]/div/div[1]/div[4]/div[2]/div[{i}]'
                              f'/div/div[3]/div[3]/div[1]/a/text()')
            if p:
                perpon = p[0]
            else:
                perpon = ''

            # 注册资金
            m=html.xpath(f'//*[@id="web-content"]/div/div[1]/div[4]/div[2]/div[{i}]/'
                             f'div/div[3]/div[3]/div[2]/span/text()')
            if m:
                money = m[0]

            else:
                money = ''
            # 成立日期
            d=html.xpath(f'//*[@id="web-content"]/div/div[1]/div[4]/div[2]/div[{i}]/'
                            f'div/div[3]/div[3]/div[3]/span/text()')
            if d:
                date = d[0]

            else:
                date = ''
            item=TianyanchaItem()
            item['gsname']=gsname
            item['state']=state
            item['perpon']=perpon
            item['money']=money
            item['riqi']=date
            yield item






