import random
import numpy as np

from tensorflow.keras.utils import to_categorical

from db import DBClient


def generate_train_dataset():
    client = DBClient()
    fonts = client.all_fonts()
    images = client.train_images()
    random.shuffle(images)
    X_filenames = [img['filename'] for img in images]
    Y_ids = [img['font'] - 1 for img in images]
    Y = to_categorical(Y_ids, num_classes=len(fonts))
    np.save('data/train/x_filenames.npy', X_filenames)
    np.save('data/train/y_labels.npy', Y)


def generate_test_dataset():
    client = DBClient()
    fonts = client.all_fonts()
    images = client.test_images()
    random.shuffle(images)
    X_filenames = [img['filename'] for img in images]
    Y_ids = [img['font'] - 1 for img in images]
    Y = to_categorical(Y_ids, num_classes=len(fonts))
    np.save('data/test/x_filenames.npy', X_filenames)
    np.save('data/test/y_labels.npy', Y)
