import requests
import re
import string
import random

from urllib.parse import quote
from multiprocessing import Pool
from fake_useragent import UserAgent
from requests.exceptions import ProxyError

from kdl_ferr_proxy import proxy


class ToutiaoSpider(object):
    def __init__(self):
        self.headers = UserAgent()
        self.proxy_list = proxy()
        self.toutiao_search_url = 'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset={}&format=json&keyword={}&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1577281055677'

    def get_search_page(self, url, keyword):
        headers = {
            'cookie': 'tt_webid=6773646488699684366; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6773646488699684366; csrftoken=9ae0db354d7958e1f4c14344f1ad315f; s_v_web_id=38b1490d4afd3dace078c373ee25af18; sid_guard=52e605465f927d3945db5fa830379cff%7C1577188142%7C5184000%7CSat%2C+22-Feb-2020+11%3A49%3A02+GMT; uid_tt=4bf1ea8b9f65fb5116d8e232f98910c1; sid_tt=52e605465f927d3945db5fa830379cff; sessionid=52e605465f927d3945db5fa830379cff; __tasessionId=v5a2m2nic1577279935041',
            'referer': 'https://www.toutiao.com/search/?keyword={}'.format(quote(keyword, safe=string.printable)),
            'User-Agent': self.headers.random
        }
        random_proxy = random.choice(self.proxy_list)
        html = requests.get(url, headers=headers, proxies=random_proxy)
        try:
            if html.status_code == 200:
                return html.json()
            else:
                return None
        except ProxyError:
            self.proxy_list.remove(random_proxy)

    def get_article_page(self, url):
        html = requests.post(url, headers={'User-Agent': self.headers.random})
        if html.status_code == 200:
            return html.text
        else:
            return None

    def _re(self, html):
        try:
            pattern = re.compile("articleInfo.*?content: '(.*?)'", re.S)
            images_list = pattern.findall(html)
            for images in images_list:
                image_split = images.split(';')
                for url in image_split:
                    if url[:4] == 'http':
                        str_url = str(url)
                        one = str_url.replace("\\", "/")
                        url = one.replace("u002F", '')[:-6]
                        yield url
        except Exception as e:
            print(e)

    def parse_toutiao_search_page(self, offset, keyword, keyword_two):
        html = self.get_search_page(self.toutiao_search_url.format(offset, keyword), keyword_two)
        for date in html['data']:
            if (date.get('display_type_self', 'None')) == 'self_article':
                article_url = date['article_url']
                self.parse_article_page(article_url)

    def parse_article_page(self, article_url):
        html = self.get_article_page(article_url)
        items = self._re(html)
        for item in items:
            url_html = requests.get(item, headers={'User-Agent': self.headers.random}).content
            filename = item[-10:] + '.jpg'
            with open(filename, 'wb')as f:
                print(filename)
                f.write(url_html)

    def main(self, offset, keyword):
        self.parse_toutiao_search_page(offset, keyword, keyword)


if __name__ == '__main__':
    toutiao = ToutiaoSpider()
    num = int(input("请输入要爬取的页数:"))
    keyword = input("请输入关键词:")
    for offset in range(num):
        toutiao.main(int(offset) * 20, keyword)
        print('第%s页爬取完成' % (int(offset) + 1))
