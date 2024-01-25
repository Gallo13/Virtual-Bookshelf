# Created by: Jess Gallo
# Date created: 01/19/2024
# Last modified: 01/24/2024
# Description: Function for adding books to the user's database


from database import establish_database_connection, execute_sql_query, insert_data

# -- CHECKING IN DATA EXISTS IN DATABASE -- #


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


# -- HANDLING DATA EXISTS IN DATABASE (INSERTS INTO DATABASE) -- #


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
        Checks if authors exists in database with book (book_author) using the author_query_value which produces the bID (book ID)

        Parameters:
            author_query_value (str): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    # Check if book exists in book_author table
    book_author_query = "SELECT * FROM book_author WHERE aID = %s"
    qvalues = (author_query_value,)
    book_author_query_value = execute_sql_query(book_author_query, qvalues)

    # If the book is not associated with the user
    if not book_author_query_value:
        # Inserts book into account_books table
        book_author_insert = "INSERT INTO book_author (aID, bID) VALUES (%s, %s);"
        ivalues = (session['uID'], author_query_value)
        insert_data(book_author_insert, ivalues)
    else:
        print('Author already associated with account!')

    return author_query_value


def handle_genre_exists(genre_query_value):
    """
        Checks if genre exists in database (book_genres) using the genre_query_value which produces the bID (book ID)

        Parameters:
            genre_query_value (str): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    # Check if book exists in book_author table
    book_genre_query = "SELECT * FROM book_author WHERE aID = %s"
    qvalues = (genre_query_value,)
    book_genre_query_value = execute_sql_query(book_genre_query, qvalues)

    # If the book is not associated with the user
    if not book_genre_query_value:
        # Inserts book into account_books table
        book_genre_insert = "INSERT INTO book_genre (gID, bID) VALUES (%s, %s);"
        ivalues = (session['uID'], genre_query_value)
        insert_data(book_genre_insert, ivalues)
    return genre_query_value


def handle_publisher_exists(publisher_query_value):
    """
        Checks if publisher exists in database (book_publisher) using the publisher_query_value which produces the bID (book ID)

        Parameters:
            publisher_query_value (str): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    # Check if book exists in book_author table
    book_publisher_query = "SELECT * FROM book_publisher WHERE pID = %s"
    qvalues = (publisher_query_value,)
    book_publisher_query_value = execute_sql_query(book_publisher_query, qvalues)

    # If the book is not associated with the user
    if not book_publisher_query_value:
        # Inserts book into account_books table
        book_publisher_insert = "INSERT INTO book_publisher (pID, bID) VALUES (%s, %s);"
        ivalues = (session['uID'], publisher_query_value)
        insert_data(book_publisher_insert, ivalues)
    return publisher_query_value


def handle_series_exists(series_query_value):
    """
        Checks if series exists in database (book_series) using the series_query_value which produces the bID (book ID)

        Parameters:
            series_query_value (str): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    # Check if book exists in book_author table
    book_series_query = "SELECT * FROM book_series WHERE sID = %s"
    qvalues = (series_query_value,)
    book_series_query_value = execute_sql_query(book_series_query, qvalues)

    # If the book is not associated with the user
    if not book_series_query_value:
        # Inserts book into account_books table
        book_series_insert = "INSERT INTO book_series (sID, bID) VALUES (%s, %s);"
        ivalues = (session['uID'], series_query_value)
        insert_data(book_series_insert, ivalues)
    return series_query_value

# -- UPDATES DATA IN DATABASE -- #


def update_read_data(rating):
    """
        Updates read data in database (books) using the rating variable

        Parameters:
            rating (int): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    # SQL query to update read data in account_books table
    rating_update = "UPDATE books SET rating = %s WHERE bID = %s;"
    uvalues = (rating, session['bID'])
    query = rating_update
    return execute_sql_query(query, uvalues)


def update_series_data(series_num):
    """
        Updates series data in database (books) using the series_num variable

        Parameters:
            series_num (int): The values to be queried from database

        Returns:
            result (list): The result of the query execution.
    """
    # SQL query to update series data in account_books table
    series_update = "UPDATE books SET number_in_series = %s WHERE bID = %s;"
    uvalues = (series_num, session['bID'])
    query = series_update
    return execute_sql_query(query, uvalues)
