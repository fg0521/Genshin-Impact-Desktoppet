import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--kl', default='kl')
parser.add_argument('--bbl', default='yuanshen/芭芭拉')
parser.add_argument('--kq', default='yuanshen/刻晴')
parser.add_argument('--ttbj', default='ttbj')
parser.add_argument('--wy', default='wy')
parser.add_argument('--dlk', default='yuanshen/迪卢克')

args = parser.parse_args()

dic = {'yuanshen/刻晴': '见光如我~ 斩尽牛杂~',
       'yuanshen/ 可莉': '哒哒哒 ～ 啦啦啦～',
       'yuanshen/芭芭拉': '演唱~ 开始~',
       'yuanshen/迪卢克': '在此~ 宣判~',
       }