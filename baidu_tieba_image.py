import re
import time
import requests
from fake_useragent import UserAgent
from lxml import etree
from multiprocessing import Pool


class CampusFlower(object):
    def __init__(self,name,offset):
        self.tieba_url = "http://tieba.baidu.com/f?"
        self.url = "http://tieba.baidu.com"
        self.count = 0
        self.params = {
            "kw":name,
            "ie":"utf-8",
            "pn":offset
        }
        # self.proxies = {"http": "http://1.193.246.69:9999"}

    def get_page(self,url):
        html = requests.get(url, headers={"User-Agent": UserAgent().random},params=self.params).text
        return html


    def get_tlink(self,url):
        html = self.get_page(url)
        pattern = re.compile('<div class="threadlist_lz clearfix".*?href="(.*?)"',re.S)
        items = pattern.findall(html)
        for item in items:
            self.get_ilink(item)

    def get_ilink(self,url):
        link_url = self.url + url
        html = requests.get(link_url, headers={"User-Agent": UserAgent().random}).text
        parse_html = etree.HTML(html)
        link_list = parse_html.xpath('//img[@class="BDE_Image"]/@src | //div[@class="video_src_wrapper"]/embed/@data-video')
        for link in link_list:
            self.count += 1
            html = requests.get(link, headers={"User-Agent": UserAgent().random}).content
            filename = link[-15:]
            with open(filename,"wb")as f:
                print("%s" %filename)
                f.write(html)


if __name__ == "__main__":
    tieba = CampusFlower("刘亦菲", 50)
    pool = Pool()
    start = time.time()
    pool.map(tieba.get_tlink(tieba.tieba_url),[offset * 50 for offset in range(tieba.params["pn"])])
    end = time.time()
    kd = int(end) - int(start)
    print("总共花费%s秒,现已爬取%s文件" % (kd, tieba.count))