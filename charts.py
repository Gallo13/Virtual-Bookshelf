# Created by: Jess Gallo
# Date created: 01/19/2024
# Last modified: 10/09/2024
# Description: Functions for Plotly charts


from plotly.offline import plot
import plotly.express as px
import pandas as pd
from add_charts import *


def count_list(lst):
    """
        Parameters:
            lst (list): query results
        Return:
            a count of the lists inside a list
    """
    try:
        return len(lst)
    except Exception as e:
        print(e)
        return None


def top_books():
    """
        :return: Plotly chart of the top 5 books for the user.
    """

    # Top 5 Books ----------------------------------------------------------------------------------------
    top_book_query_value = check_top_books_exists()
    # print(str(top_book_query_value)[0:300])
    print('top book query value', top_book_query_value)
    print('count:', count_list(top_book_query_value))
    if top_book_query_value is not None and count_list(top_book_query_value) >= 5:
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
    top_author_query_value = check_top_authors_exists()
    # print(str(top_author_query_value)[0:300])
    print('top author query value', top_author_query_value)

    if top_author_query_value is not None and count_list(top_author_query_value) >= 5:
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
    oldest_published_query_value = check_oldest_books_exists()
    # print(str(oldest_published_query_value)[0:300])

    if oldest_published_query_value is not None and count_list(oldest_published_query_value) >= 5:
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
    longest_series_query_value = check_longest_series_exists()
    # print(str(longest_series_query_value)[0:300])
    print('longest_series_query_value', longest_series_query_value)
    if longest_series_query_value is not None and count_list(longest_series_query_value) >= 5:
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
    top_genres_query_value = check_top_genre_exists()
    # print(str(top_genres_query_value)[0:300])

    if top_genres_query_value is not None and count_list(top_genres_query_value) >= 5:
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
