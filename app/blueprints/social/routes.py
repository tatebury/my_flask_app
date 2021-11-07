from sqlalchemy.sql.operators import op
from .import bp as social
from flask import render_template, flash, redirect, url_for, request, g
from app.models import User, Post, Pokemon
from flask_login import login_required, current_user
from random import randrange, choice
from sqlalchemy import and_, or_
from  sqlalchemy.sql.expression import func
from math import ceil

@social.route('/', methods = ['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        body=request.form.get('body')
        new_post=Post(user_id=current_user.id, body=body)
        new_post.save()
        return redirect(url_for('social.index'))
    posts=current_user.followed_posts()
    return render_template('index.html.j2', posts=posts)

@social.route('/show_users')
@login_required
def show_users():
    users = User.query.all()
    pokemon = Pokemon.query.all()
    return render_template('show_users.html.j2', users = users, pokemon = pokemon)

@social.route('/battle/<int:def_id>/<int:fighter_id>/<int:opponent_id>/<int:fight>', methods=['GET','POST'])
@login_required
def battle(def_id, fighter_id, opponent_id, fight=0):
    if def_id > 0:
        g.defender = User.query.get(def_id)


    if opponent_id > 0:
        opponent = Pokemon.query.get(opponent_id)
        if fighter_id > 0:
            fighter = Pokemon.query.get(fighter_id)
            fighterGoesFirst = None
            g.victory = None

            if fight==1:
                fighterHitsToKill = ceil(float(opponent.hp)/(20*float(fighter.attack) / float(opponent.defense)))
                opponentHitsToKill = ceil(float(fighter.hp)/(20*float(opponent.attack) / float(fighter.defense)))

                if fighterHitsToKill < opponentHitsToKill:
                    opponent.set_to_dead()
                    defs_pokemon = Pokemon.query.filter_by(user_id=def_id)
                    notDead=[]
                    for poke in defs_pokemon.all():
                        if poke.is_dead==False:
                            notDead.append(poke)
                    if notDead!=[]:
                        opponent = choice(notDead)
                        return render_template('battle.html.j2', defender=g.defender, fighter=fighter, opponent=opponent)
                    else:
                        g.victory=True
                        # current_user.add_offense_win()
                        # current_user.add_total_battle()
                        # g.defender.add_total_battle()
                        return render_template('battle.html.j2', defender=g.defender, victory=g.victory)


                elif fighterHitsToKill > opponentHitsToKill:
                    fighter.set_to_dead()
                    atts_pokemon = Pokemon.query.filter_by(user_id=current_user.id)
                    notDead=[]
                    for poke in atts_pokemon.all():
                        if poke.is_dead==False:
                            notDead.append(poke)
                    if notDead==[]:
                        g.victory=False
                        # g.defender.add_defense_win()
                        # g.defender.add_total_battle()
                        # current_user.add_total_battle()
                        return render_template('battle.html.j2', defender=g.defender, victory=g.victory)

                    return render_template('battle.html.j2', defender=g.defender, fighter=fighter, opponent=opponent)
                else:
                    if fighter.base_xp < opponent.base_xp:
                        fighterGoesFirst=True
                        victory=True
                    elif fighter.base_xp > opponent.base_xp:
                        fighterGoesFirst=False
                        victory=False
                    else:
                        fighterGoesFirst=choice([True,False])
                        victory=fighterGoesFirst
                    return render_template('battle.html.j2', defender=g.defender, victory=victory)

            return render_template('battle.html.j2', defender=g.defender, fighter=fighter, opponent=opponent, fighterGoesFirst=fighterGoesFirst)
        else:
            return render_template('battle.html.j2', defender=g.defender, opponent=opponent)
    else:
        defs_pokemon = Pokemon.query.filter_by(user_id=def_id)
        Pokemon().revive_all_pokemon()
        opponent = defs_pokemon.order_by(func.random()).first()
        flash(f"You challenged {g.defender.first_name} {g.defender.last_name} to a PokeBattle", 'warning')

        return render_template('battle.html.j2', defender = g.defender, opponent = opponent)

# @social.route('/fight/<int:fighter_id>/<int:opponent_id>', methods=['GET','POST'])
# @login_required
# def fight(fighter_id, opponent_id):
#     fighter = Pokemon.query.get(fighter_id)
#     opponent = Pokemon.query.get(opponent_id)

#     fighterHitsToKill = ceil(float(opponent.hp)/(20*float(fighter.attack) / float(opponent.defense)))
#     opponentHitsToKill = ceil(float(fighter.hp)/(20*float(opponent.attack) / float(fighter.defense)))

#     if fighterHitsToKill < opponentHitsToKill:
#         opponent.is_dead = True
#         return render_template('fight.html.j2', fighter_id = fighter_id, opponent_id = opponent_id)
#     elif fighterHitsToKill > opponentHitsToKill:
#         fighter.is_dead = True
#         return render_template('fight.html.j2', fighter_id = fighter_id, opponent_id = opponent_id)
#     else:
#         if fighter.base_xp < opponent.base_xp:
#             fighterGoesFirst = True
#         else:
#             fighterGoesFirst = False
        
#     return render_template('fight.html.j2', fighterGoesFirst = fighterGoesFirst)

@social.route('/edit_post/<int:id>', methods=['GET','POST'])
@login_required
def edit_post(id):

    post = Post.query.get(id)
    if request.method == 'POST':
        post.edit(request.form.get('body'))
        flash("Your post has been edited","success")
    return render_template('edit_post.html.j2', post=post)
