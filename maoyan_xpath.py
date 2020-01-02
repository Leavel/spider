import json
import requests
from requests.exceptions import RequestException
from lxml import etree
import time


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    video_list = []
    parse_html = etree.HTML(html)
    dd_list = parse_html.xpath("//dl//dd")
    for dd in dd_list:
        name = dd.xpath("./div/div/div[1]/p[1]/a/text()")[0].strip()
        star = dd.xpath("./div/div/div[1]/p[2]/text()")[0].strip()
        time = dd.xpath("./div/div/div[1]/p[3]/text()")[0].strip()[5:19]
        video_list.append({"电影名称":name,"主演":star,"时间":time})
    for video in video_list:
        print(video)
        write_to_file(video)



def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+"\n")


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    parse_one_page(html)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
        time.sleep(1)
