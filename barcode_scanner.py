# Created by: Jess Gallo
# Date Created: 02/28/24
# Last Modified: 03/03/24
# Description: Barcode scanner using OpenCV. Barcode will get ISBN


# print(cv2.getBuildInformation())

import cv2
from pyzbar import pyzbar
import requests

"""
Decodes barcodes from the given frame
Args:
    frame: The frame to decode barcodes

Returns:
    The ISBN of the barcode found if found, otherwise None.
"""


def validate_isbn(isbn_bc):
    """
    Validates the given ISBN
    Args:
        isbn_bc (str): The ISBN to validate

    Returns:
        True if the ISBN is valid, otherwise False.
    """
    if len(isbn_bc) != 13:
        return False

    # calculate the checksum
    checksum = 0
    for i in range(12):
        digit = int(isbn_bc[i])
        checksum += digit * (3 if i % 2 == 0 else 1)

    # calculate the check digit
    check_digit = 10 - (checksum % 10)
    if check_digit == 10:
        check_digit = 0

    # check if the check digit matches the last digit of the ISBN
    return check_digit == int(isbn_bc[-1])


def get_book_info(isbn):
    # Fetch data using the ISBN
    response = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn)
    data = response.json()
    if 'items' in data:
        book_info = data['items'][0]['volumeInfo']
        title = book_info['title']
        pages = book_info['pageCount']
        authors = ', '.join(book_info['authors'])
        publisher = book_info['publisher']
        published_date = book_info['publishedDate']
        return title, pages, authors, publisher, published_date
    return None
