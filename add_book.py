# Created by: Jess Gallo
# Date created: 01/19/2024
# Last modified: 01/19/2024
# Description: Function for adding books to the user's database


from datetime import datetime
from uuid import uuid4


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
    # SQL query to check if the book already exists in the database
    book_query = "SELECT * FROM books WHERE title = %s AND pages = %s AND date_published = %s"
    qvalues = (title, pages, date_published)
    query = book_query
    return execute_sql_query(query, qvalues)


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
    author_query = "SELECT * FROM authors WHERE author_fname = %s AND author_lname = %s"
    qvalues = (author_fname, author_lname)
    query = author_query
    return execute_sql_query(query, qvalues)


def check_genre_exists(genre):
    """
        Checks if author exists in database (genre table) using genre variable

        Parameters:
            genre (str): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    # SQL query to check if the author already exists in the database
    genre_query = "SELECT * FROM genre WHERE genre = %s"
    qvalues = (genre,)
    query = genre_query
    return execute_sql_query(query, qvalues)


def check_publisher_exists(publisher):
    """
        Checks if author exists in database (publisher table) using publisher variable

        Parameters:
            publisher (str): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    # SQL query to check if the author already exists in the database
    publisher_query = "SELECT * FROM publisher WHERE publisher = %s"
    qvalues = (publisher,)
    query = publisher_query
    return execute_sql_query(query, qvalues)


def check_series_exists(series):
    """
        Checks if author exists in database (series table) using series variable

        Parameters:
            series (str): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    # SQL query to check if the author already exists in the database
    series_query = "SELECT * FROM series WHERE series = %s"
    qvalues = (series,)
    query = series_query
    return execute_sql_query(query, qvalues)


def handle_book_exists(book_query_value):
    """
        Checks if books exists in database (account_books) using the book_query_value which produces the bID (book ID)

        Parameters:
            book_query_value (str): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    # Check if book exists in account books table
    account_books_query = "SELECT * FROM account_books WHERE bID = %s"
    qvalues = (book_query_value,)
    account_books_query_value = execute_sql_query(account_books_query, qvalues)

    # If the book is not associated with the user
    if not account_books_query_value:
        # Inserts book into account_books table
        account_books_insert = "INSERT INTO account_books (uID, bID) VALUES (%s, %s);"
        ivalues = (session['uID'], book_query_value)
        insert_data(account_books_insert, ivalues)
        print("Book added to account: ", book_query_value)
    # If user already inputed the book
    else:
        print('Book already associated with account!')

    return book_query_value


def handle_author_exists(author_query_value):
    """
        Checks if books exists in database (account_books) using the book_query_value which produces the bID (book ID)

        Parameters:
            author_query_value (str): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    # Check if book exists in account books table
    account_books_query = "SELECT * FROM account_books WHERE bID = %s"
    qvalues = (author_query_value,)
    account_books_query_value = execute_sql_query(account_books_query, qvalues)

    # If the book is not associated with the user
    if not account_books_query_value:
        # Inserts book into account_books table
        account_books_insert = "INSERT INTO account_books (uID, bID) VALUES (%s, %s);"
        ivalues = (session['uID'], author_query_value)
        insert_data(account_books_insert, ivalues)
    return author_query_value
