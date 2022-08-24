import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--music',default='蒙徳')
parser.add_argument('--audio',default=True)
parser.add_argument('--img_path', default='png')
parser.add_argument('--music_path', default='music')
parser.add_argument('--role', default='可莉')
args = parser.parse_args()

