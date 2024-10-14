# Created by: Jess Gallo
# Date created: 10/13/2024
# Last Modified: 10/13/2024
# Description:

import re
import os
from flask import Blueprint, render_template, request
from flask_bcrypt import Bcrypt
from account_login import *


register_routes = Blueprint('register', __name__)
register_routes.secret_key = os.getenv('SECRET_KEY')

main = 'index.html'


@register_routes.route('/register', methods=['GET', 'POST'])
def register():
    # Check if "email", "password" POST requirements exist (user submitted form)
    if request.method == 'POST':
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        # Check if account exists using MySQL
        account_query_value = check_account_exists(email)

        # If account exists show error and validation checks
        if account_query_value is not None:
            msg = 'Account already exists!'
            return render_template(main, msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            return render_template(main, msg=msg)
        elif not email or not password:
            msg = 'Please fill out the form!'
            return render_template(main, msg=msg)
        elif password != password2:
            msg = 'Passwords do not match'
            return render_template(main, msg=msg)
        else:
            # Hash the password
            hash_pw = hash_password(password, register_routes.secret_key)

            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            insert_account_data(email, hash_pw)
            print("Account Added:, ", email, hash_pw)
            msg = 'You have successfully registered! Please login!'
            return render_template(main, msg=msg)

    return render_template(main)
