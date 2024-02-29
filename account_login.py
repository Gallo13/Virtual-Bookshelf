# Created by: Jess Gallo
# Date Created: 02/28/24
# Last Modified: 02/28/24
# Description: SQL Queries or user to Login and Register

# Imports
from database import execute_sql_query
from uuid import uuid4
import hashlib


def check_account_exists(email, hash_pw):
    """
        Checks if user is in the database already

        Parameters:
            email (str): The values to be queried from database
            hash_pw (str): The values to be queried from database

        Returns:
            result (list): The result of the query
    """

    query = "SELECT * FROM accounts WHERE email = %s AND password = %s;"
    qvalues = (email, hash_pw)
    account_id = execute_sql_query(query, (qvalues,))
    return account_id[0][0] if account_id else None


def insert_account_data(email, hash_pw):
    """
        Inserts new account into database

        Parameters:
            email (str): The values to be queried from database
            hash_pw (str): The values to be queries from database

        Returns:
            result (list): The result of the query
    """
    query = "INSERT INTO accounts VALUES (%s, %s, %s)"
    qvalues = (str(uuid4()), email, hash_pw)
    return execute_sql_query(query, qvalues)


def hash_password(password, secret_key):
    """
        Hashes password during registration and login

        Parameters:
            password (str): The values to be queries from database
            secret_key (str): environment variable key

        Returns:
            result (list): hashed password
        """
    hash_pw = password + secret_key
    hash_pw = hashlib.sha1(hash_pw.encode())
    return hash_pw.hexdigest()
