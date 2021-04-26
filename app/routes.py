from app import app
from flask import redirect, render_template, url_for


@app.route('/')
def index():
    return render_template('index.html', title='Home Page')