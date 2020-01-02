import requests
import random

from fake_useragent import UserAgent

from _kdl_ferr_proxy import proxy


class DoubanSpider(object):
    def __init__(self):
        self.url = 'https://movie.douban.com/j/chart/top_list?'
        self.headers = UserAgent()
        self.proxy_list = proxy()

    def get_page(self,params):
        random_proxy = random.choice(self.proxy_list)
        headers = {'User-Agent':self.headers.random}
        print(random_proxy)
        print(headers)
        html = requests.get(url=self.url,params=params,headers=headers,proxies=random_proxy).json()
        self.parse_page(html)

    # 解析+保存
    def parse_page(self,html):
        for film in html:
            name = film['title']
            score = film['score']
            actors = film['actors']
            print(
                {"name":name,"score":score,"actors":actors}
            )

    def main(self):
        n = input("请输入页数,一页20部电影:")
        params = {
            'type': '6',
            'interval_id': '100:90',
            'action':'',
            'start': n,
            'limit': '20',
        }
        for offset in range(int(n)):
            self.get_page(params)

if __name__ == '__main__':
    DoubanSpider().main()