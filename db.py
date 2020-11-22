import sqlite3


class DBClient:
    def __init__(self, db='store.db'):
        self.conn = sqlite3.connect(db)

    def create_schema(self):
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS fonts
        (name text, style text, weight int, filename text, ps_name text, fullname text)
        ''')
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS images
        (filename text, font int, FOREIGN KEY(font) REFERENCES fonts(id))
        ''')
        self.conn.commit()

    def drop_schema(self):
        self.conn.execute('DROP TABLE IF EXISTS fonts')
        self.conn.execute('DROP TABLE IF EXISTS images')
        self.conn.commit()

    def add_font(self, name, style, weight, filename, ps_name, fullname):
        self.conn.execute('''
        INSERT INTO fonts
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, style, weight, filename, ps_name, fullname))
        self.conn.commit()

    def bulk_add_fonts(self, fonts=None):
        if fonts is None:
            fonts = []
        self.conn.executemany('''
        INSERT INTO fonts
        VALUES (?, ?, ?, ?, ?, ?)
        ''', fonts)
        self.conn.commit()

    def add_image(self, filename, font_id):
        self.conn.execute('INSERT INTO images VALUES (?, ?)', (filename, font_id))
        self.conn.commit()
