from app import app
from flask import redirect, render_template, url_for


@app.route('/')
def index():
    return render_template('index.html', title='Home Page')



@app.route('/blog')
def blog():
    return render_template('blog.html', title='Blog')


@app.route('/post_view')
def post_view():
    return render_template('post_view.html', title='Blog Post')


@app.route('/shop')
def shop():
    return render_template('shop.html', title='Shop')


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


# Dashboard code start from here

@app.route('/dashboard')
def dashboard():
    return render_template('owner/owner_index.html', title='Admin Dashboard')



@app.route('/post')
def post():
    return render_template('owner/owner_post.html', title='Post')



@app.route('/product')
def product():
    return render_template('owner/owner_product.html', title='Product')



@app.route('/subscriber')
def subscriber():
    return render_template('owner/owner_subscriber.html', title='Subscriber')



@app.route('/addpost')
def addpost():
    return render_template('owner/owner_addpost.html', title='Add Post')



@app.route('/addproduct')
def addproduct():
    return render_template('owner/owner_addproduct.html', title='Add Product')



@app.route('/owner_post_view')
def owner_post_view():
    return render_template('owner/owner_post_view.html', title='Add Product')


# End Dashboard