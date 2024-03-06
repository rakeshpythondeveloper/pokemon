from flask import Flask, render_template, redirect, request
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
import os
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://avnadmin:AVNS_0ucIPNKYt527QqAQ-Rr@mysql-a5559c2-rakeshdeveloper23-d4e6.a.aivencloud.com:28488/defaultdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

class MyForm(FlaskForm):
    name = StringField('Name')
    image_url = StringField("Image URL", validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    height = FloatField('Height (cm)', validators=[DataRequired()])
    weight = FloatField('Weight (kg)', validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    abilities = StringField("Abilities", validators=[DataRequired()])  
    submit = SubmitField('Submit')

def save_image(image_url, name):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        image_filename = f"{name.replace(' ', '_')}.png"
        image_path = f"static/images/{image_filename}"
        image.save(image_path)
        return image_path
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        search_term = request.form.get("search_term")
        details = Pokemon.query.filter(Pokemon.name.ilike(f'%{search_term}%')).all()
    else:
        details = Pokemon.query.all()
    
    return render_template("index.html", details=details)

@app.route("/new", methods=["GET", "POST"])
def new():
    form = MyForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
            image_url = form.image_url.data
            description = form.description.data
            height = form.height.data
            category = form.category.data
            weight = form.weight.data
            abilities = form.abilities.data

            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                image_data = BytesIO(image_response.content)
                image = Image.open(image_data)
                image_filename = f"{name.replace(' ', '_')}.png"
                image_path = f"pokemon/static/images/{image_filename}"  # Fixed image path

                image.save(image_path)
            else:
                image_path = None
                
            db.session.add(name=name,image_url=image_url,description=description,height=height,category=category,weight=weight,abilities=abilities)
            return redirect("/main")

    return render_template("newpokemon.html", form=form)

@app.route("/delete/<int:pokemon_id>", methods=["POST"])
def delete(pokemon_id):
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    db.session.delete(pokemon)
    db.session.commit()
    return redirect("/main")

@app.route("/update/<int:pokemon_id>", methods=["GET", "POST"])
def update(pokemon_id):
    form = MyForm()

    pokemon = Pokemon.query.get_or_404(pokemon_id)
    if request.method == "POST" and form.validate_on_submit():
        pokemon.name = form.name.data
        pokemon.image_url = form.image_url.data
        pokemon.description = form.description.data
        pokemon.height = form.height.data
        pokemon.weight = form.weight.data
        pokemon.category = form.category.data
        pokemon.abilities = form.abilities.data

        if pokemon.image_path:
            os.remove(pokemon.image_path)
        
        pokemon.image_path = save_image(form.image_url.data, form.name.data)

        db.session.commit()
        return redirect("/")

    form.name.data = pokemon.name
    form.image_url.data = pokemon.image_url
    form.description.data = pokemon.description
    form.height.data = pokemon.height
    form.weight.data = pokemon.weight
    form.category.data = pokemon.category
    form.abilities.data = pokemon.abilities

    return render_template("update.html", form=form)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
@app.route("/registration", methods=["GET", "POST"])
def reg():
    form = RegistrationForm(request.form)
    if  form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        
        print("Received registration data:")
        print(f"Username: {username}, Password: {password}, Confirm Password: {confirm_password}")

        if password == confirm_password:
     
            new_user = users(username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
           
        return "Passwords do not match. Please try again."
    return render_template("reg.html", form=form)

class users(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(100), nullable=False)
     password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

def insert_user_details(username,password):
    user = users(username=username, password=password)     
    db.session.add(user)
    db.session.commit()  

@app.route("/login", methods=["GET", "POST"])
def login():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = users.query.filter_by(username=username).first()
        print(f"Received login data:")
        print(f"Username: {username}, Password: {password}, User: {user}")  # Debug print
        if user and check_password_hash(user.password, password):
            return redirect('/')
        else:
            return "Invalid username or password."
        
    return render_template("login.html", form=form)

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True, port=8000)
