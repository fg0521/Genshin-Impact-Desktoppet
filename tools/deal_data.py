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

def add_zero(name,num=4):
    length = name.split('.')[0]
    if len(length)==1:
        return '000'+name
    elif len(length)==2:
        return '00'+name
    elif len(length)==3:
        return '0'+name
    else:
        return name


if __name__ == '__main__':
    roles = ['珊瑚宫心海','可莉','芭芭拉','刻晴','万叶','迪卢克','阿贝多','八重神子','班尼特','达达利亚','迪奥娜','菲谢尔','甘雨','胡桃','荒泷一斗','雷电将军','莫娜','七七','琴','神里绫华','神里绫人','温迪','宵宫','魈','心海','行秋','夜兰','优菈','早柚','钟离']
    df = pd.read_csv('/Users/maoyufeng/slash/ys_audio_cp.csv')
    # df = df[df['title'].str.contains('闲聊') | df['title'].str.contains('早上好') | df['title'].str.contains('中午好')
    #         | df['title'].str.contains('晚上好') | df['title'].str.contains('晚安')]
    df = df[df['title'].str.contains('想要了解')]
    df = df[df['name'].isin(roles)]
    for _,row in df.iterrows():
        name = row[1]
        title = re.sub(r'[^\u4e00-\u9fa5]+','',row[2])
        url = row[3]
        if not os.path.exists(f'./music/{name}'):
            os.mkdir(f'./music/{name}')
        download(url=url,path=f'./music/{name}/{title}.mp3')

    # path = './png/七七'
    # img_list = [i for i in os.listdir(path) if i.endswith('png')]
    # for img in img_list:
    #     try:
    #         name = img.split('-')[1]
    #         name = add_zero(name)
    #         os.rename(os.path.join(path, img), os.path.join(path, name))
    #     except:
    #         pass
