import mysql.connector
from config.config import Config

def connect() -> mysql.connector.MySQLConnection:
    '''connect to db'''
    config = {
        'host': Config.env["MYSQL_HOST"],
        'port': Config.env["MYSQL_PORT"],
        'user': Config.env["MYSQL_USERNAME"],
        'password': Config.env["MYSQL_PASSWORD"],
        'database': Config.env["MYSQL_DATABASE"],
    }

    conn = mysql.connector.connect(**config)
    #print(conn.is_connected())
    return conn


def db_close(conn: mysql.connector.MySQLConnection) -> None:
    '''close connection to db'''
    conn.close()


class OpenDBconnection():
    '''DB connection handler'''

    def __init__(self):
        self.conn = None

    def __enter__(self):
        self.conn = connect()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        db_close(self.conn)

