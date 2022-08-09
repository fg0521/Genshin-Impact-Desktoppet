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





if __name__ == '__main__':
    s = Spider()
    s.parse_url()
    s.parse_audio()
    df = pd.read_csv('ys_audio.csv')
    df.insert(0,'ID',[i for i in range(1,len(df)+1)])
    df.to_csv('ys_audio_cp.csv',index=False,encoding='utf-8')