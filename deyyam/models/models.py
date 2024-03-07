from flask_login import UserMixin
from deyyam.extensions.db import db
from werkzeug.security import check_password_hash



class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    abilities = db.Column(db.String(200), nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"), nullable=False)
    image_path = db.Column(db.String(200), nullable=True)
    like_c=db.relationship("LIKE_SE",backref="pokemon", lazy=True)
    

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    profile_image = db.Column(db.String(200), nullable=False, default="default.png")
    pokemons = db.relationship("Pokemon", backref="user", lazy=True)

     
     
    def check_pwd_hash(self,password):
        return check_password_hash(self.password,password)
    
     
     
     
     
class LIKE_SE(db.Model):
    __tablename__="likese"
    id=db.Column  (db.Integer,primary_key=True)     
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"), nullable=False)
    pokemon_id=db.Column(db.Integer,db.ForeignKey("pokemon.id"),nullable=False)