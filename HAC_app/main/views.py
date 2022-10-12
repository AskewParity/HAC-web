from flask import Blueprint
from flask import render_template


main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
@main.route('/index')
def index():
    return render_template('home.html')
