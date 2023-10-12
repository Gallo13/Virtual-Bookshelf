# Created by: Jess Gallo
# Created date: 09/01/2023
# Last Modified: 09/25/2023
# Description: Virtual Bookshelf Webapp/Storage
# Python, Flask, MySQL, ML Recommender

# Libraries
from flask import Flask, render_template, flash, url_for, request
import mysql.connector
from uuid import uuid4
from datetime import datetime

app = Flask(__name__, template_folder='HTML', static_folder='')

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='galloGiallo13',
    database='bookshelf2'
)


# route decorator to tell Flask what URL should trigger function
@app.route('/', methods=['GET',  'POST'])
def get_data():
    if request.method == 'POST':
        title = request.form['title']
        author_fname = request.form['author_fname']
        author_lname = request.form['author_lname']
        genre = request.form['genre']
        publisher = request.form['publisher']
        pages = request.form['pages']
        rating = request.form['rating']
        date_added = datetime.now().date().strftime('%Y-%m-%d')

        # print("Title: ", title,  "Author: ", author_fname, author_lname, "Genre: ", genre, "Publisher: ", publisher,
        #      "Pages: ", pages, "Rating: ", rating, "Date Added: ", date_added)

        # try:
        #    with mydb.cursor() as cursor:
        cursor = mydb.cursor()
        # BOOK TITLE ------------------------------------------------------------------------------------------
        # SQL query to check if book exists
        book_query = """SELECT bID FROM books WHERE title='%s' AND pages=%s;""" % (title, int(pages))

        if book_query is True:
            print("Book already exists", title)
        else:
            # Inserts book into database
            books_insert = ("""INSERT INTO books (bID, title, pages, rating, date_added) 
                           VALUES ('%s', '%s', %s, %s, '%s');"""
                            % (str(uuid4()), title, int(pages), int(rating),  date_added))
            cursor.execute(books_insert)
            # Executes query
            cursor.execute(book_query)
            # Stores query results into variable
            book_value = cursor.fetchone()
            print("Book added: ", title, book_value)

        # AUTHOR NAME ------------------------------------------------------------------------------------------
        # Query to check if author exists
        author_query = ("""SELECT aID FROM authors WHERE firstname = '%s' AND lastname = '%s';"""
                        % (author_fname, author_lname))
        # Checks if author exists
        if author_query is True:
            print("Author already exists", author_fname, author_lname)
        else:
            # Inserts author into database
            authors_insert = ("""INSERT INTO authors (aID, firstname, lastname) VALUES ('%s', '%s', '%s');"""
                              % (str(uuid4()), author_fname, author_lname))
            cursor.execute(authors_insert)
            # Stores query results into variable
            cursor.execute(author_query)
            author_value = cursor.fetchone()
            print("Author added: ", author_fname, author_lname,  author_value)

        # BOOK AUTHOR---------------------------------------------------------------------------------------
        book_value2 = book_value[0]
        print("Book_ID: ", book_value2)
        author_value2 = author_value[0]
        print("Author_ID: ", author_value2)
        # Inserts aID and bID into book_author table
        book_author_insert = ("""INSERT INTO book_author (bID, aID) VALUES ('%s', '%s')"""
                              % (book_value2, author_value2))
        cursor.execute(book_author_insert)

        # Checks to make sure book_author is in database
        book_author_query = ("""SELECT DISTINCT bID, aID FROM book_author WHERE bID = '%s' AND aID = '%s'"""
                             % (book_value2, author_value2))
        # Executes query
        cursor.execute(book_author_query)
        # Stores query results into variable
        book_author_value = cursor.fetchone()
        print("Book_Author added", book_author_value)

        # PUBLISHER NAME ---------------------------------------------------------------------------------------
        # Query to check if publisher exists`
        publisher_query = ("""SELECT pID FROM publisher WHERE publisher = '%s'""" % publisher)

        # Checks if author exists
        if publisher_query is True:
            print("Publisher already exists", publisher_query)
        else:
            # Inserts publisher into database
            publisher_insert = ("""INSERT INTO publisher (pID, publisher) VALUES ('%s', '%s');"""
                                % (str(uuid4()), publisher))
            cursor.execute(publisher_insert)
            # Stores query results into variable
            cursor.execute(publisher_query)
            publisher_value = cursor.fetchone()
            print("Publisher added", publisher_value)

        # BOOK PUBLISHER -----------------------------------------------------------------------------------
        publisher_value2 = publisher_value[0]
        print("Publisher_ID: ", publisher_value2)

        # Inserts bID and pID into book_publisher table
        book_publisher_insert = ("""INSERT INTO book_publisher (bID, pID) VALUES ('%s', '%s')"""
                                 % (book_value2, publisher_value2))
        cursor.execute(book_publisher_insert)

        # Checks to make sure book_publisher is in database
        book_publisher_query = ("""SELECT DISTINCT bID, pID FROM book_publisher WHERE bID = '%s' AND pID = '%s'"""
                                % (book_value2, publisher_value2))

        # Executes query
        cursor.execute(book_publisher_query)
        # Stores query results into variable
        book_publisher_value = cursor.fetchone()

        print("Book_Publisher added", book_publisher_value)

        # GENRE ------------------------------------------------------------------------------------------------
        # Query to check if genre exists
        genre_query = ("""SELECT gID FROM genre WHERE genre = '%s'""" % genre)

        # Checks if genre exists
        if genre_query is True:
            print("Genre already exists", genre_query)
        else:
            # Inserts genre into database
            genres_insert = ("""INSERT INTO genre (gID, genre) VALUES ('%s', '%s');"""
                             % (str(uuid4()), genre))
            cursor.execute(genres_insert)
            # Stores query results into variable
            cursor.execute(genre_query)
            genre_value = cursor.fetchone()
            print("Genre added", genre_value)

        # BOOK GENRE -----------------------------------------------------------------------------------
        genre_value2 = genre_value[0]
        print("Genre_ID: ", genre_value2)

        # Inserts bID and gID into book_genre table
        book_genre_insert = ("""INSERT INTO book_genre (bID, gID) VALUES ('%s', '%s')""" % (book_value2, genre_value2))
        cursor.execute(book_genre_insert)

        # Checks to make sure book_genre is in database
        book_genre_query = ("""SELECT DISTINCT bID, gID FROM book_genre WHERE bID = '%s' AND gID = '%s'"""
                            % (book_value2, genre_value2))

        # Executes query
        cursor.execute(book_genre_query)
        # Stores query results into variable
        book_genre_value = cursor.fetchone()
        print("Book_Genre added", book_genre_value)

        mydb.commit()
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

            book_data.append({'title': title, 'author': author, 'genre': genre,
                              'publisher': publisher, 'pages': pages, 'rating': rating})

            return render_template('index.html')
        """
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
