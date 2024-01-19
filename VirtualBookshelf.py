# Created by: Jess Gallo
# Created date: 09/01/2023
# Last Modified: 01/18/2023
# Description: Virtual Bookshelf Webapp/Storage
# Python, Flask, MySQL

# CHANGE WHERE msg messages go! make into popup!
# Put cursor.commit() for inserts or have different insert function

# Libraries
import hashlib
import re
from datetime import datetime
from uuid import uuid4

from database import establish_database_connection, execute_sql_query
from charts import top_books, top_authors, oldest_books, longest_series, top_genres

from flask import Flask, Blueprint, render_template, flash, url_for, request, session, jsonify
# import pandas as pd
# from dash import html

auth = Flask(__name__, template_folder='HTML', static_folder='')
# Secret key for extra protection
auth.secret_key = '85002040'


def get_form_request():
    title = request.form['title']
    author_fname = request.form['author_fname']
    author_lname = request.form['author_lname']
    genre = request.form['genre']
    genre_split = None
    publisher = request.form['publisher']
    pages = request.form['pages']
    read_checkbox = request.form.get('read_checkbox', False)
    series_checkbox = request.form.get('series_checkbox', False)
    date_added = datetime.now().date().strftime('%Y-%m-%d')
    date_published = request.form['date_published']

    print(title, author_fname, author_lname, genre, genre_split, publisher, pages, read_checkbox, series_checkbox,
          date_added, date_published)

    return (title, author_fname, author_lname, genre, genre_split, publisher, pages,
            read_checkbox, series_checkbox, date_added, date_publishe)


# Add the function by name to the jinja environment.
auth.jinja_env.globals.update(top_books=top_books)
auth.jinja_env.globals.update(top_authors=top_authors)
auth.jinja_env.globals.update(oldest_books=oldest_books)
auth.jinja_env.globals.update(longest_series=longest_series)
auth.jinja_env.globals.update(top_genres=top_genres)


@auth.route('/', methods=['GET', 'POST'])
def home():
    session['loggedin'] = False
    return render_template('index.html')


# ======================================================================================================================


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Stores email and password into variables
        email = request.form['email']
        password = request.form['password']

        # Retrieve the hashed password
        hash_pw = password + auth.secret_key
        hash_pw = hashlib.sha1(hash_pw.encode())
        password = hash_pw.hexdigest()

        # Check if account exists using MySQL
        query = "SELECT uID FROM accounts WHERE email = %s AND password = %s;"
        values = email, password

        login_query_value = execute_sql_query(query, values)
        print(login_query_value)

        # If account does not exist in accounts table in the database
        if not login_query_value:
            # Account doesn't exist or email/password incorrect
            msg = "Incorrect email/password"
            return render_template('index.html', msg=msg)

        # CREATE LOGIN HTML ===========================================================================================
        # if account exists in accounts table in the database
        else:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['email'] = email
            session['uID'] = login_query_value[0]

        return render_template('login.html')

    # ==================================================================================================================


@auth.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('email', None)
    session.pop('uID', None)
    session['loggedin'] = False
    msg = 'You have successfully logged out'
    return render_template('index.html', msg=msg)


# ======================================================================================================================


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Check if "email", "password" POST requirements exist (user submitted form)
    if request.method == 'POST':
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']

        # Check if account exists using MySQL
        query = """SELECT * FROM accounts WHERE email = '%s'"""
        values = email
        # was originally fetchone()
        account_query_value = execute_sql_query(query, values)

        # If account exists show error and validation checks
        if account_query_value:
            msg = 'Account already exists!'
            return render_template('index.html', msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            return render_template('index.html', msg=msg)
        elif not email or not password:
            msg = 'Please fill out the form!'
            return render_template('index.html', msg=msg)
        else:
            # Hash the password
            hash_pw = password + auth.secret_key
            hash_pw = hashlib.sha1(hash_pw.encode())
            password = hash_pw.hexdigest()

            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            insert = """INSERT INTO accounts VALUES ('%s', '%s', '%s')"""
            values = (str(uuid4()), email, password)
            insert_sql_query(insert, values)
            print("Account Added:, ", email, password)
            cursor.close()
            mydb.close()
            msg = 'You have successfully registered! Please login!'
            return render_template('index.html', msg=msg)

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
        return render_template('index.html', msg=msg)

    # Show registration form with message (if any)
    # return render_template('login.html', msg=msg)


# ======================================================================================================================


# route decorator to tell Flask what URL should trigger function
@auth.route('/get_data', methods=['GET', 'POST'])
def get_data():
    author_insert_value = None
    publisher_insert_value = None
    genre_insert_value = None
    series_insert_value = None
    book_value = None

    get_form_requests()

    if session['loggedin'] is False:
        msg = 'Please login to add your book!'
        return render_template('index.html', msg=msg)
    elif request.method == 'POST' and session['loggedin'] is True:
        # Checks if form is filled out
        if (title not in request.form or author_fname not in request.form or author_lname not in request.form or
                genre not in request.form or publisher not in request.form or pages not in request.form or
                date_published not in request.form):
            msg = 'Please fill out the form!'
            return render_template('login.html', msg=msg)
        else:
            # Checks if there are multiple genres associated with the book
            # Checks if there is a comma in the string
            if ',' in genre:
                # Separates string at comma and creates a string
                genre_split = [x.strip() for x in genre.split(',')]
            else:
                pass

            if read_checkbox:
                rating = request.form['rating']
            else:
                rating = None

            if series_checkbox:
                series = request.form['series']
                series_num = request.form['seriesNum']
            else:
                series = None
                series_num = None

            print(rating, series, series_num)

            try:
                # BOOK TITLE ------------------------------------------------------------------------------------------
                # SQL query to check if book exists
                book_query = """SELECT bID FROM books WHERE title='%s' AND pages=%s;"""
                values = (title, int(pages))
                query = book_query
                book_query_value = execute_sql_query(query, values)
                if not book_query_value:
                    # Inserts book into database
                    book_insert = """INSERT INTO books 
                                     (bID, title, pages, rating, number_in_series, date_added, date_published) 
                                     VALUES ('%s', '%s', %s, '%s', %s, '%s', '%s');"""
                    values = (str(uuid4()), title, int(pages), rating, series_num, date_added, date_published)
                    query = book_insert
                    execute_sql_query(query, values)

                    # Executes query
                    book_insert_value = execute_sql_query(book_query, values)
                    print("Book added: ", title, book_insert_value)

                    # Storing in new variables to change list/tuple to single string
                    book_value = book_insert_value[0]
                    print("Book_ID: ", book_value)

                    # Inserts book into account_books table
                    account_books_insert = """INSERT INTO account_books VALUES ('%s', '%s');"""
                    values = (session['uID'], book_value)
                    query = account_books_insert
                    execute_sql_query(query, values)
                    print("Book added to account: ", title, book_query_value)

                    # AUTHOR NAME --------------------------------------------------------------------------------------
                    # Query to check if author exists
                    author_query = """SELECT aID FROM authors WHERE firstname = '%s' AND lastname = '%s';"""
                    values = (author_fname, author_lname)
                    query = author_query
                    author_query_value = execute_sql_query(query, values)
                    # Checks if author exists
                    if not author_query_value:
                        # Inserts author into database
                        authors_insert = """INSERT INTO authors (aID, firstname, lastname) 
                                            VALUES ('%s', '%s', '%s');"""
                        values = (str(uuid4()), author_fname, author_lname)
                        query = authors_insert
                        execute_sql_query(query, values)
                        # Stores query results into variable
                        execute_sql_query(author_query, values)
                        print("Author added: ", author_fname, author_lname, author_insert_value)

                    else:
                        print("Author already exists", author_fname, author_lname, author_query_value)

                    # BOOK AUTHOR---------------------------------------------------------------------------------------
                    # Takes book ID and stores it into book_value
                    # Storing in new variables to change list/tuple to single string
                    book_value = book_insert_value[0]
                    print("Book_ID: ", book_value)

                    # Uses inserted author value is author was created
                    if not author_query_value:  # if author is inserted
                        author_value = author_insert_value[0]
                        print("Author_ID: ", author_value)
                    # Uses the queried author if author exists already
                    else:
                        author_value = author_query_value[0]
                        print("Author_ID: ", author_value)

                    # Inserts aID and bID into book_author table
                    book_author_insert = """INSERT INTO book_author (bID, aID) VALUES ('%s', '%s')"""
                    values = (book_value, author_value)
                    query = book_author_insert
                    execute_sql_query(query, values)

                    # Checks to make sure book_author is in database
                    book_author_query = """SELECT DISTINCT bID, aID FROM book_author WHERE bID = '%s' AND aID = '%s'"""
                    values = (book_value, author_value)
                    query = book_author_query
                    book_author_value = execute_sql_query(query, values)
                    print("Book_Author added", book_author_value)

                    # PUBLISHER NAME -----------------------------------------------------------------------------------
                    # Query to check if publisher exists`
                    publisher_query = """SELECT pID FROM publisher WHERE publisher = '%s'"""
                    values = publisher
                    query = publisher_query
                    publisher_query_value = execute_sql_query(query, values)

                    # Checks if publisher exists
                    if not publisher_query_value:
                        # Inserts publisher into database
                        publisher_insert = """INSERT INTO publisher (pID, publisher) VALUES ('%s', '%s');"""
                        values = (str(uuid4()), publisher)
                        query = publisher_insert
                        execute_sql_query(query, values)
                        print("Publisher added", publisher_insert_value)
                    else:
                        print("Publisher already exists", publisher_query_value)

                    # BOOK PUBLISHER -----------------------------------------------------------------------------------
                    # Uses publisher_insert_value if publisher doesn't already exist
                    if not publisher_query_value:
                        publisher_value = publisher_insert_value[0]
                        print("Publisher_ID: ", publisher_value)
                    # Uses publisher_query_value if publisher exists
                    else:
                        publisher_value = publisher_query_value[0]
                        print("Publisher_ID: ", publisher_value)

                    # Inserts bID and pID into book_publisher table
                    book_publisher_insert = """INSERT INTO book_publisher (bID, pID) VALUES ('%s', '%s')"""
                    value = (book_value, publisher_value)
                    query = book_publisher_insert
                    execute_sql_query(query, value)

                    # Checks to make sure book_publisher is in database
                    book_publisher_query = """SELECT DISTINCT bID, pID FROM book_publisher 
                                            WHERE bID = '%s' AND pID = '%s'"""
                    values = (book_value, publisher_value)
                    query = book_publisher_query
                    book_publisher_value = execute_sql_query(query, values)
                    print("Book_Publisher added", book_publisher_value)

                    # GENRE --------------------------------------------------------------------------------------------
                    # Uses single genre
                    if not genre_split:
                        # Query to check if genre exists
                        genre_query = """SELECT gID FROM genre WHERE genre = '%s'"""
                        values = genre
                        query = genre_query
                        genre_query_value = execute_sql_query(query, values)

                        # Checks if genre exists
                        if not genre_query_value:
                            # Inserts genre into database
                            genres_insert = """INSERT INTO genre (gID, genre) VALUES ('%s', '%s');"""
                            values = (str(uuid4()), genre)
                            query = genres_insert
                            execute_sql_query(query, values)
                            genre_insert_value = cursor.execute(genres_insert)
                            print("Genre added", genre_insert_value)
                        else:
                            print("Genre already exists", genre_query_value)

                        # BOOK GENRE -----------------------------------------------------------------------------------
                        # Uses genre_insert_value if genre_query_value is None
                        if not genre_query_value:
                            genre_value = genre_insert_value[0]
                            print("Genre_ID: ", genre_value)
                        # Uses genre_query_value if genre exists
                        else:
                            genre_value = genre_query_value[0]
                            print("Genre_ID: ", genre_value)

                        # Inserts bID and gID into book_genre table
                        book_genre_insert = """INSERT INTO book_genre (bID, gID) VALUES ('%s', '%s')"""
                        values = (book_value, genre_value)
                        query = book_genre_insert
                        execute_sql_query(query, values)

                        # Checks to make sure book_genre is in database
                        book_genre_query = """SELECT DISTINCT bID, gID FROM book_genre 
                                            WHERE bID = '%s' AND gID = '%s'"""
                        values = (book_value, genre_value)
                        query = book_genre_query
                        book_genre_value = execute_sql_query(query, values)
                        print("Book_Genre added", book_genre_value)

                    # Uses genre_split that is a list
                    else:
                        for g in genre_split:
                            # Query to check if genre exists
                            genre_query = """SELECT gID FROM genre WHERE genre = '%s'"""
                            values = g
                            query = genre_query
                            genre_query_value = execute_sql_query(query, values)

                            # Checks if genre exists
                            if not genre_query_value:
                                # Inserts genre into database
                                genres_insert = """INSERT INTO genre (gID, genre) VALUES ('%s', '%s');"""
                                values = (str(uuid4()), g)
                                query = genres_insert
                                genre_insert_value = cursor.execute(query, values)
                                print("Genre added", genre_insert_value)
                            else:
                                print("Genre already exists", genre_query_value)

                            # BOOK GENRE -------------------------------------------------------------------------------
                            # Uses genre_insert_value if genre_query_value is None
                            if not genre_query_value:
                                genre_value = genre_insert_value[0]
                                print("Genre_ID: ", genre_value)
                            # Uses genre_query_value if genre exists
                            else:
                                genre_value = genre_query_value[0]
                                print("Genre_ID: ", genre_value)

                            # Inserts bID and gID into book_genre table
                            book_genre_insert = """INSERT INTO book_genre (bID, gID) VALUES ('%s', '%s')"""
                            values = (book_value, genre_value)
                            query = book_genre_insert
                            execute_sql_query(query, values)

                            # Checks to make sure book_genre is in database
                            book_genre_query = """SELECT DISTINCT bID, gID 
                                                FROM book_genre WHERE bID = '%s' AND gID = '%s'"""
                            values = (book_value, genre_value)
                            query = book_genre_query
                            book_genre_value = execute_sql_query(query, values)
                            print("Book_Genre added", book_genre_value)

                    # SERIES NAME --------------------------------------------------------------------------------------
                    if not series:
                        mydb.commit()
                    else:
                        # Query to check if series exists
                        series_query = """SELECT sID FROM series WHERE seriesName = '%s';"""
                        values = series
                        query = series_query
                        series_query_value = execute_sql_query(query, values)
                        # Checks if series exists
                        if not series_query_value:
                            # Inserts series into database
                            series_insert = """INSERT INTO series (sID, seriesName) VALUES ('%s', '%s');"""
                            values = (str(uuid4()), series)
                            query = series_insert
                            series_insert_value = execute_sql_query(query, values)
                            print("Series added: ", series, series_insert_value)

                        else:
                            print("Series already exists", series, series_query_value)

                        # BOOK SERIES -- -------------------------------------------------------------------------------
                        # Uses series_insert_value if series_query_value is None
                        if not series_query_value:
                            series_value = series_insert_value[0]
                            print("Series_ID: ", series_value)
                        # Uses series_query_value if series exists
                        else:
                            series_value = series_query_value[0]
                            print("Series_ID: ", series_value)

                        # Inserts bID and sID into book_series table
                        book_series_insert = """INSERT INTO book_series (bID, sID) VALUES ('%s', '%s')"""
                        values = (book_value, series_value)
                        query = book_series_insert
                        execute_sql_query(query, values)

                        # Checks to make sure book_series is in database
                        book_series_query = """SELECT DISTINCT bID, sID FROM book_series 
                                                WHERE bID = '%s' AND sID = '%s'"""
                        values = (book_value, series_value)
                        query = book_series_query
                        book_series_value = execute_sql_query(query, values)
                        print("Book_Series added", book_series_value)

                        mydb.commit()
                else:
                    print("Book already exists", title, book_query_value)

                    # Checks if book exists in account books table to see if the account has the book associated with it
                    account_books_query = """SELECT * FROM account_books WHERE bID = '%s'"""
                    values = book_query_value
                    query = account_books_query
                    account_books_query_value = execute_sql_query(query, values)

                    if not account_books_query_value:
                        # Inserts book into account_books table
                        account_books_insert = """INSERT INTO account_books VALUES ('%s', '%s');"""
                        values = (session['uID'], book_value)
                        query = account_books_insert
                        execute_sql_query(query, values)
                        print("Book added to account: ", title, book_query_value)
                        cursor.close()
                        mydb.close()
                    else:
                        print('Book already associated with account!')
                        # mydb.close()
            except mysql.connector.Error as err:
                # Handles Errors and gives the error codes to let us know what the issue is
                print(err)
                print("Error Code: ", err.errno)
                print("SQLSTATE: ", err.sqlstate)
                print("Message: ", err.msg)
                # raise Exception("Could not connect to database")
                # return render_template('login.html')
            finally:
                cursor.close()
                mydb.close()
                # return render_template('login.html')


if __name__ == '__main__':
    auth.run(debug=True)
