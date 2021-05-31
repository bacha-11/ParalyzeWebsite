from datetime import datetime
from enum import unique
from app import db



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False, unique=True)
    image = db.Column(db.LargeBinary)
    image_name = db.Column(db.String(64))
    article = db.Column(db.Text, nullable=False)
    article_views = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return 'Post -> {}'.format(self.title)



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    price = db.Column(db.String(264), nullable=False)
    product_url = db.Column(db.String(500), nullable=False)
    product_image = db.Column(db.LargeBinary)
    product_image_name = db.Column(db.String(64))
    product_views = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __str__(self):
        return "Product -> {}".format(self.title)



class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(132), nullable=False, unique=True)

    def __str__(self):
        return 'Email -> {}'.format(self.email)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(132), nullable=False)
    email = db.Column(db.String(132), nullable=False)
    question = db.Column(db.String(500), nullable=False)

    def __str__(self):
        return 'Name -> {}'.format(self.name)




