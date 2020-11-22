from db import DBClient

if __name__ == '__main__':
    client = DBClient()
    client.create_schema()
    exit(0)
