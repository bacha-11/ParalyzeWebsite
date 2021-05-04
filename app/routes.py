from app import app
from flask import redirect, render_template, url_for


@app.route('/')
def index():
    return render_template('index.html', title='Home Page')



@app.route('/blog')
def blog():
    return render_template('blog.html', title='Blog')


@app.route('/shop')
def shop():
    return render_template('shop.html', title='Shop')