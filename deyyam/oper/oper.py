from deyyam.models.models import users
from deyyam.extensions.db import db
from deyyam.models.models import Pokemon
import requests
from PIL import Image
from io import BytesIO

def save_image(image_url, name):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        image_filename = f"{name.replace(' ', '_')}.png"
        image_path = f"deyyam/static/images/{image_filename}"
        image.save(image_path)
        return image_path
    else:
        return None
    
def insert_user_details(username,password):
    user = users(username=username, password=password)     
    db.session.add(user)
    db.session.commit()  

def fetch_pokemon_by_id(pokemon_id):
    return Pokemon.query.get(pokemon_id)
def update_pokemon_data(pokemon_id, form):
    pokemon = Pokemon.query.get(pokemon_id)
    pokemon.name = form.name.data
    pokemon.image_url = form.image_url.data
    pokemon.description = form.description.data
    pokemon.height = form.height.data
    pokemon.weight = form.weight.data
    pokemon.category = form.category.data
    pokemon.abilities = form.abilities.data
    db.session.commit()