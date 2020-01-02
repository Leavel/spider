import requests
import time
import random
from hashlib import md5


def get_salt_sign_ts(word):
    # ts
    ts = str(int(time.time() * 1000))
    # salt
    salt = ts + str(random.randint(0, 9))
    # sign
    string = "fanyideskweb" + word + salt + "n%A-rKaT5fb[Gy?;N5@Tj"
    s = md5()
    s.update(string.encode())
    sign = s.hexdigest()
    return ts, salt, sign


def attack_yd(word):
    ts, salt, sign = get_salt_sign_ts(word)
    url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '236',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'OUTFOX_SEARCH_USER_ID_NCOO=692738834.5379668; OUTFOX_SEARCH_USER_ID="1132887710@10.169.0.84"; _ga=GA1.2.845087185.1573310083; _gid=GA1.2.289821871.1577172330; JSESSIONID=aaaCs8_fqXaOj7zFkl38w; ___rl__test__cookies=1577179093744',
        'Host': 'fanyi.youdao.com',
        'Origin': 'http://fanyi.youdao.com',
        'Referer': 'http://fanyi.youdao.com/',
        'User-Agent': 'Mozilla/5.0 X11; Linux x86_64 AppleWebKit/537.36 KHTML, like Gecko Chrome/78.0.3904.87 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    data = {
        "i": word,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": salt,
        "sign": sign,
        "ts": ts,
        "bv": "54601983cd937ebe6d8d70bf1bdaa240",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTlME",
    }

    html = requests.post(url,data=data, headers=headers).json()
    print(html['translateResult'][0][0]['tgt'])


if __name__ == "__main__":
    while True:
        word = input("请输入要翻译的单词:")
        attack_yd(word)
