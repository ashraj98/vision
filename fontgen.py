import os
import random

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from google.protobuf import text_format

from protobuf import fonts_public_pb2


def read_font_metadata(path):
    protobuf_file = open(path, 'r')
    protobuf = protobuf_file.read()

    font_family = fonts_public_pb2.FamilyProto()
    text_format.Merge(protobuf, font_family)
    return font_family


def read_all_fonts(root_dir='data/fonts'):
    fonts = []
    for subdir, dirs, files in os.walk(root_dir):
        if 'METADATA.pb' in files:
            md = read_font_metadata(path=f'{subdir}/METADATA.pb')
            for font in md.fonts:
                fonts.append((
                    font.name, font.style, font.weight, f'{subdir}/{font.filename}',
                    font.post_script_name, font.full_name,
                ))
    fonts.sort()
    return fonts


def random_text(font='/Library/Fonts/Arial.ttf', lowercase=True):
    str_choices = 'abcdefghijklmnopqrstuvwxyz '
    noise_var = random.randint(50, 150)
    height = 100
    width = 500
    font_size = int(height * .8)
    random_color = np.random.randint(low=0, high=255, size=(1, 1, 3), dtype=np.uint8)
    noise = np.random.randint(low=-noise_var, high=noise_var, size=(height, width, 3))
    pixels = (random_color + noise).astype(np.uint8)
    pixels = cv2.medianBlur(pixels, 7)
    bg = cv2.cvtColor(pixels, cv2.COLOR_BGR2RGB)
    bg = Image.fromarray(bg)
    d = ImageDraw.Draw(bg)
    font = ImageFont.truetype(font, font_size)
    text = ''.join(random.choices(str_choices, k=random.randint(8, 16)))
    if not lowercase:
        text = text.upper()
    w, h = font.getsize(text)
    d.text(((width - w) // 2, (height - h) // 2), text=text, font=font, fill=(255, 255, 255))
    bg.save('data/pil/random_text.png')
