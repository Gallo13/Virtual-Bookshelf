# Created by: Jess Gallo
# Created date: 09/01/2023
# Last Modified: 03/04/2023
# Description: Virtual Bookshelf Webapp/Storage
# Python, Flask, MySQL

# CHANGE WHERE msg messages go! make into popup!
# add barcode scanner
# add book cover scanner
# add

# Libraries
import re
import os

from flask import Flask, render_template, request, send_from_directory
from datetime import datetime


from charts import *
from add_book import *
from account_login import *
from barcode_scanner import *


# auth = Flask(__name__, template_folder='Templates', static_folder='static')
auth = Flask(__name__, template_folder='templates')
auth.secret_key = os.getenv('SECRET_KEY')


# Add the function by name to the jinja environment.
auth.jinja_env.globals.update(top_books=top_books)
auth.jinja_env.globals.update(top_authors=top_authors)
auth.jinja_env.globals.update(oldest_books=oldest_books)
auth.jinja_env.globals.update(longest_series=longest_series)
auth.jinja_env.globals.update(top_genres=top_genres)

main = 'index.html'
login = 'login.html'


# ======================================================================================================================


@auth.route('/', methods=['GET', 'POST'])
def home():
    session['loggedin'] = False
    return render_template(main)


# Creates static file path for images
@auth.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)


# ======================================================================================================================


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Stores email and password into variables
        email = request.form['email']
        password = request.form['password']

        # Retrieve the hashed password
        hash_pw = hash_password(password, auth.secret_key)

        # Check if account exists using MySQL
        login_query_value = check_account_exists(email, hash_pw)

        # If account does not exist in accounts table in the database
        if not login_query_value:
            # Account doesn't exist or email/password incorrect
            msg = "Incorrect email/password"
            return render_template(main, msg=msg)

        # if account exists in accounts table in the database
        else:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['email'] = email
            session['uID'] = login_query_value

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
    return render_template(main, msg=msg)


# ======================================================================================================================


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Check if "email", "password" POST requirements exist (user submitted form)
    if request.method == 'POST':
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        # Check if account exists using MySQL
        account_query_value = check_account_exists(email, password)

        # If account exists show error and validation checks
        if account_query_value is not None:
            msg = 'Account already exists!'
            return render_template(main, msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            return render_template(main, msg=msg)
        elif not email or not password:
            msg = 'Please fill out the form!'
            return render_template(main, msg=msg)
        elif password != password2:
            msg = 'Passwords do not match'
            return render_template(main, msg=msg)
        else:
            # Hash the password
            hash_pw = hash_password(password, auth.secret_key)

            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            insert_account_data(email, hash_pw)
            print("Account Added:, ", email, hash_pw)
            msg = 'You have successfully registered! Please login!'
            return render_template(main, msg=msg)

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
        return render_template(main, msg=msg)


# ======================================================================================================================


# route decorator to tell Flask what URL should trigger function
@auth.route('/get_data', methods=['POST'])
def get_data():
    # get user input
    isbn = request.form['isbn']
    title = request.form['title']
    author_fname = request.form['author_fname']
    author_lname = request.form['author_lname']
    genre = request.form['genre']
    publisher = request.form['publisher']
    pages = request.form['pages']
    date_added = datetime.now().date().strftime('%Y-%m-%d')
    date_published = request.form['date_published']
    read_checkbox = request.form.get('read_checkbox')
    rating = request.form.get('rating')
    series_checkbox = request.form.get('series_checkbox')
    series = request.form.get('series')
    number_in_series = request.form.get('seriesNum')

    if rating == '' or number_in_series == '':
        number_in_series = None
        rating = None
    else:
        rating = int(rating)
        number_in_series = int(number_in_series)

    # Checks if user is logged in (if user is not logged in)
    if session['loggedin'] is False:
        msg = 'Please login to add your book!'
        return render_template(main, msg=msg)

    # If user is logged in
    if request.method == 'POST' and session['loggedin'] is True:
        # Checks if form is filled out
        if not any([isbn, title, author_fname, author_lname, genre, publisher, pages, date_published]):
            msg = 'Please fill out the form!'
            return render_template(login, msg=msg)

        try:
            # new session['uID'] only for querying during get_data()
            session['uID2'] = session['uID'][0]

            # -- BOOK ----------------------------------------------
            # Checks if book already exists in database (books table) - executes SELECT statement
            book_query_value = check_book_exists(isbn)
            # If book exists in database (books table)
            if book_query_value is not None:
                session['bID'] = book_query_value
                # Checks if book is associated with user and if it is not, it insert it into account_books tables
                insert_account_books()
            else:
                # If book does not exist in database (books table) then we need to insert the book into the database.
                # Insert book into database
                ivalue = (isbn, title, int(pages), rating, date_added, date_published, number_in_series)
                insert_book(ivalue)
                # Checks for updated book in DB
                book_query_value = check_book_exists(isbn)
                session['bID'] = book_query_value
                # Adds book to user (bID into account_books table)
                insert_account_books()

                # -- AUTHOR -----------------------------
                # Checks if author is already in database (authors table) - executes SELECT statement
                author_query_value = check_author_exists(author_fname, author_lname)
                # If author in database but needs to be associated with the new book
                if author_query_value:
                    # Checks if author is associated with the book and if not, it insert it into book_authors table
                    insert_book_author(author_query_value)
                else:
                    # Insert author into database
                    ivalue = (str(uuid4()), author_fname, author_lname)
                    insert_author(ivalue)
                    # Checks for updated author in DB
                    author_query_value = check_author_exists(author_fname, author_lname)
                    # Insert author into book_authors table (register author under current book)
                    insert_book_author(author_query_value)

                # -- GENRE -----------------------------
                # Checks if there are multiple genres inputted
                if ',' in genre:
                    # Separates string at comma and creates a string
                    genre_split = [x.strip() for x in genre.split(',')]
                    for g in genre_split:
                        # change name to genre to not make a new function
                        genre = g
                        genre_query_value = check_genre_exists(genre)
                        if genre_query_value:
                            # Checks if genre is associated with the book and if it is not, it insert it
                            # into book_genres table
                            insert_book_genre(genre_query_value)
                        else:
                            # Insert author into database
                            ivalue = (str(uuid4()), genre)
                            insert_genre(ivalue)
                            # Checks for updated genre in DB
                            genre_query_value = check_genre_exists(genre)
                            # Insert genre into book_genres table (register genre under current book)
                            insert_book_genre(genre_query_value)
                # If there is only one genre inputted
                else:
                    # Checks if genre is already in database
                    genre_query_value = check_genre_exists(genre)
                    # If genre in database but needs to be associated with the new book
                    if genre_query_value:
                        # Checks if genre is associated with the book and if not, it insert it into book_genres table
                        insert_book_genre(genre_query_value)
                    else:
                        # Insert genre into database
                        ivalue = (str(uuid4()), genre)
                        insert_genre(ivalue)
                        # Checks for updated genre in DB
                        genre_query_value = check_genre_exists(genre)
                        # Insert genre into book_genres table (register genre under current book)
                        insert_book_genre(genre_query_value)

                # -- PUBLISHER -----------------------------
                # Checks if publisher is already in database
                publisher_query_value = check_publisher_exists(publisher)
                # If publisher in database but needs to be associated with the new book
                if publisher_query_value:
                    # Checks if publisher is associated with the book and if it is not,
                    # it insert it into book_publisher table
                    insert_book_publisher(publisher_query_value)
                else:
                    # Insert publisher into database
                    ivalue = (str(uuid4()), publisher)
                    insert_publisher(ivalue)
                    # Checks for updated publisher in DB
                    publisher_query_value = check_publisher_exists(publisher)
                    # Insert genre into book_genres table (register genre under current book)
                    insert_book_publisher(publisher_query_value)

                # -- Series ----------------------------------------------
                # Updates series of books if user has series checked
                if series_checkbox != 'None' and series != '':
                    # Checks if series already exists
                    series_query_value = check_series_exists(series)
                    # If series exists but needs to be associated with the new book
                    if series_query_value:
                        # Checks if series is associated with the book and if not, it insert it into book_series table
                        insert_book_series(series_query_value)
                        update_series(number_in_series)
                    else:
                        # Insert series into database
                        ivalue = (str(uuid4()), series)
                        insert_series(ivalue)
                        # Checks for updated series in DB
                        series_query_value = check_series_exists(series)
                        # Insert genre into book_genres table (register genre under current book)
                        insert_book_series(series_query_value)
                        update_series(number_in_series)

                # -- READ ----------------------------------------------
                # Updates rating of books if user has read checked
                # if read_checkbox == 'True' and rating != '':
                if read_checkbox != 'None' and rating is not None:
                    update_read(rating)
        finally:
            # Clears session['bID'] - not sure if I really need this - will try with and without
            session['bID'] = None
            return render_template(login)


@auth.route('/scan_barcode', methods=['GET', 'POST'])
def scan_barcode():
    print('You clicked the barcode')
    if request.method == 'POST':
        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()
        barcode_read = False
        while ret and not barcode_read:
            ret, frame = camera.read()
            frame, barcode_read, isbn = read_barcode(frame)
            cv2.imshow('Real Time Barcode Scanner', frame)
            if barcode_read:
                print("ISBN: ", isbn)
                break
            elif cv2.waitKey(1) & 0xFF == 27:
                break

        camera.release()
        cv2.destroyAllWindows()
    return render_template(login)


if __name__ == '__main__':
    auth.run(debug=True)
