# Created by: Jess Gallo
# Created date: 09/01/2023
# Last Modified: 10/25/2023
# Description: Virtual Bookshelf Webapp/Storage
# Python, Flask, MySQL, ML Recommender

# Libraries
from flask import Flask, render_template, flash, url_for, request
import mysql.connector
from mysql.connector.errors import Error
from uuid import uuid4
from datetime import datetime

app = Flask(__name__, template_folder='HTML', static_folder='')


# route decorator to tell Flask what URL should trigger function
@app.route('/', methods=['GET',  'POST'])
def get_data():
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='galloGiallo13',
        database='virtual_bookshelf'
    )

    if request.method == 'POST':
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
            if book_query_value:
                print("Book already exists", title, book_query_value)
            else:
                pass

            if not book_query_value:
                # if series number doesn't exist
                if not series_num:
                    # Inserts book into database
                    books_insert = ("""INSERT INTO books (bID, title, pages, rating, date_added, date_published) 
                                     VALUES ('%s', '%s', %s, '%s', '%s',  '%s');"""
                                    % (str(uuid4()), title, int(pages), rating, date_added,  date_published))
                    cursor.execute(books_insert)
                    # Executes query
                    cursor.execute(book_query)
                    # Stores query results into variable
                    book_insert_value = cursor.fetchone()
                    print("Book added: ", title, book_insert_value)
                # if series number exists
                else:
                    # Inserts book into database
                    books_insert = ("""INSERT INTO books 
                                    (bID, title, pages, rating, number_in_series, date_added, date_published) 
                                    VALUES ('%s', '%s', %s, '%s', %s, '%s',  '%s');"""
                                    % (str(uuid4()), title, int(pages), rating, series_num, date_added, date_published))
                    cursor.execute(books_insert)
                    # Executes query
                    cursor.execute(book_query)
                    # Stores query results into variable
                    book_insert_value = cursor.fetchone()
                    print("Book added: ", title, book_insert_value)

                # AUTHOR NAME ------------------------------------------------------------------------------------------
                # Query to check if author exists
                author_query = ("""SELECT aID FROM authors WHERE firstname = '%s' AND lastname = '%s';"""
                                % (author_fname, author_lname))
                cursor.execute(author_query)
                author_query_value = cursor.fetchone()
                # Checks if author exists
                if not author_query_value:
                    # Inserts author into database
                    authors_insert = ("""INSERT INTO authors (aID, firstname, lastname) VALUES ('%s', '%s', '%s');"""
                                      % (str(uuid4()), author_fname, author_lname))
                    cursor.execute(authors_insert)
                    # Stores query results into variable
                    cursor.execute(author_query)
                    author_insert_value = cursor.fetchone()
                    print("Author added: ", author_fname, author_lname, author_insert_value)

                else:
                    print("Author already exists", author_fname, author_lname, author_query_value)

                # BOOK AUTHOR---------------------------------------------------------------------------------------
                # Takes book ID and stores it into book_value2
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

                # PUBLISHER NAME ---------------------------------------------------------------------------------------
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

                # GENRE ------------------------------------------------------------------------------------------------
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
                    book_genre_query = ("""SELECT DISTINCT bID, gID FROM book_genre WHERE bID = '%s' AND gID = '%s'"""
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
                        book_genre_query = (
                                    """SELECT DISTINCT bID, gID FROM book_genre WHERE bID = '%s' AND gID = '%s'"""
                                    % (book_value, genre_value))
                        # Executes query
                        cursor.execute(book_genre_query)
                        # Stores query results into variable
                        book_genre_value = cursor.fetchone()
                        print("Book_Genre added", book_genre_value)

                # SERIES NAME ------------------------------------------------------------------------------------------
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

                    # BOOK SERIES -- -----------------------------------------------------------------------------------
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
                    book_series_query = ("""SELECT DISTINCT bID, sID FROM book_series WHERE bID = '%s' AND sID = '%s'"""
                                         % (book_value, series_value))
                    # Executes query
                    cursor.execute(book_series_query)
                    # Stores query results into variable
                    book_series_value = cursor.fetchone()
                    print("Book_Series added", book_series_value)

                    mydb.commit()
            else:
                # flash('Book already exists!'
                print("Book already exists", title, book_query_value)
                cursor.close()
                # mydb.close()
        except mysql.connector.Error as err:
            # Handles Errors and gives the error codes to let us know what the issue is
            print(err)
            print("Error Code: ", err.errno)
            print("SQLSTATE: ", err.sqlstate)
            print("Message: ", err.msg)
            # raise Exception("Could not connect to database")
        finally:
            print('Done')
            cursor.close()
            mydb.close()

        """
        if not title:
            flash('Title is required!')
        elif not author:
            flash('Author is required!')
        elif not genre:
            flash('Genre is required!')
        elif not publisher:
            flash('Publisher is required!')
        elif not pages:
            flash('Pages is required!')
        elif not rating:
            flash('Rating is required!')
        else:
            flash('Book added successfully!')
        """
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
