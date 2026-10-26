import os
import mysql.connector
from mysql.connector import errorcode

db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_port = int(os.getenv("DB_PORT"))
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

def get_connection():
    try:
        connection = mysql.connector.connect(host = db_host, port = db_port, database = db_name, user = db_user, password = db_password)
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
