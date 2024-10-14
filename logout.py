# Created by: Jess Gallo
# Date Created: 10/13/2024
# Last Modified: 10/13/2024
# Description:

from flask import Blueprint, session, render_template

logout_routes = Blueprint('logout', __name__)


@logout_routes.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.clear()
    msg = 'You have successfully logged out'
    # return redirect(url_for('login.login'))
    return render_template('index.html', msg=msg)
