import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--music', default='蒙德')
parser.add_argument('--audio', default=True)
parser.add_argument('--img_path', default='png')
parser.add_argument('--music_path', default='music')
parser.add_argument('--role', default='可莉')
args = parser.parse_args()

frame = {
    '阿贝多': 50,
    '芭芭拉': 50,
    '八重神子': 50,
    '班尼特': 50,
    '达达利亚': 50,
    '迪奥娜': 50,
    '迪卢克': 50,
    '菲谢尔': 50,
    '甘雨': 50,
    '胡桃': 70,
    '荒泷一斗': 50,
    '可莉': 50,
    '刻晴': 50,
    '雷电将军': 50,
    '莫娜': 50,
    '七七': 50,
    '琴': 50,
    '珊瑚宫心海': 50,
    '神里绫华': 50,
    '神里绫人': 50,
    '万叶': 50,
    '宵宫': 50,
    '魈': 50,
    '心海': 50,
    '行秋': 50,
    '夜兰': 50,
    '优菈': 50,
    '早柚': 50,
    '钟离': 50
}
