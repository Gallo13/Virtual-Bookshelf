# Created by: Jess Gallo
# Created date: 09/01/2023
# Last Modified: 09/01/2023
# Description: Virtual Bookshelf Webapp/Storage
# Python, Flask, MySQL, ML Recommender

# Libraries
from flask import Flask, render_template, flash, url_for, request
import mysql.connector
from uuid import uuid4

app = Flask(__name__, template_folder='HTML', static_folder='')

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='galloGiallo13',
    database='bookshelf'
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

        try:
            with mydb.cursor() as cursor:
                # BOOK TITLE ------------------------------------------------------------------------------------------
                books_insert = "INSERT INTO books (bID, title, pages, rating) VALUES (%s, %s, %s, %s)"
                book_value = cursor.execute(books_insert, (str(uuid4()), title, pages, rating))
                if book_value > 0:
                    book_query = ("SELECT bID "
                                  "FROM books"
                                  "WHERE title = %s")
                    print("Book already exists", book_query)
                else:
                    print("Book added", book_value)

                # AUTHOR NAME ------------------------------------------------------------------------------------------
                authors_insert = "INSERT INTO authors (aID, firstname, lastname) VALUES (%s, %s, %s)"
                author_value = cursor.execute(authors_insert, (str(uuid4()), author_fname, author_lname))
                author_query = ("SELECT DISTINCT authors.aID "
                                "FROM authors JOIN book_author "
                                "ON authors.aID = book_author.aID "
                                "WHERE firstname = %s AND lastname = %s")
                if author_value > 0:
                    print("Author already exists", author_query)
                else:
                    print("Author added", author_value)
                    # BOOK AUTHOR---------------------------------------------------------------------------------------
                    book_author_insert = "INSERT INTO book_author (bID, aID) VALUES (%s, %s, %s)"
                    book_author_value = cursor.execute(book_author_insert, (str(uuid4()), book_query, author_query))
                    print("Book_Author added", book_author_value)

                # PUBLISHER NAME ---------------------------------------------------------------------------------------
                publishers_insert = "INSERT INTO publishers (pID, name) VALUES (%s, %s)"
                publisher_value = cursor.execute(publishers_insert, (str(uuid4()), publisher))
                publisher_query = ("SELECT DISTINCT publishers.pID "
                                   "FROM publishers JOIN book_publisher "
                                   "ON publishers.pID = book_publisher.pID "
                                   "WHERE name = %s")
                if publisher_value > 0:
                    print("Publisher already exists", publisher_query)
                else:
                    print("Publisher added", publisher_value)
                    # BOOK PUBLISHER -----------------------------------------------------------------------------------
                    book_publisher_insert = "INSERT INTO book_publisher (bID, pID) VALUES (%s, %s, %s)"
                    book_pub_value = cursor.execute(book_publisher_insert, (str(uuid4()), book_query, publisher_query))
                    print("Book_Publisher added", book_pub_value)

                # GENRE ------------------------------------------------------------------------------------------------
                    sql_genre_insert = "INSERT INTO genres (gID, name) VALUES (%s, %s)"
                    genre_value = cursor.execute(sql_genre_insert, (str(uuid4()), genre))
                    genre_query = ("SELECT DISTINCT genre.gID "
                                   "FROM genre JOIN book_genre "
                                   "ON genre.gID = book_genre.gID "
                                   "WHERE genre = %s")
                    if genre_value > 0:
                        print("Genre already exists", genre_query)
                    else:
                        print("Genre added", genre_value)
                        # BOOK GENRE -----------------------------------------------------------------------------------
                        book_genre_insert = "INSERT INTO book_genre (bID, gID) VALUES (%s, %s, %s)"
                        book_genre_value = cursor.execute(book_genre_insert, (str(uuid4()), book_query, genre_query))
                        print("Book_Genre added", book_genre_value)

                # mydb.commit()
                print(cursor.rowcount, "record inserted.")
        finally:
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
