# Created by: Jess Gallo
# Created date: 09/01/2023
# Last Modified: 01/24/2023
# Description: Virtual Bookshelf Webapp/Storage
# Python, Flask, MySQL

# CHANGE WHERE msg messages go! make into popup!
# Put cursor.commit() for inserts or have different insert function

# Libraries
import hashlib
import re

from flask import Flask, Blueprint, render_template, redirect, url_for, request, session
from datetime import datetime
from uuid import uuid4

from database import establish_database_connection, execute_sql_query, insert_data
from charts import top_books, top_authors, oldest_books, longest_series, top_genres
from add_book import check_book_exists, check_author_exists, check_genre_exists, check_publisher_exists, \
    check_series_exists, handle_book_exists, handle_author_exists, handle_genre_exists, handle_publisher_exists, \
    handle_series_exists, update_read_data, update_series_data

auth = Flask(__name__, template_folder='HTML', static_folder='')
# Secret key for extra protection
auth.secret_key = '85002040'

# Add the function by name to the jinja environment.
auth.jinja_env.globals.update(top_books=top_books)
auth.jinja_env.globals.update(top_authors=top_authors)
auth.jinja_env.globals.update(oldest_books=oldest_books)
auth.jinja_env.globals.update(longest_series=longest_series)
auth.jinja_env.globals.update(top_genres=top_genres)

# ======================================================================================================================


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
        qvalues = email, password

        login_query_value = execute_sql_query(query, qvalues)
        print(login_query_value)

        # If account does not exist in accounts table in the database
        if not login_query_value:
            # Account doesn't exist or email/password incorrect
            msg = "Incorrect email/password"
            return render_template('index.html', msg=msg)

        # if account exists in accounts table in the database
        else:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['email'] = email
            session['uID'] = login_query_value[0]

        login_html = 'login.html'
        return render_template(login_html)

# ==================================================================================================================


@auth.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('email', None)
    session.pop('uID', None)
    session['loggedin'] = False
    msg = 'You have successfully logged out'
    main = 'index.html'
    return render_template(main, msg=msg)

# ======================================================================================================================


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Check if "email", "password" POST requirements exist (user submitted form)
    if request.method == 'POST':
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']

        # Check if account exists using MySQL
        query = "SELECT * FROM accounts WHERE email = %s"
        qvalues = email
        account_query_value = execute_sql_query(query, qvalues)

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
            query = "INSERT INTO accounts VALUES (%s, %s, %s)"
            qvalues = (str(uuid4()), email, password)
            execute_sql_query(query, qvalues)
            print("Account Added:, ", email, password)
            msg = 'You have successfully registered! Please login!'
            return render_template('index.html', msg=msg)

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
        return render_template('index.html', msg=msg)

# ======================================================================================================================


# route decorator to tell Flask what URL should trigger function
@auth.route('/get_data', methods=['POST'])
def get_data():
    # get user input
    title = request.form['title']
    author_fname = request.form['author_fname']
    author_lname = request.form['author_lname']
    genre = request.form['genre']
    publisher = request.form['publisher']
    pages = request.form['pages']
    date_added = datetime.now().date().strftime('%Y-%m-%d')
    date_published = request.form['date_published']
    rating = request.form.get('rating', None)
    read_checkbox = request.form.get('read_checkbox', False)
    number_in_series = request.form.get('series_num', None)
    series_checkbox = request.form.get('series_checkbox', False)

    # Checks if user is logged in (if user is not logged in)
    if session['loggedin'] is False:
        msg = 'Please login to add your book!'
        home_html = 'index.html'
        return render_template(home_html, msg=msg)

    # If user is logged in
    if request.method == 'POST' and session['loggedin'] is True:
        # Checks if form is filled out
        # if not title or not author_fname or not author_lname or not genre or not publisher or not pages
        # or not date_published:
        if not any([title, author_fname, author_lname, genre, publisher, pages, date_published]):
            msg = 'Please fill out the form!'
            login_html = 'login.html'
            return render_template(login_html, msg=msg)

        """ 
        If book exists in database (from other user) then information about author, genre, publisher, and series 
        are done and the only thing we need to do is check if it is associated with the current user (meaning if they 
        already inputted the book) and if they didn't we will add the book to the user (bID into account_books table)
        """

        # -- BOOK ----------------------------------------------
        # Checks if book already exists in database (books table)
        book_query_value = check_book_exists(title, pages, date_published)
        # If book exists in database (books table) but not associated with user
        if book_query_value:
            print("Book already exists: ", title, book_query_value[0])
            # Checks if book is associated with user and if it is not, it insert it into account_books tables
            handle_book_exists(book_query_value[0])

        """
         If book does not exist in database (books table) then we need to insert the book into the database.
        """
        # Insert book into database
        ivalue = (str(uuid4()), title, int(pages), rating, date_added, date_published, number_in_series)
        book_value = insert_book(insert, ivalue)
        print('Book added: ', title, book_value[0])

        # Insert book into account_books table (register book under current user)
        ivalue = (session['uID'], book_value[0])
        account_books_value = insert_account_books(query, ivalue)
        print('Book added to account: ', title, account_books_value[0])

        # -- AUTHOR -----------------------------
        # Checks if author is already in database
        author_query_value = check_author_exists(author_fname, author_lname)
        # If author in database but needs to be associated with the new book
        if author_query_value:
            print("Author already exists: ", author_fname, author_lname, author_query_value[0])
            # Checks if author is associated with the book and if it is not, it insert it into account_books table
            handle_author_exists(author_query_value[0])
        else:
            # Insert author into database
            insert_book_author(author_query_value)
            print("Author added: ", author_fname, author_lname, author_query_value[0])
            # Insert author into book_authors table (register author under current book)
            handle_author_exists(author_query_value[0])

        # -- GENRE -----------------------------
        # Checks if there are multiple genres inputted
        if ',' in genre:
            # Separates string at comma and creates a string
            genre_split = [x.strip() for x in genre.split(',')]
            for g in genre_split:
                genre_query_value = check_genre_exists(g)
                if genre_query_value:
                    print("Genre already exists: ", g, genre_query_value[0])
                    # Checks if genre is associated with the book and if it is not, it insert it into book_genres table
                    handle_genre_exists(genre_query_value[0])
                else:
                    # Insert genre into database
                    insert_book_genre(genre_query_value)
                    print("Genre added: ", g, genre_query_value[0])
                    # Insert genre into book_genres table (register genre under current book)
                    handle_genre_exists(genre_query_value[0])
        # If there is only one genre inputted
        else:
            # Checks if genre is already in database
            genre_query_value = check_genre_exists(genre)
            # If genre in database but needs to be associated with the new book
            if genre_query_value:
                print("Genre already exists: ", genre, genre_query_value[0])
                # Checks if genre is associated with the book and if it is not, it insert it into book_genres table
                handle_genre_exists(genre_query_value[0])
            else:
                # Insert author into database
                insert_book_genre(genre_query_value)
                print("Genre added: ", genre, genre_query_value[0])
                # Insert genre into book_genres table (register genre under current book)
                handle_genre_exists(genre_query_value[0])

        # -- PUBLISHER -----------------------------
        # Checks if publisher is already in database
        publisher_query_value = check_publisher_exists(publisher)
        # If publisher in database but needs to be associated with the new book
        if publisher_query_value:
            print("Publisher already exists: ", publisher, publisher_query_value[0])
            # Checks if publisher is associated with the book and if it is not, it insert it into book_publisher table
            handle_publisher_exists(publisher_query_value[0])
        else:
            # Insert publisher into database
            insert_book_publisher(publisher_query_value)
            print("Publisher added: ", publisher, publisher_query_value[0])
            # Insert genre into book_genres table (register genre under current book)
            handle_publisher_exists(publisher_query_value[0])

        # -- READ ----------------------------------------------
        # Updates rating of books if user has read checked
        if read_checkbox:
            update_read_data(rating)
            print("Rating updated: ", rating)
        else:
            pass

        # -- Series ----------------------------------------------
        # Updates series of books if user has series checked
        if series_checkbox:
            # Checks if series already exists
            series_query_value = check_series_exists(series)
            # If series exists but needs to be associated with the new book
            if series_query_value:
                print("Series already exists: ", series, series_query_value[0])
                # Checks if series is associated with the book and if it is not, it insert it into book_series table
                handle_series_exists(series_query_value[0])
            else:
                # Insert series into database
                insert_book_series(series_query_value)
                print("Series added: ", series, series_query_value[0])
                # Insert genre into book_genres table (register genre under current book)
                handle_series_exists(series_query_value[0])

                # Updates series number of books if user has series checked
                # Gets the series number of the series that the book is associated with
                series_query_value = check_series_exists(series)
                # Gets the series number of the series that the book is associated with
                series_num = series_query_value[0]
                print("Series number: ", series_num)

                update_series_data(series, series_num)
                print("Series updated: ", series)
        # If series isn't checked off, we can leave the values as NULL
        else:
            pass

        msg = 'Book added successfully!'
        login_html = 'login.html'
        return render_template(login_html, msg=msg)

    """
            if series_checkbox:
                series = request.form['series']
                series_num = request.form['seriesNum']
            else:
                series = None
                series_num = None

            print(rating, series, series_num)

            try:

            
            except mysql.connector.Error as err:
                # Handles Errors and gives the error codes to let us know what the issue is
                print(err)
                print("Error Code: ", err.errno)
                print("SQLSTATE: ", err.sqlstate)
                print("Message: ", err.msg)
            finally:
                return render_template(login_html)
    """


if __name__ == '__main__':
    auth.run(debug=True)
