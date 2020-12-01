import sqlite3


class DBClient:
    def __init__(self, db='store.db'):
        self.conn = sqlite3.connect(db)
        self.conn.row_factory = sqlite3.Row

    def create_schema(self):
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS fonts
        (id integer primary key autoincrement, name text, style text,
        weight int, filename text, ps_name text, fullname text)
        ''')
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS images
        (id integer primary key autoincrement, filename text, font int, FOREIGN KEY(font) REFERENCES fonts(id))
        ''')
        self.conn.commit()

    def drop_schema(self):
        self.conn.execute('DROP TABLE IF EXISTS fonts')
        self.conn.execute('DROP TABLE IF EXISTS images')
        self.conn.commit()

    def add_font(self, name, style, weight, filename, ps_name, fullname):
        self.conn.execute('''
        INSERT INTO fonts(name, style, weight, filename, ps_name, fullname)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, style, weight, filename, ps_name, fullname))
        self.conn.commit()

    def bulk_add_fonts(self, fonts=None):
        if fonts is None:
            fonts = []
        self.conn.executemany('''
        INSERT INTO fonts(name, style, weight, filename, ps_name, fullname)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', fonts)
        self.conn.commit()

    def add_image(self, filename, font_id):
        self.conn.execute('INSERT INTO images(filename, font) VALUES (?, ?)', (filename, font_id))
        self.conn.commit()

    def all_fonts(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM fonts')
        result = [dict(row) for row in c.fetchall()]
        return result

    def all_images(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM images')
        result = [dict(row) for row in c.fetchall()]
        return result

    def train_images(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM images WHERE id % 600 < 200')
        result = [dict(row) for row in c.fetchall()]
        return result

    def test_images(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM images WHERE id % 600 > 579')
        result = [dict(row) for row in c.fetchall()]
        return result

    def image_count_for_font(self, font_id):
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM images WHERE font = ?', (font_id,))
        result = c.fetchone()
        if result is None:
            return 0
        return result[0]

