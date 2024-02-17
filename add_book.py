# Created by: Jess Gallo
# Date created: 01/19/2024
# Last modified: 01/31/2024
# Description: Function for adding books to the user's database


from database import execute_sql_query
from flask import session

# -- BOOK DATA ------------------------------------


def check_book_exists(title, pages, date_published):
    """
        Checks if books exists in database (books table) using titles, pages and date-published

        Parameters:
            title (str): The values to be queried from database
            pages (int): The values to be queried from database
            date_published (str): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    # !!!!!!!!!!!!!! should check by title and author instead
    # SQL query to check if the book already exists in the database
    query = "SELECT bID FROM books WHERE title = %s AND pages = %s AND date_published = %s"
    qvalues = (title, pages, date_published)
    # executes book_query (select statement)
    book_id = execute_sql_query(query, qvalues)
    return book_id[0][0] if book_id else None


def insert_account_books():
    """
        Checks if books exists in database (account_books) using the book_query_value which produces the bID (book ID)

        Returns:
            result (list): The result of the query execution.
    """
    # Check if book exists in account_books table
    query = "SELECT * FROM account_books WHERE bID = %s AND uID = %s"
    qvalues = (session['bID'], session['uID2'])
    account_books_query_value = execute_sql_query(query, qvalues)

    # If the book is not associated with the user
    if not account_books_query_value:
        # Inserts book into account_books table
        query = "INSERT INTO account_books (uID, bID) VALUES (%s, %s);"
        qvalues = (session['uID2'], session['bID'])
        return execute_sql_query(query, qvalues)
    # If user already inputed the book
    else:
        print('Book already associated with account!')
        return account_books_query_value


def insert_book(ivalues):
    """
        Executes an INSERT statement with the provided parameters and values.

        Parameters:
            ivalues (tuple): The values to be inserted into the database.

        Returns:
            result (list): The result of the query execution.
    """
    query = ("INSERT INTO books (bID, title, pages, rating, date_added, date_published, number_in_series) "
             "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    return execute_sql_query(query, ivalues)


# -- AUTHOR DATA -----------------------------------


def check_author_exists(author_fname, author_lname):
    """
        Checks if author exists in database (authors table) using author's first and last name

        Parameters:
            author_fname (str): The values to be queried from database
            author_lname (str): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    # SQL query to check if the author already exists in the database
    query = "SELECT aID FROM authors WHERE firstname = %s AND lastname = %s"
    qvalues = (author_fname, author_lname)
    author_id = execute_sql_query(query, qvalues)
    return author_id[0][0] if author_id else None


def insert_author(ivalues):
    """
        Executes an INSERT statement with the provided parameters and values.

        Parameters:
            ivalues (tuple): The values to be inserted into the database.

        Returns:
            result (list): The result of the query execution.
    """
    query = "INSERT INTO authors (aID, firstname, lastname) VALUES (%s, %s, %s)"
    execute_sql_query(query, ivalues)


def insert_book_author(author_query_value):
    """
        Checks if authors exists in database with book (book_author) using the author_query_value which produces
        the bID (book ID)

        Parameters:
            author_query_value (str): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    # Inserts book into account_books table
    query = "INSERT INTO book_author (bID, aID) VALUES (%s, %s);"
    qvalues = (session['bID'], author_query_value)
    return execute_sql_query(query, qvalues)


# -- GENRE DATA -----------------------------------


def check_genre_exists(genre):
    """
        Checks if genre exists in database (genre table) using genre variable

        Parameters:
            genre (str): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    # SQL query to check if the author already exists in the database
    query = "SELECT gID FROM genre WHERE genre = %s"
    qvalues = (genre,)
    genre_id = execute_sql_query(query, qvalues)
    return genre_id[0][0] if genre_id else None


def insert_book_genre(genre_query_value):
    """
        Checks if genre exists in database (book_genres) using the genre_query_value which produces the bID (book ID)

        Parameters:
            genre_query_value (str): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    query = "INSERT INTO book_genre (bID, gID) VALUES (%s, %s);"
    qvalues = (session['bID'], genre_query_value)
    return execute_sql_query(query, qvalues)


def insert_genre(ivalues):
    """
        Executes an INSERT statement with the provided parameters and values.

        Parameters:
            ivalues (tuple): The values to be inserted into the database.

        Returns:
            result (list): The result of the query execution.
    """
    query = "INSERT INTO genre (gID, genre) VALUES (%s, %s)"
    return execute_sql_query(query, ivalues)


# -- PUBLISHER DATA -----------------------------------


def check_publisher_exists(publisher):
    """
        Checks if author exists in database (publisher table) using publisher variable

        Parameters:
            publisher (str): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    # SQL query to check if the author already exists in the database
    query = "SELECT pID FROM publisher WHERE publisher = %s"
    qvalues = (publisher,)
    publisher_id = execute_sql_query(query, qvalues)
    return publisher_id[0][0] if publisher_id else None


def insert_book_publisher(publisher_query_value):
    """
        Checks if publisher exists in database (book_publisher) using the publisher_query_value which produces
        the bID (book ID)

        Parameters:
            publisher_query_value (str): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    # Inserts book into account_books table
    query = "INSERT INTO book_publisher (bID, pID) VALUES (%s, %s);"
    qvalues = (session['bID'], publisher_query_value)
    return execute_sql_query(query, qvalues)


def insert_publisher(ivalues):
    """
        Executes an INSERT statement with the provided parameters and values.

        Parameters:
            ivalues (tuple): The values to be inserted into the database.

        Returns:
            result (list): The result of the query execution.
    """
    query = "INSERT INTO publisher (pID, publisher) VALUES (%s, %s)"
    return execute_sql_query(query, ivalues)


# -- SERIES DATA -----------------------------------


def check_series_exists(series):
    """
        Checks if series exists in database (series table) using series variable

        Parameters:
            series (str): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    # SQL query to check if the author already exists in the database
    query = "SELECT sID FROM series WHERE seriesName = %s"
    qvalues = (series,)
    series_id = execute_sql_query(query, qvalues)
    return series_id[0][0] if series_id else None


def insert_book_series(series_query_value):
    """
        Checks if series exists in database (book_series) using the series_query_value which produces the bID (book ID)

        Parameters:
            series_query_value (str): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    # Inserts book into account_books table
    query = "INSERT INTO book_series (bID, sID) VALUES (%s, %s);"
    qvalues = (session['bID'], series_query_value)
    return execute_sql_query(query, qvalues)


def insert_series(ivalues):
    """
        Executes an INSERT statement with the provided parameters and values.

        Parameters:
            ivalues (tuple): The values to be inserted into the database.

        Returns:
            result (list): The result of the query execution.
    """

    query = "INSERT INTO series (sID, seriesName) VALUES (%s, %s)"
    return execute_sql_query(query, ivalues)


# -- UPDATES DATA IN DATABASE -- #


def update_read(rating):
    """
        Updates read data in database (books) using the rating variable

        Parameters:
            rating (int): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    # SQL query to update read data in account_books table
    query = "UPDATE books SET rating = %s WHERE bID = %s;"
    qvalues = (rating, session['bID'])
    return execute_sql_query(query, qvalues)


def update_series(number_in_series):
    """
        Updates series data in database (books) using the series_num variable

        Parameters:
            number_in_series (int): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    # SQL query to update series data in account_books table
    query = "UPDATE books SET number_in_series = %s WHERE bID = %s;"
    qvalues = (number_in_series, session['bID'])
    return execute_sql_query(query, qvalues)
