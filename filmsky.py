import requests
import re

class FilmSkySpider(object):
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"}
        self.proxies = {"http": "http://163.204.244.248:9999"}

    def get_page(self,url):
        _request = requests.get(url,headers=self.headers,proxies=self.proxies).content.decode("GBK","ignore")  # ignore 忽略不识别的编码方式
        return _request

    def parse_one_page(self,html):
        pattern = re.compile('<table width="100%".*?<a href="(.*?)".*?>(.*?)</a>',re.S)
        film_list = pattern.findall(html)
        for film in film_list:
            name = film[1].strip()
            link = film[0].strip()
            download_link = self.parse_two_page(link)
            print("标题:%s,下载连接:%s"%(name,download_link))

    def parse_two_page(self,link):
        url = "https://www.dygod.net"
        html = self.get_page(url + link)
        pattern = re.compile('<table style="BORDER-BOTTOM.*?<a href="(.*?)">',re.S)
        return pattern.findall(html)[0]


if __name__ == "__main__":
    url = "https://www.dygod.net/html/gndy/dyzz/index.html"
    spider = FilmSkySpider()
    html = spider.get_page(url)
    spider.parse_one_page(html)

