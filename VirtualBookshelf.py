# Created by: Jess Gallo
# Created date: 09/01/2023
# Last Modified: 01/19/2023
# Description: Virtual Bookshelf Webapp/Storage
# Python, Flask, MySQL

# CHANGE WHERE msg messages go! make into popup!
# Put cursor.commit() for inserts or have different insert function

# Libraries
import hashlib
import re

from flask import Flask, Blueprint, render_template, redirect, url_for, request, session

from database import establish_database_connection, execute_sql_query, insert_data
from charts import top_books, top_authors, oldest_books, longest_series, top_genres
from add_book import check_book_exists, check_author_exists, check_series_exists, check_genre_exists

auth = Flask(__name__, template_folder='HTML', static_folder='')
# Secret key for extra protection
auth.secret_key = '85002040'

# Add the function by name to the jinja environment.
auth.jinja_env.globals.update(top_books=top_books)
auth.jinja_env.globals.update(top_authors=top_authors)
auth.jinja_env.globals.update(oldest_books=oldest_books)
auth.jinja_env.globals.update(longest_series=longest_series)
auth.jinja_env.globals.update(top_genres=top_genres)

# auth.jinja_env.globals.update(get_form_request=get_form_request)
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
    return redirect(url_for('index', msg=msg))
    # return render_template('index.html', msg=msg)


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
@auth.route('/get_data', methods=['GET', 'POST'])
def get_data():
    """
    author_insert_value = None
    publisher_insert_value = None
    genre_insert_value = None
    series_insert_value = None
    book_value = None
    """

    # Get user input
    """
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
    """

    # get user input
    title = request.form['title']
    author_fname = request.form['author_fname']
    author_lname = request.form['author_lname']
    genre = request.form['genre']
    publisher = request.form['publisher']
    pages = request.form['pages']
    date_added = datetime.now().date().strftime('%Y-%m-%d')
    date_published = request.form['date_published']

    # Checks if user is logged in (if user is not logged in)
    if session['loggedin'] is False:
        msg = 'Please login to add your book!'
        home_html = 'index.html'
        return render_template(home_html, msg=msg)

    # If user is logged in
    if request.method == 'POST' and session['loggedin'] is True:
        # Checks if form is filled out
        if not title or not author_fname or not author_lname or not genre or not publisher or not pages:
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
            return handle_book_exists(book_query_value[0])

        """
         If book does not exist in database (books table) then we need to insert the book into the database.
        """
        # Insert book into database
        ivalue = (str(uuid4()), title, int(pages), rating, date_added, date_published, number_in_series)
        book_value = insert_book(query, ivalue)
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
            return handle_author_exists(author_query_value[0])
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
                if  genre_query_value:
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
                return handle_genre_exists(genre_query_value[0])
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
            return handle_publisher_exists(publisher_query_value[0])
        else:
            # Insert publisher into database
            insert_book_publisher(publisher_query_value)
            print("Publisher added: ", publisher, publisher_query_value[0])
            # Insert genre into book_genres table (register genre under current book)
            return handle_publisher_exists(publisher_query_value[0])
    """

        # Check if book already exists
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
                book_query = "SELECT bID FROM books WHERE title=%s AND pages=%s;"
                qvalues = (title, int(pages))
                query = book_query
                book_query_value = execute_sql_query(query, qvalues)
                print("Book_ID: ", book_query_value)
                if not book_query_value:
                    # Inserts book into database
                    book_insert = ("INSERT INTO books (bID, title, pages, rating, date_added, "
                                   "date_published, number_in_series) VALUES (%s, %s, %s, %s, %s, %s, %s);")
                    ivalues = (str(uuid4()), title, int(pages), rating, date_added, date_published, series_num)
                    insert = book_insert
                    book_insert_value = insert_data(insert, ivalues)
                    print("Book added: ", title, book_insert_value[0])

                    # Storing in new variables to change list/tuple to single string
                    # book_value = book_insert_value[0]
                    print("Book_ID: ", book_query_value[0])

                    # Inserts book into account_books table
                    account_books_insert = "INSERT INTO account_books (uID, bID) VALUES (%s, %s);"
                    ivalues = (session['uID'], book_query_value)
                    print(account_books_insert)
                    print(ivalues)
                    insert = account_books_insert
                    insert_data(insert, ivalues)

                    # ********  Add query to check to was added   ******************
                    # account_books_query = "SELECT "

                    print("Book added to account: ", title, book_query_value[0])

                    # AUTHOR NAME --------------------------------------------------------------------------------------
                    # Query to check if author exists
                    author_query = "SELECT aID FROM authors WHERE firstname = %s AND lastname = %s;"
                    qvalues = (author_fname, author_lname)
                    query = author_query
                    author_query_value = execute_sql_query(query, qvalues)
                    print("Author_ID: ", author_query_value)
                    # Checks if author exists
                    if not author_query_value:
                        # Inserts author into database
                        authors_insert = "INSERT INTO authors (aID, firstname, lastname) VALUES (%s, %s, %s);"
                        ivalues = (str(uuid4()), author_fname, author_lname)
                        insert = authors_insert
                        insert_data(insert, ivalues)
                        # Stores query results into variable
                        author_insert_value = execute_sql_query(author_query, qvalues)
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
                    book_author_insert = "INSERT INTO book_author (bID, aID) VALUES (%s, %s)"
                    qvalues = (book_value, author_value)
                    query = book_author_insert
                    execute_sql_query(query, qvalues)

                    # Checks to make sure book_author is in database
                    book_author_query = "SELECT DISTINCT bID, aID FROM book_author WHERE bID = %s AND aID = %s"
                    qvalues = (book_value, author_value)
                    query = book_author_query
                    book_author_value = execute_sql_query(query, qvalues)
                    print("Book_Author added", book_author_value)

                    # PUBLISHER NAME -----------------------------------------------------------------------------------
                    # Query to check if publisher exists`
                    publisher_query = "SELECT pID FROM publisher WHERE publisher = %s"
                    qvalues = publisher
                    query = publisher_query
                    publisher_query_value = execute_sql_query(query, qvalues)

                    # Checks if publisher exists
                    if not publisher_query_value:
                        # Inserts publisher into database
                        publisher_insert = "INSERT INTO publisher (pID, publisher) VALUES (%s, %s);"
                        ivalues = (str(uuid4()), publisher)
                        query = publisher_insert
                        execute_sql_query(query, ivalues)
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
                    book_publisher_insert = "INSERT INTO book_publisher (bID, pID) VALUES (%s, %s)"
                    ivalue = (book_value, publisher_value)
                    query = book_publisher_insert
                    execute_sql_query(query, ivalue)

                    # Checks to make sure book_publisher is in database
                    book_publisher_query = "SELECT DISTINCT bID, pID FROM book_publisher WHERE bID = %s AND pID = %s"
                    qvalues = (book_value, publisher_value)
                    query = book_publisher_query
                    book_publisher_value = execute_sql_query(query, qvalues)
                    print("Book_Publisher added", book_publisher_value)

                    # GENRE --------------------------------------------------------------------------------------------
                    # Uses single genre
                    if not genre_split:
                        # Query to check if genre exists
                        genre_query = "SELECT gID FROM genre WHERE genre = %s"
                        qvalues = genre
                        query = genre_query
                        genre_query_value = execute_sql_query(query, qvalues)

                        # Checks if genre exists
                        if not genre_query_value:
                            # Inserts genre into database
                            genres_insert = "INSERT INTO genre (gID, genre) VALUES (%s, %s);"
                            ivalues = (str(uuid4()), genre)
                            query = genres_insert
                            insert_data(query, ivalues)
                            genre_insert_value = execute_sql_query(genres_insert, ivalues)
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
                        book_genre_insert = "INSERT INTO book_genre (bID, gID) VALUES (%s, %s)"
                        ivalues = (book_value, genre_value)
                        query = book_genre_insert
                        insert_data(query, ivalues)

                        # Checks to make sure book_genre is in database
                        book_genre_query = "SELECT DISTINCT bID, gID FROM book_genre WHERE bID = %s AND gID = %s"
                        qvalues = (book_value, genre_value)
                        query = book_genre_query
                        book_genre_value = execute_sql_query(query, qvalues)
                        print("Book_Genre added", book_genre_value)

                    # Uses genre_split that is a list
                    else:
                        for g in genre_split:
                            # Query to check if genre exists
                            genre_query = "SELECT gID FROM genre WHERE genre = %s"
                            qvalues = g
                            query = genre_query
                            genre_query_value = execute_sql_query(query, qvalues)

                            # Checks if genre exists
                            if not genre_query_value:
                                # Inserts genre into database
                                genres_insert = "INSERT INTO genre (gID, genre) VALUES (%s, %s);"
                                ivalues = (str(uuid4()), g)
                                query = genres_insert
                                genre_insert_value = insert_data(query, ivalues)
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
                            book_genre_insert = "INSERT INTO book_genre (bID, gID) VALUES (%s, %s)"
                            ivalues = (book_value, genre_value)
                            query = book_genre_insert
                            insert_data(query, ivalues)

                            # Checks to make sure book_genre is in database
                            book_genre_query = "SELECT DISTINCT bID, gID FROM book_genre WHERE bID = %s AND gID = %s"
                            qvalues = (book_value, genre_value)
                            query = book_genre_query
                            book_genre_value = execute_sql_query(query, qvalues)
                            print("Book_Genre added", book_genre_value)

                    # SERIES NAME --------------------------------------------------------------------------------------
                    if not series:
                        # have inserts committed now but i don't think this will work with everything labeled the same
                        # mydb.commit()
                        pass
                    else:
                        # Query to check if series exists
                        series_query = "SELECT sID FROM series WHERE seriesName = %s;"
                        qvalues = series
                        query = series_query
                        series_query_value = execute_sql_query(query, qvalues)
                        # Checks if series exists
                        if not series_query_value:
                            # Inserts series into database
                            series_insert = "INSERT INTO series (sID, seriesName) VALUES (%s, %s);"
                            ivalues = (str(uuid4()), series)
                            query = series_insert
                            series_insert_value = insert_data(query, ivalues)
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
                        book_series_insert = "INSERT INTO book_series (bID, sID) VALUES (%s, %s)"
                        ivalues = (book_value, series_value)
                        query = book_series_insert
                        insert_data(query, ivalues)

                        # Checks to make sure book_series is in database
                        book_series_query = "SELECT DISTINCT bID, sID FROM book_series WHERE bID = %s AND sID = %s"
                        qvalues = (book_value, series_value)
                        query = book_series_query
                        book_series_value = execute_sql_query(query, qvalues)
                        print("Book_Series added", book_series_value)

                        mydb.commit()
                else:
                    print("Book already exists", title, book_query_value[0])

                    # Checks if book exists in account books table to see if the account has the book associated with it
                    account_books_query = "SELECT * FROM account_books WHERE bID = %s"
                    qvalues = book_query_value[0]
                    query = account_books_query
                    account_books_query_value = execute_sql_query(query, qvalues)

                    if not account_books_query_value:
                        # Inserts book into account_books table
                        print('book_value: ', book_query_value[0])
                        account_books_insert = "INSERT INTO account_books (uID, bID) VALUES (%s, %s);"
                        ivalues = (session['uID'], book_query_value[0])
                        query = account_books_insert
                        insert_data(query, ivalues)
                        print("Book added to account: ", title, book_query_value)
                        mydb.close()
                    else:
                        print('Book already associated with account!')
            
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
