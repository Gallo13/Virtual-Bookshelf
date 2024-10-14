# Created by: Jess Gallo
# Date Created: 10/09/2024
# Last Modified: 10/09/2024

from flask import render_template, request
from datetime import datetime

from add_book import *
from account_login import *
from flask import Blueprint, session

get_data_routes = Blueprint('get_data', __name__)

# changed from just methods=['POST']


@get_data_routes.route('/get_data', methods=['GET'])
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
        return render_template('index.html', msg=msg)

    # If user is logged in
    if request.method == 'POST' and session['loggedin'] is True:
        # Checks if form is filled out
        if not any([isbn, title, author_fname, author_lname, genre, publisher, pages, date_published]):
            msg = 'Please fill out the form!'
            return render_template('login.html', msg=msg)

        try:
            # new session['uID'] only for querying during get_data()
            session['uID2'] = session['uID'][0]

            # -- BOOK ----------------------------------------------
            # Checks if book already exists in database (books table) - executes SELECT statement
            book_query_value = check_book_exists(isbn)
            # If book exists in database (books table)
            if book_query_value is not None:
                session['isbn'] = book_query_value
                # Checks if book is associated with user and if it is not, it insert it into account_books tables
                insert_account_books()
            else:
                # If book does not exist in database (books table) then we need to insert the book into the database.
                # Insert book into database
                ivalue = (isbn, title, int(pages), rating, date_added, date_published, number_in_series)
                insert_book(ivalue)
                # Checks for updated book in DB
                book_query_value = check_book_exists(isbn)
                session['isbn'] = book_query_value
                # Adds book to user (isbn into account_books table)
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
            # Clears session['isbn'] - not sure if I really need this - will try with and without
            session['isbn'] = None
            return render_template('login.html')
