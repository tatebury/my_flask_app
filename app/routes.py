
   
from flask import render_template, request, redirect, url_for
import requests
from app import app
from .forms import LoginForm, PokeNameForm, RegisterForm
from .models import User
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
@login_required
def home():
    return render_template('home.html.j2')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Do login Stuff
        email = request.form.get("email").lower()
        password = form.password.data
        u = User.query.filter_by(email=email).first()
        print(u)
        if u is not None and u.check_hashed_password(password):
            login_user(u)
            # Give User feeedback of success
            return redirect(url_for('home'))
        else:
            # Give user Invalid Password Combo error
            return redirect(url_for('login'))
    return render_template("login.html.j2", form=form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user is not None:
        logout_user()
        return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data={
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email": form.email.data.lower(),
                "password": form.password.data
            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
        except:
            error_string="There was a problem creating your account. Please try again"
            return render_template('register.html.j2',form=form, error=error_string)
        # Give the user some feedback that says registered successfully 
        return redirect(url_for('login'))

    return render_template('register.html.j2',form=form)

@app.route('/pokemon', methods=['GET', 'POST'])
@login_required
def pokemon():
    form = PokeNameForm()
    poke_list = requests.get("https://pokeapi.co/api/v2/pokemon/")
    if request.method == 'POST':
        names = request.form.get('name').split(',')
        pokemon_info = []
        for name in names:
            name = name.strip().lower()
            url = f'https://pokeapi.co/api/v2/pokemon/{name}'
            response = requests.get(url)
            if response.ok:
                #request worked
                if not response.json():
                    return "We had an error loading your pokemon likely the name is not in the pokemon database"
                pokemon = response.json()

                single_poke={
                    'name': pokemon['name'],
                    'base_xp': pokemon['base_experience'],
                    'hp': pokemon['stats'][0]['base_stat'],
                    'defense': pokemon['stats'][2]['base_stat'],
                    'attack': pokemon['stats'][1]['base_stat'],
                    'url': pokemon['sprites']['front_shiny']
                }
                pokemon_info.append(single_poke)

            
            else:
                return "Houston We have a problem"
                # The request fail

        return render_template('pokemon.html.j2', pokemon=pokemon_info, form=form)     
        

    return render_template('pokemon.html.j2', form=form)