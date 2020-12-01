import random
import shutil
from datetime import datetime

import stringcase

from db import DBClient
from fontgen import random_text, read_all_fonts
from upload import upload_train_data


def load_fonts_into_schema():
    client = DBClient()
    client.drop_schema()
    client.create_schema()
    fonts = read_all_fonts(root_dir='data/fonts')
    client.bulk_add_fonts(fonts=fonts)


def generate_training_data():
    client = DBClient()
    fonts = client.all_fonts()
    for i, font in enumerate(fonts):
        for j in range(600):
            random_text(font=font['filename'], lowercase=True)
            uid = upload_train_data('data/pil/random_text.png')
            client.add_image(f'train/{uid}.jpg', font['id'])
        for j in range(600):
            random_text(font=font['filename'], lowercase=False)
            uid = upload_train_data('data/pil/random_text.png')
            client.add_image(f'train/{uid}.jpg', font['id'])
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"#{i}: {font['name']} done at {current_time}.")


def generate_font_samples():
    client = DBClient()
    fonts = client.all_fonts()
    for i, font in enumerate(fonts):
        random_text(font=font['filename'], lowercase=False)
        shutil.copyfile('data/pil/random_text.png', f'data/samples/{stringcase.snakecase(font["name"])}.jpg')


if __name__ == '__main__':
    load_fonts_into_schema()
    generate_training_data()
    exit(0)
