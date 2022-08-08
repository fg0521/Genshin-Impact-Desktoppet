import re

import requests
from bs4 import BeautifulSoup
import pprint


class Spider():
    def __init__(self):
        self.url = 'https://bbs.mihoyo.com/ys/obc/content/1614/detail?bbs_presentation_style=no_header'
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

    def parse(self):
        res = requests.get(self.url,self.headers)
        if res.status_code == 200:
            print(res.text)
            soup = BeautifulSoup(res.text,'html.parser')
            title_list = soup.select('.obc-tmpl-fold__title p')
            titles = [i.text for i in title_list]
            print(titles)

            audio_list = soup.select('.audio')
            audios = [i.find("source").get("src") for i in audio_list]
            print(audios)

            content_list = soup.select('.obc-tmpl__paragraph-box p')
            contents = [i.text for i in content_list if i.text]
            print(contents)

            # print(re.findall('<div class="obc-tmpl__paragraph-box obc-tmpl__rich-text">(.*?)</div>',str(soup)))


if __name__ == '__main__':
    s = Spider()
    s.parse()