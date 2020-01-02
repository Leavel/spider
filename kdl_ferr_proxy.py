import requests
import time
import random
from fake_useragent import UserAgent
from lxml import etree

proxy_pool = []


def get_page(url):
    headers = {"User-Agent": UserAgent().random}
    html = requests.get(url, headers=headers).text
    parse_page(html)


def parse_page(html):
    parse_html = etree.HTML(html)
    tr_list = parse_html.xpath("//tbody/tr")
    for tr in tr_list:
        ip = "".join(tr.xpath('./td[1]/text()'))
        port = "".join(tr.xpath('./td[2]/text()'))
        proxies = {
            "http": "http://{}:{}".format(ip, port),
            # "https": "https://{}:{}".format(ip, port)
        }
        proxy_pool.append(proxies)


def proxy():
    # n = int(input("请输入要抓取几页ip,一页15个:"))
    # start = 1
    # end = n + 1
    for offset in range(1,2):
        url = "https://www.kuaidaili.com/free/inha/{}/".format(offset)
        get_page(url)
        # time_random = random.randint(3, 8)
        # print("列表中现已有%s个ip" % len(proxy_pool))
        # if offset + 1 < end:
        #     print("第%s页数据已抓取晚完成,隔%s秒后进行下一页数据爬取" % (offset, time_random))
        #     time.sleep(time_random)
        # else:
        #     print("第%s页数据已抓取晚完成,ip爬取完成" % offset)

    return proxy_pool
