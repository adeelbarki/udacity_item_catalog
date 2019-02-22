from datetime import datetime
from project import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    picture = db.Column(db.String(250))



class Category(db.Model):
    __tablename__ = 'category'
    name = db.Column(db.String(80), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    items = db.relationship('Item')

    # serializable format
    @property
    def serialize(self):

        return {
            'name': self.name,
            'id': self.id,
            
        }


class Item(db.Model):
    __tablename__ = 'cat_item'
    title = db.Column(db.String(80), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')

    # serializable format
    @property
    def serialize(self):

        return {
            'title': self.title,
            'description': self.description,
            'id': self.id,
            'cat_id': self.cat_id,
        }

