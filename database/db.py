import mysql.connector as mysql
import env

def get_connection():
    connection = mysql.connect(
        host=env.MYSQL_HOST,
        user=env.MYSQL_USER,
        passwd=env.MYSQL_ROOTPASS,
        database=env.MYSQL_DATABASE,
        port=3306
    )
    return connection


def get_cursor():
    return get_connection().cursor(dictionary=True)
