#!/usr/bin/env python
# coding=utf-8
# author: Lionly

from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
from os import path
import numpy as np
import argparse
import sys

d = path.dirname(__file__)

encoding = sys.stdin.encoding
if encoding is None:
    encoding = 'UTF-8'
parser = argparse.ArgumentParser(description=u'标签词云工具', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("list", help=u" list data ( string ) Like: '哈哈|12#呵呵|1' ")
parser.add_argument("-m", "--mask", help=u"mask img")
parser.add_argument("-o", "--output", help=u"output file path", default=path.join(d, 'tmp.png'))

args = parser.parse_args()
tags = args.list.decode(encoding)

font_path = path.join(d, 'FZHei.ttf')
if not args.mask:
    wc = WordCloud(background_color="white", font_path=font_path, max_font_size=60, max_words=500, random_state=42)
else:  # 通过 mask 参数 来设置词云形状
    mask_img = np.array(Image.open(path.join(d, args.mask)))
    image_colors = ImageColorGenerator(mask_img)
    wc = WordCloud(background_color="white", font_path=font_path, max_font_size=60, max_words=500, mask=mask_img,
                   color_func=image_colors)

# generate word cloud
lists = tags.split('#')
if len(lists) > 2:
    fre = {}
    for item in lists:
        k, v = item.split('|')
        fre[k] = int(v)
    wc.generate_from_frequencies(fre)  # wc.fit_words(fre)
else:
    wc.generate(tags)

# save
wc.to_file(args.output)
print {'code': 1, 'path': args.output}
