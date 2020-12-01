import random
import shutil
from datetime import datetime

import stringcase
import numpy as np

from db import DBClient
from fontgen import random_text, read_all_fonts
from fonts.generator import Generator
from fonts.model import model
from fonts.preprocess import generate_train_dataset, generate_test_dataset
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
    batch_size = 8
    X_train_filenames = np.load('data/train/x_filenames.npy')
    y_train = np.load('data/train/y_labels.npy')
    X_test_filenames = np.load('data/test/x_filenames.npy')
    y_test = np.load('data/test/y_labels.npy')

    training_batch_generator = Generator(X_train_filenames, y_train, batch_size)
    validation_batch_generator = Generator(X_test_filenames, y_test, batch_size)
    model.fit(x=training_batch_generator,
              steps_per_epoch=int(46092 // batch_size),
              epochs=2,
              verbose=1,
              validation_data=validation_batch_generator,
              validation_steps=int(9108 // batch_size))
    model.save(filepath='models/font', overwrite=True, include_optimizer=True)
    exit(0)
