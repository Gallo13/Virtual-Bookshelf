# Created by: Jess Gallo
# Date Created: 10/13/2024
# Last Modified: 10/13/2024
# Description:

from flask import Blueprint, send_from_directory, session, render_template


home_routes = Blueprint('home', __name__)


@home_routes.route('/', methods=['GET', 'POST'])
def home():
    session['loggedin'] = False
    return render_template('index.html')


# Creates static file path for images
@home_routes.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)
