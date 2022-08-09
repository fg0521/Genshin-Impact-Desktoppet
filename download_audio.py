import requests
def download(url,path):
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in res.iter_content():
                f.write(chunk)
        f.close()
    else:
        print('链接不可访问...')

if __name__ == '__main__':
    url = 'https://uploadstatic.mihoyo.com/ys-obc/2021/03/12/4359827/83e894b9faa4ebe8935d75a5c54c959c_3883502189516950902.mp3'
    path = 'test.mp3'
    download(url,path)




