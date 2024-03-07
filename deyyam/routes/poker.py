from flask import render_template, redirect, request,Blueprint,flash
from deyyam.forms.forms import MyForm
from deyyam.oper.oper import save_image
from deyyam.extensions.db import db
from deyyam.models.models import Pokemon
from flask_login import current_user
import requests
from PIL import Image
from io import BytesIO
from deyyam.oper.oper import insert_pokemon_data


poker_bp=Blueprint("poker",__name__)
@poker_bp.route("/new", methods=["GET", "POST"])
def new():
    form = MyForm(request.form)
    pokemon_exists = False 
    if form.validate_on_submit():
        name = form.name.data

       
        existing_pokemon = Pokemon.query.filter_by(name=name).first()

        if existing_pokemon:
            pokemon_exists = True  
            flash("This Pokémon already exists!", "error")
            return render_template("newpokemon.html", form=form, pokemon_exists=pokemon_exists) 
        else:
            image_url = form.image_url.data
            description = form.description.data
            height = form.height.data
            category = form.category.data
            weight = form.weight.data
            abilities = form.abilities.data

        
            if current_user.is_authenticated:
                user_id = current_user.id

                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image_data = BytesIO(image_response.content)
                    image = Image.open(image_data)
                    image_filename = f"{name.replace(' ', '_')}.png"
                    image_path = f"deyyam/static/images/{image_filename}" 

                    image.save(image_path)
                else:
                    image_path = None

                insert_pokemon_data(name, image_url, description, height, weight, category, abilities, image_path, user_id)

                flash("New Pokémon added successfully!", "success")
                return redirect("/main")

    return render_template("newpokemon.html", form=form, pokemon_exists=pokemon_exists)

