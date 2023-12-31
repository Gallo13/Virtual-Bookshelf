# Created by: Jess Gallo
# Created date: 09/01/2023
# Last Modified: 11/20/2023
# Description: Virtual Bookshelf Webapp/Storage
# Python, Flask, MySQL

# CHANGE WHERE msg messages go! make into popup!

# Libraries
import hashlib
import re
from datetime import datetime
from uuid import uuid4

import mysql.connector
from flask import Flask, render_template, flash, url_for, request, session, jsonify
from mysql.connector.errors import Error
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.express as px
from dash import html

# from chart_studio.plotly import plot, iplot
# from chart_studio.grid_objs import GridDat

auth = Flask(__name__, template_folder='HTML', static_folder='')

# Connect to database
mydb = (mysql.connector.connect(
    host='localhost',
    user='root',
    password='####',
    database='virtual_bookshelf'
))

# Secret key for extra protection
auth.secret_key = '####'


def top_books():
    cursor = mydb.cursor()
    # Top 5 Books ----------------------------------------------------------------------------------------
    top_book_query = """SELECT b.title, a.firstname, a.lastname, b.rating
                        FROM books as b
                        JOIN account_books as ab ON b.bID = ab.bID 
                        JOIN book_author as ba ON b.bID = ba.bID
                        JOIN authors as a ON ba.aID = a.aID
                        WHERE uID = '%s' 
                        ORDER BY rating DESC LIMIT 5;""" % session['uID']
    cursor.execute(top_book_query)
    top_book_query_value = cursor.fetchall()
    # print(str(top_book_query_value)[0:300])

    # Convert SQL Query to Pandas Dataframe
    top_book_df = pd.DataFrame([[ij for ij in i] for i in top_book_query_value])
    top_book_df.columns = ['Title', 'First Name', 'Last Name', 'Rating']

    # Plotly Chart
    book_fig = px.bar(top_book_df,
                  x='Title',
                  y='Rating',
                  hover_data=['First Name', 'Last Name'],
                  labels={'x': 'Title', 'y': 'Rating'},
                  title="Your Top 5 Books",
                  orientation='h')
    book_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    # fig2.update_yaxes(autorange="reversed")

    top_book_plot = plot(book_fig, include_plotlyjs=False, output_type='div')

    return top_book_plot


def top_authors():
    cursor = mydb.cursor()
    # Most Read Author ----------------------------------------------------------------------------------------
    top_author_query = """ SELECT firstname, lastname, COUNT(lastname) as count
                           FROM authors
                           JOIN book_author ON authors.aID = book_author.aID
                           JOIN account_books ON book_author.bID = account_books.bID
                           WHERE account_books.uID = '%s'
                           GROUP BY firstname, lastname
                           ORDER BY count DESC
                           LIMIT 5;""" % session['uID']
    cursor.execute(top_author_query)
    top_author_query_value = cursor.fetchall()
    # print(str(top_author_query_value)[0:300])

    # Convert SQL Query to Pandas Dataframe
    top_author_df = pd.DataFrame([[ij for ij in i] for i in top_author_query_value])
    top_author_df.columns = ['First Name', 'Last Name', 'Count']

    # Plotly Chart
    author_fig = px.bar(top_author_df,
                  x='Count',
                  y='Last Name',
                  hover_data=['First Name'],
                  labels={'x': 'Count', 'y': 'Last Name'},
                  title="Your Top 5 Authors",
                  orientation='h')
    author_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    author_fig.update_yaxes(autorange="reversed")

    top_author_plot = plot(author_fig, include_plotlyjs=False, output_type='div')

    return top_author_plot


def oldest_books():
    cursor = mydb.cursor()
    # Top 5 Oldest Books ----------------------------------------------------------------------------------------
    oldest_published_query = """SELECT title, date_published
                                FROM books 
                                JOIN account_books ON books.bID = account_books.bID 
                                WHERE uID = '%s' 
                                ORDER BY date_published ASC LIMIT 5""" % session['uID']
    cursor.execute(oldest_published_query)
    oldest_published_query_value = cursor.fetchall()
    # print(str(oldest_published_query_value)[0:300])

    # Convert SQL Query to Pandas Dataframe
    oldest_published_df = pd.DataFrame([[ij for ij in i] for i in oldest_published_query_value])
    oldest_published_df.columns = ['Title', 'Date Published']

    # Plotly Chart
    oldest_fig = px.line(oldest_published_df,
                         y='Date Published',
                         x='Title',
                         hover_data=['Title'],
                         labels={'x': 'Date Published', 'y': 'Title'},
                         title="Your Top 5 Oldest Published Books")
    oldest_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    oldest_fig.update_traces(textfont_color='rgba(196, 186, 166, 1)')
    # fig4.update_yaxes(autorange="reversed")

    oldest_published_plot = plot(oldest_fig, include_plotlyjs=False, output_type='div')

    return oldest_published_plot


def longest_series():
    cursor = mydb.cursor()
    # Top 5 Longest Series ----------------------------------------------------------------------------------------
    longest_series_query = """SELECT b.title, s.seriesName, MAX(b.number_in_series) as NumberInSeries
                              FROM series as s
                              JOIN book_series as bs ON s.sID = bs.sID
                              JOIN books as b ON bs.bID = b.bID
                              JOIN account_books as ab ON b.bID = ab.bID
                              WHERE uID = '%s';""" % session['uID']
    cursor.execute(longest_series_query)
    longest_series_query_value = cursor.fetchall()
    # print(str(longest_series_query_value)[0:300])

    # Convert SQL Query to Pandas Dataframe
    longest_series_df = pd.DataFrame([[ij for ij in i] for i in longest_series_query_value])
    longest_series_df.columns = ['Title', 'Series Name', 'Number In Series']

    # Plotly Chart
    series_fig = px.bar(longest_series_df,
                        x='Number In Series',
                        y='Title',
                        hover_data=['Series Name'],
                        labels={'x': 'Number In Series', 'y': 'Title'},
                        title="Your Top 5 Longest Series")
    series_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    #series_fig.update_yaxes(autorange="reversed")

    longest_series_plot = plot(series_fig, include_plotlyjs=False, output_type='div')

    return longest_series_plot


def top_genres():
    cursor = mydb.cursor()
    # Top 5 Genres ----------------------------------------------------------------------------------------
    top_genres_query = """SELECT g.genre, COUNT(DISTINCT g.genre) as TotalCount
                          FROM genre as g
                          JOIN book_genre as bg ON g.gID = bg.gID
                          JOIN books as b ON bg.bID = b.bID
                          JOIN account_books as ab ON ab.bID = ab.bID
                          WHERE ab.uID = '%s' GROUP BY g.genre;""" % session['uID']
    cursor.execute(top_genres_query)
    top_genres_query_value = cursor.fetchall()
    # print(str(top_genres_query_value)[0:300])

    # Convert SQL Query to Pandas Dataframe
    top_genres_df = pd.DataFrame([[ij for ij in i] for i in top_genres_query_value])
    top_genres_df.columns = ['Genre', 'Count']

    # print(top_genres_df)
    # Plotly Chart
    genre_fig = px.pie(top_genres_df,
                       values='Count',
                       names='Genre',
                       title="Count of all Genres",
                       color_discrete_sequence=px.colors.sequential.YlOrBr)
    genre_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')

    top_genres_plot = plot(genre_fig, include_plotlyjs=False, output_type='div')
    return top_genres_plot


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
        cursor = mydb.cursor()
        login_query = ("""SELECT uID FROM accounts WHERE email = '%s' AND password = '%s';""" % (email, password))
        cursor.execute(login_query)
        # Fetch one record and return the result
        login_query_value = cursor.fetchone()
        # print(login_query_value)

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
            # Redirect to home page
            # return render_template('login.html')

            # Run query functions
            top_books()
            top_authors()

            # fig2.show(renderer='svg', width=500, height=500)

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
        cursor = mydb.cursor()
        account_query = ("""SELECT * FROM accounts WHERE email = '%s'""" % email)
        cursor.execute(account_query)
        account_query_value = cursor.fetchone()

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
            account_insert = ("""INSERT INTO accounts VALUES ('%s', '%s', '%s')""" % (str(uuid4()), email, password))
            cursor.execute(account_insert)
            print("Account Added:, ", email, password)
            mydb.commit()
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
    title = request.form['title']
    author_fname = request.form['author_fname']
    author_lname = request.form['author_lname']
    genre = request.form['genre']
    genre_split = None
    publisher = request.form['publisher']
    pages = request.form['pages']
    rating = request.form['rating']
    checkbox = request.form.get('checkbox', False)
    date_added = datetime.now().date().strftime('%Y-%m-%d')
    date_published = request.form['date_published']

    if session['loggedin'] is False:
        msg = 'Please login to add your book!'
        return render_template('index.html', msg=msg)
    elif request.method == 'POST' and session['loggedin'] is True:
        # Checks if form is filled out
        if (title not in request.form or author_fname not in request.form or author_lname not in request.form or
                genre not in request.form or publisher not in request.form or pages not in request.form or
                rating not in request.form or date_published not in request.form):
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

            if checkbox:
                series = request.form['series']
                series_num = request.form['seriesNum']
            else:
                series = None
                series_num = None

            cursor = mydb.cursor()

            try:
                # BOOK TITLE ------------------------------------------------------------------------------------------
                # SQL query to check if book exists
                book_query = ("""SELECT bID FROM books WHERE title='%s' AND pages=%s;"""
                              % (title, int(pages)))
                cursor.execute(book_query)
                book_query_value = cursor.fetchone()
                if not book_query_value:
                    # if series number doesn't exist
                    if not series_num:
                        # Inserts book into database
                        books_insert = ("""INSERT INTO books (bID, title, pages, rating, date_added, date_published) 
                                         VALUES ('%s', '%s', %s, '%s', '%s',  '%s');"""
                                        % (str(uuid4()), title, int(pages), rating, date_added, date_published))
                        cursor.execute(books_insert)
                        # Executes query
                        cursor.execute(book_query)
                        # Stores query results into variable
                        book_insert_value = cursor.fetchone()
                        print("Book added: ", title, book_insert_value)

                        # Takes book ID and stores it into book_value
                        # Storing in new variables to change list/tuple to single string
                        book_value = book_insert_value[0]
                        print("Book_ID: ", book_value)

                        # Inserts book into account_books table
                        account_books_insert = ("""INSERT INTO account_books VALUES ('%s', '%s');"""
                                                % (session['uID'], book_value))
                        cursor.execute(account_books_insert)
                        print("Book added to account: ", title, book_query_value)
                    # if series number exists
                    else:
                        # Inserts book into database
                        books_insert = ("""INSERT INTO books 
                                        (bID, title, pages, rating, number_in_series, date_added, date_published) 
                                        VALUES ('%s', '%s', %s, '%s', %s, '%s',  '%s');"""
                                        % (str(uuid4()), title, int(pages), rating,
                                           series_num, date_added, date_published))
                        cursor.execute(books_insert)
                        # Executes query
                        cursor.execute(book_query)
                        # Stores query results into variable
                        book_insert_value = cursor.fetchone()
                        print("Book added: ", title, book_insert_value)

                        # Storing in new variables to change list/tuple to single string
                        book_value = book_insert_value[0]
                        print("Book_ID: ", book_value)

                        # Inserts book into account_books table
                        account_books_insert = ("""INSERT INTO account_books VALUES ('%s', '%s');"""
                                                % (session['uID'], book_value))
                        cursor.execute(account_books_insert)
                        print("Book added to account: ", title, book_query_value)

                    # AUTHOR NAME --------------------------------------------------------------------------------------
                    # Query to check if author exists
                    author_query = ("""SELECT aID FROM authors WHERE firstname = '%s' AND lastname = '%s';"""
                                    % (author_fname, author_lname))
                    cursor.execute(author_query)
                    author_query_value = cursor.fetchone()
                    # Checks if author exists
                    if not author_query_value:
                        # Inserts author into database
                        authors_insert = ("""INSERT INTO authors (aID, firstname, lastname) 
                                            VALUES ('%s', '%s', '%s');"""
                                          % (str(uuid4()), author_fname, author_lname))
                        cursor.execute(authors_insert)
                        # Stores query results into variable
                        cursor.execute(author_query)
                        author_insert_value = cursor.fetchone()
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
                    book_author_insert = ("""INSERT INTO book_author (bID, aID) VALUES ('%s', '%s')"""
                                          % (book_value, author_value))
                    cursor.execute(book_author_insert)

                    # Checks to make sure book_author is in database
                    book_author_query = ("""SELECT DISTINCT bID, aID FROM book_author WHERE bID = '%s' AND aID = '%s'"""
                                         % (book_value, author_value))
                    # Executes query
                    cursor.execute(book_author_query)
                    # Stores query results into variable
                    book_author_value = cursor.fetchone()
                    print("Book_Author added", book_author_value)

                    # PUBLISHER NAME -----------------------------------------------------------------------------------
                    # Query to check if publisher exists`
                    publisher_query = ("""SELECT pID FROM publisher WHERE publisher = '%s'""" % publisher)
                    cursor.execute(publisher_query)
                    publisher_query_value = cursor.fetchone()

                    # Checks if publisher exists
                    if not publisher_query_value:
                        # Inserts publisher into database
                        publisher_insert = ("""INSERT INTO publisher (pID, publisher) VALUES ('%s', '%s');"""
                                            % (str(uuid4()), publisher))
                        cursor.execute(publisher_insert)
                        # Stores query results into variable
                        cursor.execute(publisher_query)
                        publisher_insert_value = cursor.fetchone()
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
                    book_publisher_insert = ("""INSERT INTO book_publisher (bID, pID) VALUES ('%s', '%s')"""
                                             % (book_value, publisher_value))
                    cursor.execute(book_publisher_insert)

                    # Checks to make sure book_publisher is in database
                    book_publisher_query = ("""SELECT DISTINCT bID, pID FROM book_publisher 
                                            WHERE bID = '%s' AND pID = '%s'"""
                                            % (book_value, publisher_value))
                    # Executes query
                    cursor.execute(book_publisher_query)
                    # Stores query results into variable
                    book_publisher_value = cursor.fetchone()
                    print("Book_Publisher added", book_publisher_value)

                    # GENRE --------------------------------------------------------------------------------------------
                    # Uses single genre
                    if not genre_split:
                        # Query to check if genre exists
                        genre_query = ("""SELECT gID FROM genre WHERE genre = '%s'""" % genre)
                        cursor.execute(genre_query)
                        genre_query_value = cursor.fetchone()

                        # Checks if genre exists
                        if not genre_query_value:
                            # Inserts genre into database
                            genres_insert = ("""INSERT INTO genre (gID, genre) VALUES ('%s', '%s');"""
                                             % (str(uuid4()), genre))
                            cursor.execute(genres_insert)
                            # Stores query results into variable
                            cursor.execute(genre_query)
                            genre_insert_value = cursor.fetchone()
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
                        book_genre_insert = ("""INSERT INTO book_genre (bID, gID) VALUES ('%s', '%s')"""
                                             % (book_value, genre_value))
                        cursor.execute(book_genre_insert)

                        # Checks to make sure book_genre is in database
                        book_genre_query = ("""SELECT DISTINCT bID, gID FROM book_genre 
                                                WHERE bID = '%s' AND gID = '%s'"""
                                            % (book_value, genre_value))
                        # Executes query
                        cursor.execute(book_genre_query)
                        # Stores query results into variable
                        book_genre_value = cursor.fetchone()
                        print("Book_Genre added", book_genre_value)

                    # Uses genre_split that is a list
                    else:
                        for g in genre_split:
                            # Query to check if genre exists
                            genre_query = ("""SELECT gID FROM genre WHERE genre = '%s'""" % g)
                            cursor.execute(genre_query)
                            genre_query_value = cursor.fetchone()

                            # Checks if genre exists
                            if not genre_query_value:
                                # Inserts genre into database
                                genres_insert = ("""INSERT INTO genre (gID, genre) VALUES ('%s', '%s');"""
                                                 % (str(uuid4()), g))
                                cursor.execute(genres_insert)
                                # Stores query results into variable
                                cursor.execute(genre_query)
                                genre_insert_value = cursor.fetchone()
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
                            book_genre_insert = ("""INSERT INTO book_genre (bID, gID) VALUES ('%s', '%s')"""
                                                 % (book_value, genre_value))
                            cursor.execute(book_genre_insert)

                            # Checks to make sure book_genre is in database
                            book_genre_query = (
                                    """SELECT DISTINCT bID, gID FROM book_genre WHERE bID = '%s' AND gID = '%s'"""
                                    % (book_value, genre_value))
                            # Executes query
                            cursor.execute(book_genre_query)
                            # Stores query results into variable
                            book_genre_value = cursor.fetchone()
                            print("Book_Genre added", book_genre_value)

                    # SERIES NAME --------------------------------------------------------------------------------------
                    if not series:
                        mydb.commit()
                    else:
                        # Query to check if series exists
                        series_query = ("""SELECT sID FROM series WHERE seriesName = '%s';""" % series)
                        cursor.execute(series_query)
                        series_query_value = cursor.fetchone()
                        # Checks if series exists
                        if not series_query_value:
                            # Inserts series into database
                            series_insert = ("""INSERT INTO series (sID, seriesName) VALUES ('%s', '%s');"""
                                             % (str(uuid4()), series))
                            cursor.execute(series_insert)
                            # Stores query results into variable
                            cursor.execute(series_query)
                            series_insert_value = cursor.fetchone()
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
                        book_series_insert = ("""INSERT INTO book_series (bID, sID) VALUES ('%s', '%s')"""
                                              % (book_value, series_value))
                        cursor.execute(book_series_insert)

                        # Checks to make sure book_series is in database
                        book_series_query = ("""SELECT DISTINCT bID, sID FROM book_series 
                                                WHERE bID = '%s' AND sID = '%s'"""
                                             % (book_value, series_value))
                        # Executes query
                        cursor.execute(book_series_query)
                        # Stores query results into variable
                        book_series_value = cursor.fetchone()
                        print("Book_Series added", book_series_value)

                        mydb.commit()
                else:
                    print("Book already exists", title, book_query_value)

                    # Checks if book exists in account books table to see if the account has the book associated with it
                    account_books_query = ("""SELECT * FROM account_books WHERE bID = '%s'""" % book_query_value)
                    cursor.execute(account_books_query)
                    account_books_query_value = cursor.fetchone()

                    if not account_books_query_value:
                        # Inserts book into account_books table
                        account_books_insert = ("""INSERT INTO account_books VALUES ('%s', '%s');"""
                                                % (session['uID'], book_value))
                        cursor.execute(account_books_insert)
                        print("Book added to account: ", title, book_query_value)
                        mydb.commit()
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
