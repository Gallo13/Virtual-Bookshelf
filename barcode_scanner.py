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


def read_barcode(frame):
    barcodes = pyzbar.decode(frame)
    barcode_read = False
    isbn_bc = None
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        # take the information from the barcode
        barcode_info = barcode.data.decode('utf-8')
        # draw a rectangle around the barcode
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # put text on top of rectangle so information can be read as text
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)

        print("Recognized Barcode:",  barcode_info)
        barcode_read = True
        isbn_bc = barcode_info
    # return the bounding box of the barcode
    return frame, barcode_read, isbn_bc


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


"""
 def print_barcode():
        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()
        barcode_read = False
        isbn_bc = None
        while ret and not barcode_read:
            ret, frame = camera.read()
            frame, barcode_read, isbn_bc = read_barcode(frame)
            cv2.imshow('Real Time Barcode Scanner', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        camera.release()
        cv2.destroyAllWindows()
        return isbn_bc

    isbn = print_barcode()
    if isbn:
        print('ISBN detected:', isbn)
    else:
        print('ISBN not detected')

    return render_template(login)

"""
