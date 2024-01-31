# Created by: Jess Gallo
# Date created: 01/19/2024
# Last modified: 01/30/2024
# Description: Functions for Plotly charts


from plotly.offline import plot
import plotly.express as px
import pandas as pd
from flask import Flask, session
from database import execute_sql_query


def top_books():
    """
    :return: Plotly chart of the top 5 books for the user.
    """

    # Top 5 Books ----------------------------------------------------------------------------------------
    query = ("SELECT b.title, a.firstname, a.lastname, b.rating "
             "FROM books as b "
             "JOIN account_books as ab ON b.bID = ab.bID "
             "JOIN book_author as ba ON b.bID = ba.bID "
             "JOIN authors as a ON ba.aID = a.aID "
             "WHERE uID = %s "
             "ORDER BY rating DESC LIMIT 5;")
    qvalues = session['uID']
    top_book_query_value = execute_sql_query(query, qvalues)
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
    """
    :return: Plotly chart of the top 5 authors for the user.
    """
    # Most Read Author ----------------------------------------------------------------------------------------
    query = """SELECT firstname, lastname, COUNT(lastname) as count
               FROM authors
               JOIN book_author ON authors.aID = book_author.aID
               JOIN account_books ON book_author.bID = account_books.bID
               WHERE account_books.uID = %s
               GROUP BY firstname, lastname
               ORDER BY count DESC
               LIMIT 5;"""
    qvalues = session['uID']
    top_author_query_value = execute_sql_query(query, qvalues)
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
    """
    :return: Plotly chart of the 5 oldest published books for the user.
    """
    # Top 5 Oldest Books ----------------------------------------------------------------------------------------
    query = """SELECT title, date_published
               FROM books 
               JOIN account_books ON books.bID = account_books.bID 
               WHERE uID = %s 
               ORDER BY date_published ASC LIMIT 5"""
    qvalues = session['uID']
    oldest_published_query_value = execute_sql_query(query, qvalues)
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
    """
    :return: Plotly chart of the longest series of books for the user.
    """
    # Top 5 Longest Series ----------------------------------------------------------------------------------------
    query = """SELECT b.title, s.seriesName, MAX(b.number_in_series) as NumberInSeries
               FROM series as s
               JOIN book_series as bs ON s.sID = bs.sID
               JOIN books as b ON bs.bID = b.bID
               JOIN account_books as ab ON b.bID = ab.bID
               WHERE uID = %s;"""
    qvalues = session['uID']
    longest_series_query_value = execute_sql_query(query, qvalues)
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

    longest_series_plot = plot(series_fig, include_plotlyjs=False, output_type='div')

    return longest_series_plot


def top_genres():
    """
    :return: Plotly chart of the top 5 genres for the user.
    """
    # Top 5 Genres ----------------------------------------------------------------------------------------
    query = """SELECT g.genre, COUNT(DISTINCT g.genre) as TotalCount
               FROM genre as g
               JOIN book_genre as bg ON g.gID = bg.gID
               JOIN books as b ON bg.bID = b.bID
               JOIN account_books as ab ON ab.bID = ab.bID
               WHERE ab.uID = %s GROUP BY g.genre;"""
    qvalues = session['uID']
    top_genres_query_value = execute_sql_query(query, qvalues)
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
