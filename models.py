from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.Text)
    dept = db.relationship('Post', backref='user_table',
                           cascade="all, delete-orphan")

    def __repr__(self):
        s = self
        return f"< User id = {s.id} first_name = {s.first_name} last_name = {s.last_name} image_url = {s.image_url}>"


class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user_table.id'), nullable=False)
    relation = db.relationship('Tag', secondary='posttag', backref='posts')

    def __repr__(self):
        s = self
        return f"<Posts id {s.id} {s.title} {s.content} {s.created_at}>"


class PostTag(db.Model):

    __tablename__ = 'posttag'

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)


class Tag(db.Model):

    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    def __repr__(self):
        return f'tag_id = {self.id} tag_name={self.name}'
