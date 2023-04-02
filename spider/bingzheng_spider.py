import re
import urllib.error
import urllib.request
import xlwt
import requests

from bs4 import BeautifulSoup


def get_html(url):
    # 网站请求
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Referer": "http://www.birdreport.cn/",
        "requestId": "54585a16f827af4e82f8a93f826cbe5c",
        "sign": "42cf2dbbfbf0edec7a10261aa6ee5149",
        "timestamp": "1680010312000",
    }
    params = {
        "params": "aMduN2WBrMfxVsUeRzwtoMsEXAvn9W1oER3har/WFHu64RRyAsKAeP0iDKrZ4RPWi+++nZRsnDyqXu3B9xz1ChUjbsEnpoguDsbc/MkXEBjMDZRAzPmnsbVk6bAGDNNJSuQcLy9NiATe4JoQwMs7xrWx1o+CTsKPB+5ADGtd2qM="
    }
    request = requests.post(url=url, headers=head, params=params, verify=False)
    return request.text


if __name__ == '__main__':
    url = 'https://api.birdreport.cn/front/activity/search'
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser", from_encoding="gb18030")
    print(soup)

