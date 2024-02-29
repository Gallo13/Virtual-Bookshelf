# Created by: Jess Gallo
# Date Created: 01/16/2024
# Last Modified: 01/16/2024
# Description: Recommender System based on user's genre list, author list, and books in library.
# The recommender uses book description and vectorizes it and figures out bok recommendation based on
# the cosine similarity. It uses the GoodReads dataset

# Libraries
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
file = '../books.csv'
data = pd.read_csv(file, header=None, sep='\t')


# Gets book title, author first name, author last name, rating (only books with a score greater than 2) and genre
book_info_query = ("""SELECT b.title, a.firstname, a.lastname, b.rating, g.genre
                    FROM books as b
                    JOIN account_books as ab ON b.bID = ab.bID
                    JOIN book_author as ba ON b.bID = ba.bID
                    JOIN authors as a ON ba.aID = a.aID
                    INNER JOIN book_genre as bg ON b.bID = bg.bID
                    INNER JOIN genre as g ON bg.gID = g.gID
                    WHERE uID = '30bc5133-8e64-4295-aa4d-048fb95cc4ac' AND rating > 2
                    ORDER BY rating DESC;""")
                    # % session['uID'])
                    # WHERE uID = '%s' AND rating > 2

book_info_query_value = ()

# Turning query results into pandas dataframe
book_info_df = pd.DataFrame([[ij for ij in i] for i in book_info_query_value])
book_info_df.columns = ['title', 'fname', 'lname', 'rating', 'genre']

print(book_info_df.head(10))

# Join author first name and last name together in one column
book_info_df['author'] = book_info_df['fname'] + ' ' + book_info_df['lname']

# Drop the separate fname and lname columns
book_info_df.drop(['fname', 'lname'], axis=1, inplace=True)

print(book_info_df.head(10))
print(book_info_df.shape)
print(book_info_df.info())
print(book_info_df.isnull().any())

# Data Cleaning


#

"""
# Create user-defined function to filter books based on genre, author, and book title
def get_book_indices(genre, author, title, data):
    # Get indices of books in selected genre
    genre_books = data[data['genres'].str.contains(genre)]

    # Get indices of books by selected author
    author_books = genre_books[genre_books['authors'].str.contains(author)]

    # Get indices of books with the selected title
    title_books = author_books[author_books['title'].str.contains(title)]

    return title_books.index


# Create a user-defined function to recommend books:
def recommend_books(user_genres, user_authors, user_titles, num_recommendations=5, data=data):
    # Create a TfidfVectorizer to transform the book descriptions into a matrix of TF-IDF features
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(data['description'])

    # Compute the cosine similarity between the books
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Get the indices of books that the user has read
    user_book_indices = [data[data['title'].str.contains(title)].index[0] for title in user_titles]

    # Create a series of cosine similarities from the books the user has read to all other books
    user_book_similarity = sum([list(enumerate(cosine_sim[user_book_index])) for user_book_index in user_book_indices],
                               [])

    # Sort the series of cosine similarities by descending order
    sorted_user_book_similarity = sorted(user_book_similarity, key=lambda x: x[1], reverse=True)

    # Create a list of indices of the top 5 most similar books to the books that the user has read
    top_book_indices = [index for index, score in sorted_user_book_similarity[1:num_recommendations + 1]]

    # Return the titles of the top 5 most similar books
    return data['title'].iloc[top_book_indices]


# Define the user's preferences
user_genres = ['Science Fiction', 'Fantasy']
user_authors = ['Neal Stephenson', 'J.R.R. Tolkien']
user_titles = ['Anathem', 'The Lord of the Rings']

# Generate recommendations
recommendations = recommend_books(user_genres, user_authors, user_titles)

# Print recommendations
print(recommendations)
"""