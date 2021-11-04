from app import db
from flask import render_template, request, flash, redirect
from flask.helpers import url_for
import requests
from app.models import Pokemon, User
from flask_login import login_required, current_user
from .import bp as main
from .forms import PokeNameForm

@main.route('/', methods=['GET'])
@login_required
def index():
    
    return render_template('home.html.j2')

@main.route('/pokemon', methods=['GET', 'POST'])
@login_required
def pokemon(resent = False):
    form = PokeNameForm()
    poke_list = requests.get("https://pokeapi.co/api/v2/pokemon/")
    if request.method == 'POST':
        names = request.form.get('name').strip(',').split(',')
        
        pokemon_info = []
        for name in names:
            name = name.strip(', ').lower()

            if ',' in name or name=="":
                flash('We could not find that entry in our database.', 'danger')
                return redirect(url_for('main.pokemon'))
            url = f'https://pokeapi.co/api/v2/pokemon/{name}'
            response = requests.get(url)
            print(url)
            if response.ok:
                #request worked
                if not response.json():
                    flash('We had an error loading your pokemon likely the name is not in the pokemon database','danger')
                    return redirect(url_for('main.pokemon'))
                pokemon = response.json()

                single_poke={
                    'name': pokemon['name'],
                    'ability': pokemon['forms'][0]['name'],
                    'base_xp': pokemon['base_experience'],
                    'hp': pokemon['stats'][0]['base_stat'],
                    'defense': pokemon['stats'][2]['base_stat'],
                    'attack': pokemon['stats'][1]['base_stat'],
                    'url': pokemon['sprites']['front_shiny']
                }



                # if current_user.has_caught(single_poke):
                #     flash(f'You already have a {name}', 'danger')
                # else:
                new_pokemon = Pokemon()
                new_pokemon.user_id = current_user.id
                new_pokemon.from_dict(single_poke)
                new_pokemon.save()
                current_user.remove_duplicates()
                #     flash('You have added a new Pokemon!', 'success')


                pokemon_info.append(new_pokemon)


            
            else:
                flash('We could not find that entry in our database.', 'danger')
                return redirect(url_for('main.pokemon'))

        return render_template('pokemon.html.j2', pokemon=pokemon_info, form=form)     
        

    return render_template('pokemon.html.j2', form=form)


@main.route('/show_pokemon', methods=['GET','POST'])
@login_required
def show_pokemon():

    pokemon = current_user.pokemon.all()
    return render_template('show_pokemon.html.j2', pokemon = pokemon)

@main.route('/remove_pokemon/<int:id>', methods=['GET','POST'])
@login_required
def remove_pokemon(id):
    poke = Pokemon.query.get(id)
    if request.method=='POST': 
        current_user.release(poke)
        flash(f'{poke.name} has been released', 'warning')
        return redirect(url_for('main.show_pokemon'))

@main.route('/add_pokemon/<int:id>', methods=['GET','POST'])
@login_required
def add_pokemon(id):
    poke = Pokemon.query.get(id)
    if request.method=='POST': 
        current_user.catch(poke)
        flash(f'{poke.name} has been caught', 'success')
        return redirect(url_for('main.pokemon'))


# @main.route('/to_fight/<int:def_id>/<int:fighter_id>', methods=['GET','POST'])
# @login_required
# def to_fight(def_id, fighter_id):
#     fighter = Pokemon.query.get(id)
#     if request.method=='POST':
#         return redirect(url_for('main.show_pokemon'), fighter = fighter)
#             user_to_battle = User.query.get(id)
#     # current_user.battle(user_to_battle)
#     return render_template('battle.html.j2', defender = user_to_battle)

