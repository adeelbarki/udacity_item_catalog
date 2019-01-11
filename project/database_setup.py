from project import db

class Category(db.Model):
    __tablename__ = 'category'
    name = db.Column(db.String(80), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    items = db.relationship('Item')



class Item(db.Model):
    __tablename__ = 'cat_item'
    title = db.Column(db.String(80), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
