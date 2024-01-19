# Created by: Jess Gallo
# Date created: 01/19/2024
# Last Modified: 01/19/2024
# Description: Functions to establish a database connection and execute SQL queries.


import mysql.connector
from mysql.connector.errors import Error
from mysql.connector import errorcode


def establish_database_connection():
    mydb = (mysql.connector.connect(
        host='localhost',
        user='root',
        password='galloGiallo13',
        database='virtual_bookshelf'
    ))
    return mydb


def execute_sql_query(query, values):
    mydb = establish_database_connection()
    cursor = mydb.cursor()

    if values is not None:
        cursor.execute(query, values)
    else:
        cursor.execute(query)

    result = cursor.fetchall()

    cursor.close()
    cursor.close()

    return result
