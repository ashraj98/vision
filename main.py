from db import DBClient
from fontgen import random_text, read_all_fonts


def load_fonts_into_schema():
    client = DBClient()
    client.drop_schema()
    client.create_schema()
    fonts = read_all_fonts(root_dir='data/fonts')
    client.bulk_add_fonts(fonts=fonts)


if __name__ == '__main__':
    random_text(font='data/fonts/ibmplexsans/IBMPlexSans-Bold.ttf')
    exit(0)
