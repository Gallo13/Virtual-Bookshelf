# Create by: Jess Gallo
# Date created: 10/13/2024
# Last Modified: 10/13/2024
# Description:

import os
from account_login import *
from flask import Blueprint, render_template, request, session

login_routes = Blueprint('login', __name__)
login_routes.secret_key = os.getenv('SECRET_KEY')


@login_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Stores email and password into variables
        email = request.form['email']
        password = request.form['password']

        # Retrieve the hashed password
        hash_pw = hash_password(password, login_routes.secret_key)

        # Check if account exists using MySQL
        login_query_value = login_confirmation(email, hash_pw)

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
            session['uID'] = login_query_value
            return render_template('login.html')