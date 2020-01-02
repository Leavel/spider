import requests
import json
import random
from fake_useragent import UserAgent

from kdl_ferr_proxy import proxy


class TencentSpider(object):
    def __init__(self):
        self.headers = UserAgent()
        self.proxy_list = proxy()
        self.index_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1577268229839&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
        self.two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1577269136284&postId={}&language=zh-cn'

    def get_page(self, url):
        headers = {'User-Agent': self.headers.random}
        proxy = random.choice(self.proxy_list)
        html = requests.get(url, headers=headers, proxies=proxy)
        if html.status_code == 200:
            return json.loads(html.text)
        else:
            return None

    def parse_index_page(self, offset):
        """
        解析一级页面
        :return:
        """
        html = self.get_page(self.index_url.format(offset))
        for job in html['Data']['Posts']:
            postid = job['PostId']
            job_name = job['RecruitPostName']
            two_url = self.two_url.format(postid)
            duty, requirement = self.parse_two_page(two_url)
            print(
                {'岗位名称:': job_name, '岗位要求:': duty, '岗位职责:': requirement}
            )

    def parse_two_page(self, two_url):
        html = self.get_page(two_url)
        duty = html['Data']['Responsibility']
        requirement = html['Data']['Requirement']
        return duty, requirement

    def main(self):
        for offset in range(1, 11):
            self.parse_index_page(str(offset))


if __name__ == '__main__':
    TencentSpider().main()
