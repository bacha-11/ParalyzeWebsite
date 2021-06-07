from sqlalchemy.orm import query
from app import app, db
from base64 import b64encode
from app.models import Contact, Post, Product, Subscriber
from flask import redirect, request, render_template, url_for, flash, g, session, make_response
from werkzeug.utils import secure_filename

app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]




@app.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()[0:6]

    if request.method == 'POST':
        email = request.form['email']

        subscriber = Subscriber.query.filter_by(email=email).first()
        if subscriber:
            flash('Already subscribe our news least!', "warning")
            return redirect(url_for('index'))  

        new_sub = Subscriber(email=email)
        db.session.add(new_sub)
        db.session.commit()
        flash("Successfully subscribe our news least!", "success")
        return redirect(url_for('index'))
    
    return render_template('client/index.html', title='Home Page', posts=posts, b64encode=b64encode)



@app.route('/blog', methods=['GET', 'POST'])
def blog():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.paginate(
        page, app.config["POST_PER_PAGE"], False
    )
    next_url = url_for('blog', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('blog', page=posts.prev_num) \
        if posts.has_prev else None

    if request.method == 'POST':
        email = request.form['email']

        subscriber = Subscriber.query.filter_by(email=email).first()
        if subscriber:
            flash('Already subscribe our news least!', "warning")
            return redirect(url_for('blog'))  

        new_sub = Subscriber(email=email)
        db.session.add(new_sub)
        db.session.commit()
        flash("Successfully subscribe our news least!", "success")
        return redirect(url_for('blog'))

    return render_template('client/blog.html', title='Blog', posts=posts.items, next_url=next_url, prev_url=prev_url, b64encode=b64encode)


@app.route('/post-detial-view/<id>', methods=['GET', 'POST'])
def post_view(id):
    posts = Post.query.order_by(Post.timestamp.desc()).all()[0:9]
    post = Post.query.filter_by(id=id).first()
    image = b64encode(post.image).decode("utf-8")
    post.article_views = post.article_views + 1
    db.session.commit()

    if request.method == 'POST':
        email = request.form['email']

        subscriber = Subscriber.query.filter_by(email=email).first()
        if subscriber:
            flash('Already subscribe our news least!', "warning")
            return redirect(url_for('post_view', id=post.id))  

        new_sub = Subscriber(email=email)
        db.session.add(new_sub)
        db.session.commit()
        flash("Successfully subscribe our news least!", "success")
        return redirect(url_for('post_view', id=post.id))

    return render_template('client/post_view.html', title='Blog Post', post=post, image=image, posts=posts)


@app.route('/shop-products', methods=['GET', 'POST'])
def shop():
    products = Product.query.all()

    if request.method == 'POST':
        email = request.form['email']

        subscriber = Subscriber.query.filter_by(email=email).first()
        if subscriber:
            flash('Already subscribe our news least!', "warning")
            return redirect(url_for('shop'))  

        new_sub = Subscriber(email=email)
        db.session.add(new_sub)
        db.session.commit()
        flash("Successfully subscribe our news least!", "success")
        return redirect(url_for('shop'))

    return render_template('client/shop.html', title='Shop', products=products, b64encode=b64encode)



@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        question = request.form['question']
        new_contact = Contact(name=name, email=email, question=question)
        db.session.add(new_contact)
        db.session.commit()
        flash('{} your query is successfully send!'.format(name.title()), "success")
        return redirect(url_for('contact'))
        
    return render_template('client/contact.html', title='Contact')


@app.route('/about')
def about():
    return render_template('client/about.html', title='About')




# Dashboard code start from here
admin_username = ['admin']
admin_password = ['admin']



# @app.before_request
# def before_request():
#     g.admin_username



@app.route('/admin-login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # user = [x for x in admin if admin.username == username][0]

        if username in admin_username and password in admin_password:
            session['username'] = admin_username
            flash('Successfully Login', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Username or Password', 'warning')
            return redirect(url_for('login'))

    return render_template('owner/owner_login.html', title='Admin Login')



@app.route('/admin-registration')
def registration():
    return render_template('owner/owner_registration.html', title='Admin Registration')


@app.route('/list-of-admin', methods=['GET', 'POST'])
def list_of_admin():
    return render_template('owner/list_of_admin.html', title='Admin List')


@app.route('/dashboard')
def dashboard():
    post_count = Post.query.all()
    product_count = Product.query.all()
    sub_count = Subscriber.query.all()
    posts = Post.query.order_by(Post.timestamp.desc()).all()[0:5]
    subscribers = Subscriber.query.order_by(Subscriber.id.desc()).all()[0:6]

    query = request.args.get('query')
    if query:
        search_post = Post.query.filter(Post.title.contains(query)).all()
        return render_template('owner/owner_search_post.html', title='Search Result', search_post=search_post, query=query)

    return render_template('owner/owner_index.html', title='Admin Dashboard', posts=posts, post_count=post_count, product_count=product_count, sub_count=sub_count, subscribers=subscribers)



def allowed_image(filename):

    if not '.' in filename:
        flash("File must have '.' !")
        return False

    ext = filename.rsplit('.',1)[1]
    if ext.upper() in app.config['ALLOWED_IMAGE_EXTENSIONS']:
        return True
    else:
        flash('File must be PNG, JPG, JPEG, GIF !', "danger")
        return False


@app.route('/addpost', methods=['GET', 'POST'])
def addpost():
    posts = Post.query.all()
    if request.method == 'POST':
        title = request.form['title']
        article = request.form['article']


        for check_title in posts:
            if title == check_title.title:
                flash('Title already present chose a different title!', "danger")
                return redirect(url_for('addpost'))


        image = request.files['image']

        if image.filename == '':
            flash('File must have name!', "warning")
            return redirect(url_for('addpost'))

        if allowed_image(image.filename):
            image_name = secure_filename(image.filename)

            new_post = Post(title=title, image=image.read(), image_name=image_name, article=article)
            db.session.add(new_post)
            db.session.commit()
            flash('Post successfully added!', "success")
            return redirect(url_for('addpost'))

    
    query = request.args.get('query')
    if query:
        search_post = Post.query.filter(Post.title.contains(query)).all()
        return render_template('owner/owner_search_post.html', title='Search Result', search_post=search_post, query=query)

    return render_template('owner/owner_addpost.html', title='Add Post', post=None)



@app.route('/owner_post_view/<id>')
def owner_post_view(id):
    post = Post.query.filter_by(id=id).first()
    image = b64encode(post.image).decode("utf-8")
    return render_template('owner/owner_post_view.html', title='Post Detial View', post=post, image=image)



@app.route('/post')
def post():
    query = request.args.get('query')
    if query:
        search_post = Post.query.filter(Post.title.contains(query)).all()
        return render_template('owner/owner_search_post.html', title='Search Result', search_post=search_post, query=query)
    
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False
    ) 
    next_url = url_for('post', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('post', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('owner/owner_post.html', title='Post', posts=posts.items, next_url=next_url, prev_url=prev_url)



@app.route('/delete_post/<id>')
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    flash('Post successfully deleted!', "success")
    return redirect(url_for('post'))



@app.route('/edit_post/<id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.filter_by(id=id).first()
    if request.method == 'POST':
        post.title = request.form['title']
        post.article = request.form['article']
        img = request.files['image']

        if img.filename == '':
            flash('File must have name!', "warning")
            return redirect(url_for('edit_post'))

        if allowed_image(img.filename):
            post.image_name = img.filename
            post.image = img.read()
            db.session.commit()
            return redirect(url_for('post'))
    return render_template('owner/owner_addpost.html', title='Edit Post', post=post)



@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        product_url = request.form['product_url']
        product_image = request.files['product_image']
        
        if product_image.filename == '':
            flash('File must have name!', "warning")
            return redirect(url_for('addproduct'))

        if allowed_image(product_image.filename):
            product_image_name = secure_filename(product_image.filename)

            new_product = Product(title=title, 
                                 price=price, 
                                 product_url=product_url, 
                                 product_image=product_image.read(), 
                                 product_image_name=product_image_name)
            db.session.add(new_product)
            db.session.commit()
            flash('Product successfully added!', "success")
            return redirect(url_for('addproduct'))


    query = request.args.get('query')
    if query:
        search_product = Product.query.filter(Product.title.contains(query)).all()
        return render_template('owner/owner_search_post.html', title='Search Result', search_product=search_product, query=query)

    return render_template('owner/owner_addproduct.html', title='Add Product', product=None)



@app.route('/edit_product/<id>', methods=["GET", "POST"])
def edit_product(id):
    product = Product.query.filter_by(id=id).first()
    
    if request.method == "POST":
        product.title = request.form["title"]
        product.price = request.form['price']
        product.product_url = request.form['product_url']
        product_image = request.files['product_image']

        if product_image.filename == '':
            flash('File must have name', "warning")
            return redirect(url_for('edit_image'))

        if allowed_image(product_image.filename):
            product.product_image_name = secure_filename(product_image.filename)
            product.product_image = product_image.read()
            db.session.commit()
            flash('Product successfully updated!', "success")
            return redirect(url_for('product'))

    return render_template('owner/owner_addproduct.html', title='Edit Product', product=product)



@app.route('/delete_product/<id>')
def delete_product(id):
    product = Product.query.filter_by(id=id).first()
    db.session.delete(product)
    db.session.commit()
    flash('Product successfully deleted!', "success")
    return redirect(url_for('product'))



@app.route('/product')
def product():
    query = request.args.get('query')
    if query:
        search_product = Product.query.filter(Product.title.contains(query)).all()
        return render_template('owner/owner_search_post.html', title='Search Result', search_product=search_product, query=query)

    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False
    )
    next_url = url_for('product', page=products.next_num) \
        if products.has_next else None
    prev_url = url_for('product', page=products.prev_num) \
        if products.has_prev else None

    return render_template('owner/owner_product.html', title='Product', products=products.items, next_url=next_url, prev_url=prev_url)



@app.route('/owner_product_view/<id>')
def owner_product_view(id):
    product = Product.query.filter_by(id=id).first()
    image = b64encode(product.product_image).decode('utf-8')
    return render_template('owner/owner_product_view.html', title='Product Detial View', product=product, image=image)



@app.route('/subscriber')
def subscriber():
    page = request.args.get('page', 1, type=int)
    subscribers = Subscriber.query.order_by(Subscriber.id.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False
    )

    next_url = url_for('subscriber', page=subscribers.next_num) \
        if subscribers.has_next else None

    prev_url = url_for('subscriber', page=subscribers.prev_num) \
        if subscribers.has_prev else None


    query = request.args.get('query')
    if query:
        search_email = Subscriber.query.filter(Subscriber.email.contains(query)).all()
        return render_template('owner/owner_search_post.html', title='Search Result', search_email=search_email, query=query)

    return render_template('owner/owner_subscriber.html', title='Subscriber', subscribers=subscribers.items, next_url=next_url, prev_url=prev_url)


@app.route('/delete_subscriber<id>')
def delete_subscriber(id):
    subscriber = Subscriber.query.filter_by(id=id).first()
    db.session.delete(subscriber)
    db.session.commit()
    flash("Successfully deleted!", "success")
    return redirect(url_for('subscriber'))



@app.route('/contact-list')
def contact_list():
    page = request.args.get('page', 1, type=int)
    contacts = Contact.query.order_by(Contact.id.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False
    )
    next_url = url_for('contact_list', page=contacts.next_num) \
        if contacts.has_next else None
    prev_url = url_for('contact_list', page=contacts.prev_num) \
        if contacts.has_prev else None

    return render_template('owner/owner_contact_view.html', title='Contact', contacts=contacts.items, next_url=next_url, prev_url=prev_url)


@app.route("/delete_contact/<id>")
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash("Successfully Deleted!", "success")
    return redirect(url_for("contact_list"))


@app.route('/contact_detial_view/<id>')
def contact_detial_view(id):
    contact = Contact.query.filter_by(id=id).first()
    return render_template('owner/contact_detial_view.html', title='Contact Detial View', contact=contact)


# End Dashboard