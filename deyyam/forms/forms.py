
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm



class MyForm(FlaskForm):
    name = StringField('Name')
    image_url = StringField("Image URL", validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    height = FloatField('Height (cm)', validators=[DataRequired()])
    weight = FloatField('Weight (kg)', validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    abilities = StringField("Abilities", validators=[DataRequired()])  
    submit = SubmitField('Submit')

class loginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('register')