# Created by: Jess Gallo
# Created date: 09/01/2023
# Last Modified: 10/13/2023
# Description: Virtual Bookshelf Webapp/Storage
# Python, Flask, MySQL

# CHANGE WHERE msg messages go! make into popup!
# add book cover scanner
# web scrapping with isbn to get author fname, lname, publisher, release date, etc.
# create separate files for each function to run faster

# Libraries
import os
from flask import Flask
from home import *
from login import *
from register import *
from get_data import *
from scan_barcode import *
from charts import *

auth = Flask(__name__, template_folder='templates')
auth.secret_key = os.getenv('SECRET_KEY')

auth.register_blueprint(home_routes)
auth.register_blueprint(login_routes)
auth.register_blueprint(register_routes)
auth.register_blueprint(get_data_routes)
auth.register_blueprint(scan_barcode_routes)

# Add the function by name to the jinja environment.
auth.jinja_env.globals.update(top_books=top_books)
auth.jinja_env.globals.update(top_authors=top_authors)
auth.jinja_env.globals.update(oldest_books=oldest_books)
auth.jinja_env.globals.update(longest_series=longest_series)
auth.jinja_env.globals.update(top_genres=top_genres)


if __name__ == '__main__':
    auth.run(debug=True)
