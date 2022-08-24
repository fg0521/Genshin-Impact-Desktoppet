import os

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
    path = './png/胡桃'
    img_list = [i for i in os.listdir(path) if i.endswith('png')]
    for img in img_list:
        try:
            name = img.split('-')[1]
            name = add_zero(name)
            os.rename(os.path.join(path,img),os.path.join(path,name))
        except:
            pass
    # print(add_zero('123.jpg'))