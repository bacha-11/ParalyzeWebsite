from datetime import datetime
from app import db



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False, unique=True)
    image = db.Column(db.LargeBinary)
    image_name = db.Column(db.String(64))
    article = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return 'Post -> {}'.format(self.title)
