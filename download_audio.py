import re

import requests
import pandas as pd
import os
def download(url,path):
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in res.iter_content():
                f.write(chunk)
        f.close()
        print(f'{path}下载完成...')
    else:
        print('链接不可访问...')

if __name__ == '__main__':
    # roles = ['珊瑚宫心海']
    # # roles = ['心海','可莉','芭芭拉','刻晴','万叶','迪卢克','阿贝多','八重神子','班尼特','达达利亚','迪奥娜','菲谢尔','甘雨','胡桃','荒泷一斗','雷电将军','莫娜','七七','琴','神里绫华','神里绫人','温迪','宵宫','魈','心海','行秋','夜兰','优菈','早柚','钟离']
    # df = pd.read_csv('/Users/maoyufeng/slash/ys_audio_cp.csv')
    # df = df[df['title'].str.contains('闲聊') | df['title'].str.contains('早上好') | df['title'].str.contains('中午好')
    #         | df['title'].str.contains('晚上好') | df['title'].str.contains('晚安')]
    # df = df[df['name'].isin(roles)]
    # for _,row in df.iterrows():
    #     name = row[1]
    #     title = re.sub(r'[^\u4e00-\u9fa5]+','',row[2])
    #     url = row[3]
    #     if not os.path.exists(f'./music/{name}'):
    #         os.mkdir(f'./music/{name}')
    #     download(url=url,path=f'./music/{name}/{title}.mp3')

    url = 'https://uploadstatic.mihoyo.com/ys-obc/2022/05/31/16576950/32af01bf230c82224d761358b997aa44_1930351836123595686.mp3'
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open('music/夜兰/晚安.mp3', 'wb') as f:
            for chunk in res.iter_content():
                f.write(chunk)
        f.close()

