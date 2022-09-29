import requests


if __name__ == '__main__':
    url = 'http://233366.proxy.nscc-gz.cn:8888/?text=你好&speaker=派蒙'
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open('./test.mp3', 'wb') as f:
            for chunk in res.iter_content():
                f.write(chunk)
        f.close()
        print(f'下载完成...')
    else:
        print('链接不可访问...')