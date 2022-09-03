import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pprint
import os

class Spider():
    def __init__(self):
        self.roles = {}
        self.url = 'https://bbs.mihoyo.com/ys/obc/channel/map/80/84?bbs_presentation_style=no_header'
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}


    def parse_url(self):
        res = requests.get(self.url, self.headers)
        if res.status_code == 200:
            # print(res.text)
            soup = BeautifulSoup(res.text,'html.parser')
            role_list = soup.select('.home-channel__red--point a')
            # print(len(role_list))
            for role in role_list:
                name = role['title'].split(' ')[0]
                url = role['href']
                self.roles[name] = 'https://bbs.mihoyo.com'+url


    def parse_audio(self):
        for name,url in self.roles.items():
            res = requests.get(url,self.headers)
            data = []
            if res.status_code == 200:
                # print(res.text)
                soup = BeautifulSoup(res.text,'html.parser')
                title_list = soup.select('.obc-tmpl-fold__title p')
                titles = [i.text for i in title_list]
                # print(titles)

                audio_content_list = soup.select('.obc-tmpl__paragraph-box')
                audio_content = []
                for ac in audio_content_list:
                    s = BeautifulSoup(str(ac),'html.parser')
                    content = ''
                    try:
                        audio  = s.select('audio')[0].find('source').get('src')
                    except:
                        audio = ''
                    for i in range(1,4):
                        c = s.select('p')[-i].text
                        if c:
                            content = c
                            break
                    # print(audio,content)
                    audio_content.append([audio,content])

                for i in range(len(titles)):
                    data.append({'name':name,'title':titles[i],'audio':audio_content[i][0],'content':audio_content[i][1]})
            df = pd.DataFrame(data=data)
            if os.path.exists('ys_audio.csv'):
                df.to_csv('ys_audio.csv',index=False,header=False,encoding='utf-8',mode='a')
            else:
                df.to_csv('ys_audio.csv',index=False,encoding='utf-8')


class Spider2():
    def __init__(self):
        self.url = 'https://bbs.mihoyo.com/ys/obc/content/90/detail?bbs_presentation_style=no_header'
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip,deflate,br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': '_MHYUUID=bc3559d4-c619-4a2f-ba4b-24de096e07fe; UM_distinctid=182f975a254717-0909e187ccc105-1b525635-1fa400-182f975a255199f; DEVICEFP_SEED_ID=a35efdf72aaf4c13; DEVICEFP_SEED_TIME=1662042637981; mi18nLang=zh-cn; _gid=GA1.2.881785575.1662168831; CNZZDATA1275023096=1136165396-1662042007-https%253A%252F%252Fbbs.mihoyo.com%252F%7C1662168153; DEVICEFP=38d7eb133dcf0; .thumbcache_a5f2da7236017eb7e922ea0d742741d5=WQ3qDA1Z6n/GcrhltPncsPOHt1/2qIrLAWPTRthERnfC98u+J9NdzjUq2dDwikC7Y2/cmeQH7SmmNNTn+AKJKQ%3D%3D; _gat_gtag_UA_133007358_5=1; _ga_9TTX3TE5YL=GS1.1.1662169003.2.1.1662169038.0.0.0; _ga=GA1.2.1366436115.1662042610',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

    def get_role_info(self):
        res = requests.get(self.url,self.headers)
        if res.status_code == 200:
            print(res.text)
            soup = BeautifulSoup(res.text,'html.parser')
            info_list = soup.select('.obc-tmpl-illustration__first-col')
            pprint.pprint(info_list)


if __name__ == '__main__':
    # s = Spider()
    # s.parse_url()
    # s.parse_audio()
    # df = pd.read_csv('ys_audio.csv')
    # df.insert(0,'ID',[i for i in range(1,len(df)+1)])
    # df.to_csv('ys_audio_cp.csv',index=False,encoding='utf-8')

    s = Spider2()
    s.get_role_info()