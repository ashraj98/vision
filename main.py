from db import DBClient
from fontgen import read_all_fonts

if __name__ == '__main__':
    client = DBClient()
    client.drop_schema()
    client.create_schema()
    fonts = read_all_fonts(root_dir='data/fonts')
    client.bulk_add_fonts(fonts=fonts)
    exit(0)
