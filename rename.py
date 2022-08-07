import os

if __name__ == '__main__':
    path = './yuanshen/芭芭拉'
    img_list = [i for i in os.listdir(path) if i.endswith('png')]
    for img in img_list:
        name = img.split('-')[1]
        os.rename(os.path.join(path,img),os.path.join(path,name))