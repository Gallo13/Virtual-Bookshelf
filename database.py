# Created by: Jess Gallo
# Date created: 01/19/2024
# Last Modified: 01/19/2024
# Description: Functions to establish a database connection and execute SQL queries.

import os
import mysql.connector


def establish_database_connection():
    """
        Establishes a database connection. The connection is made using the mysql.connector library.

        Parameters:
            None

        Returns:
            mydb (mysql.connector.connect): The database connection object.
        """

    password = os.getenv('MYSQL_PASSWORD')
    # Edit configuration --> environment variables --> MYSQL_PASSWORD

    mydb = (mysql.connector.connect(
        host='localhost',
        user='root',
        password=password,
        database='virtual_bookshelf'
    ))
    return mydb


def execute_sql_query(query, qvalues):
    """
        Executes an SELECT FROM WHERE statement with the provided parameters and values.

        Parameters:
            query (str): The SQL INSERT statement.
            qvalues (tuple): The values to be inserted into the database.

        Returns:
            result (list): The result of the query execution.
    """

    # Establishes a connection to the database
    mydb = establish_database_connection()
    cursor = mydb.cursor()

    try:
        if qvalues is not None:
            cursor.execute(query, qvalues)
        else:
            cursor.execute(query)

        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        # Handles Errors and gives the error codes to let us know what the issue is
        print(err)
        print("Error Code: ", err.errno)
        print("SQLSTATE: ", err.sqlstate)
        print("Message: ", err.msg)
    finally:
        cursor.close()
        mydb.close()

        """
        except Exception as e:
            # Rollback the changes and close the cursor and database connection
            print(f"An error occurred: {e}")
            mydb.rollback()
        """


def insert_book(insert, ivalues):
    """
        Executes an INSERT statement with the provided parameters and values.

        Parameters:
            insert (str): The SQL INSERT statement.
            ivalues (tuple): The values to be inserted into the database.

        Returns:
            result (list): The result of the query execution.
    """
    book_insert = ("INSERT INTO books (bID, title, pages, rating, date_added, date_published, number_in_series) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    ivalues
