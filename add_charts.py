# Created by: Jess Gallo
# Date created: 02/25/24
# Last Modified: 10/09/24
# Description: Queries for charts creation

# Imports
from database import execute_sql_query
from flask import session


def check_top_books_exists():
    """
        Checks if user has any book data

        Returns:
            result (list): The result of the query execution.
    """
    query = ("SELECT b.title, a.firstname, a.lastname, b.rating "
             "FROM books as b "
             "JOIN account_books as ab ON b.isbn = ab.isbn "
             "JOIN book_author as ba ON b.isbn = ba.isbn "
             "JOIN authors as a ON ba.aID = a.aID "
             "WHERE uID = %s "
             "ORDER BY rating DESC LIMIT 5;")
    qvalues = session['uID']
    top_books = execute_sql_query(query, (qvalues,))
    return top_books if top_books else None


def check_top_authors_exists():
    """
        Checks if user has any book data

        Returns:
            result (list): The result of the query execution.
    """
    query = """SELECT firstname, lastname, COUNT(lastname) as count
                FROM authors
                JOIN book_author ON authors.aID = book_author.aID
                JOIN account_books ON book_author.isbn = account_books.isbn
                WHERE account_books.uID = %s
                GROUP BY firstname, lastname
                ORDER BY count DESC
                LIMIT 5;"""
    qvalues = session['uID']
    top_author = execute_sql_query(query, (qvalues,))
    return top_author[0][0:2] if top_author else None


def check_oldest_books_exists():
    """
        Checks if user has any book data

        Returns:
            result (list): The result of the query execution.
    """
    query = """SELECT title, date_published
                FROM books 
                JOIN account_books ON books.isbn = account_books.isbn 
                WHERE uID = %s 
                ORDER BY date_published ASC LIMIT 5"""
    qvalues = session['uID']
    oldest_books = execute_sql_query(query, (qvalues,))
    return oldest_books[0] if oldest_books else None


def check_longest_series_exists():
    """
        Checks if user has any book data

        Returns:
            result (list): The result of the query execution.
    """
    query = """SELECT b.title, s.seriesName, MAX(b.number_in_series) as NumberInSeries
               FROM series as s
               JOIN book_series as bs ON s.sID = bs.sID
               JOIN books as b ON bs.isbn = b.isbn
               JOIN account_books as ab ON b.isbn = ab.isbn
               WHERE uID = %s
               GROUP BY title, s.seriesName;"""
    qvalues = session['uID']
    longest_series = execute_sql_query(query, (qvalues,))
    print('longest series', longest_series)
    return longest_series[0] if longest_series else None


def check_top_genre_exists():
    """
        Checks if user has any book data

        Returns:
            result (list): The result of the query execution.
    """
    query = """SELECT g.genre, COUNT(DISTINCT g.genre) as TotalCount
               FROM genre as g
               JOIN book_genre as bg ON g.gID = bg.gID
               JOIN books as b ON bg.isbn = b.isbn
               JOIN account_books as ab ON ab.isbn = ab.isbn
               WHERE ab.uID = %s 
               GROUP BY g.genre;"""
    qvalues = session['uID']
    top_genre = execute_sql_query(query, (qvalues,))
    print('top genre', top_genre)
    return top_genre[0] if top_genre else None
