from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '10a8bc5c5154fd95af8cd8fc5ae07b3c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///categorymenu.db'
db = SQLAlchemy(app)


from project import routes