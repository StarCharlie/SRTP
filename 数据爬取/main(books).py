import requests
import fake_useragent
from fake_useragent import UserAgent
from lxml import etree
import csv
class dangdang(object):
    def __init__(self):
        self.url = 'http://book.chaoxing.com/search/keyword_{}/fenleiID_0/field_all/sortName_/nPage_1/size_100.html'
        ua = UserAgent(verify_ssl=False)
        for i in range(1, 100):
            self.headers = {
                'User-Agent': ua.random
            }
    def get_html(self,url):
        response=requests.get(url,headers=self.headers)
        html=response.text
        return html
    def parse_html(self,html):
        target=etree.HTML(html)
        names = target.xpath('//ul[@class="list"]/li[@class="clearfix"]/div[@class="pic_upost"]/a/@title')
        titles=target.xpath('//ul[@class="list"]/li[@class="clearfix"]/div[@class="list_right"]/p[@class="name"]/span/text()')
        with open('D:/dangdang.csv','a',newline='',encoding='gb18030') as f:
            csvwriter = csv.writer(f, delimiter=',')
            for name,title in zip(names,titles):
                csvwriter.writerow([name,title])
    def main(self):
        product = str(input('关键词索引：'))
        url = self.url.format(product)
        html=self.get_html(url)
        self.parse_html(html)
if __name__ == '__main__':
    spider = dangdang()
    spider.main()
