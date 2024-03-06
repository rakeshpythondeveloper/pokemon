
from deyyam.extensions.db import db



class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    abilities = db.Column(db.String(200), nullable=False)
    image_path = db.Column(db.String(200), nullable=True)

class users(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(100), nullable=False)
     password = db.Column(db.String(200), nullable=False)