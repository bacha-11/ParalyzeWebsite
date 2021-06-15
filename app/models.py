from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import datetime
from enum import unique
from app import db
import json
from time import time


class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    last_contact_read_time = db.Column(db.DateTime)
    last_sub_read_time = db.Column(db.DateTime)

    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')

    def __repr__(self):
        return 'Admin -> {}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    
    def new_contact(self):
        last_read_time = self.last_contact_read_time or datetime(1900, 1, 1)
        return Contact.query.filter(Contact.timestamp > last_read_time).count()


    def new_subscriber(self):
        last_read_time = self.last_sub_read_time or datetime(1900, 1, 1)
        return Subscriber.query.filter(Subscriber.timestamp > last_read_time).count()

    
    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n


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
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return 'Email -> {}'.format(self.email)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(132), nullable=False)
    email = db.Column(db.String(132), nullable=False)
    question = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return 'Name -> {}'.format(self.name)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('owner.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))

