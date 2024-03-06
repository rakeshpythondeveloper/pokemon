from flask import render_template, redirect, request,Blueprint
from deyyam.forms.forms import MyForm
from deyyam.oper.oper import save_image
from deyyam.extensions.db import db
from deyyam.models.models import Pokemon
import requests
from PIL import Image
from io import BytesIO


poker_bp=Blueprint("poker",__name__)
@poker_bp.route("/new", methods=["GET", "POST"])
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
            
            response = requests.get(image_url)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                image = Image.open(image_data)
                image_filename = f"{name.replace(' ', '_')}.png"
                image_path = f"deyyam/static/images/{image_filename}"
                image.save(image_path)
            
                print("Received form data:")
                print(f"Name: {name}, Image URL: {image_url}, Description: {description}, Height: {height}, Weight: {weight}, Category: {category}, Abilities: {abilities}")

                image_path = save_image(image_url, name)

                print("Saved image path:", image_path)

                pokemon = Pokemon(name=name, image_url=image_url, description=description, height=height,
                                weight=weight, category=category, abilities=abilities, image_path=image_path)
                db.session.add(pokemon)
                db.session.commit()

                return redirect("/main")
            else:
                return None

         

    return render_template("newpokemon.html", form=form)

