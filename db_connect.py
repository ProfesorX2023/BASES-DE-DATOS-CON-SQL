# db_connect.py
import mysql.connector as mysql

DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "123456"   # cámbialo
DB_NAME = "NetflixDB"

def get_conn(db=None):
    return mysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=db
    )