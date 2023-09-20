# Created by: Jess Gallo
# Created date: 09/01/2023
# Last Modified: 09/01/2023
# Description: Virtual Bookshelf Webapp/Storage
# Python, Flask, MySQL, ML Reccommender

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
                sql_books = "INSERT INTO books (bID, title, pages, rating) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql_books, (str(uuid4()), title, pages, rating))

                sql_authors = "INSERT INTO authors (aID, fname, lname) VALUES (%s, %s, %s)"
                author_value = cursor.execute(sql_authors, (str(uuid4()), author_fname, author_lname))
                if author_value > 0:
                    query = "SELECT aID FROM authors WHERE fname = %s AND lname = %s"
                    print("Author already exists", query)
                else:
                    sql_authors = "INSERT INTO authors (aID, fname, lname) VALUES (%s, %s, %s)"
                    cursor.execute(sql_authors, (str(uuid4()), author_fname, author_lname))
                    print("Author added")

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
