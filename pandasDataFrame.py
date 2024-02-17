# Created by: Jess Gallo
# Created on: 02/05/2024
# Last Modified on: 02/05/2024
# Description: Turning MySQL Database into pandas dataframe

import pandas as pd
import mysql.connector
import numpy as np

# export mysql datatabase into csv file
query = ("SELECT b.title, a.firstname, a.lastname, b.rating, g.genre, s.seriesName "
         "FROM books as b "
         "INNER JOIN account_books as ab ON b.bID = ab.bID "
         "INNER JOIN book_author as ba ON b.bID = ba.bID"
         "INNER JOIN authors as a ON ba.aID = a.aID"
         "INNER JOIN book_genre as bg ON b.bID = bg.bID"
         "INNER JOIN genre as g ON bg.gID = g.gID"
         "LEFT JOIN book_series as bs ON b.bID = bs.bID"
         "LEFT JOIN series as s ON bs.sID = s.sID"
         "WHERE uID = '30bc5133-8e64-4295-aa4d-048fb95cc4ac' AND rating > 2"
         "ORDER BY rating DESC LIMIT 100"
         "INTO OUTFILE 'C:/Users/Gallo/Desktop/Python/book_info.csv';")
