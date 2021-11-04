from .import bp as social
from flask import render_template, flash, redirect, url_for, request
from app.models import User, Post, Pokemon
from flask_login import login_required, current_user

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

@social.route('/battle/<int:def_id>/<int:fighter_id>', methods=['GET','POST'])
@login_required
def battle(def_id, fighter_id):
    user_to_battle = User.query.get(def_id)
    defs_pokemon = Pokemon.query.filter_by(user_id=def_id).first()
    if fighter_id > 0:
        fighter = Pokemon.query.get(fighter_id)
        return render_template('battle.html.j2', defender = user_to_battle, fighter = fighter, opponent = defs_pokemon)
    elif fighter_id == 0:
        return render_template('battle.html.j2', defender = user_to_battle, opponent = defs_pokemon)

    # flash(f"You challenged {user_to_battle.first_name} {user_to_battle.last_name} to a PokeBattle", 'warning')
    return render_template('battle.html.j2', defender = user_to_battle)


# @social.route('/unfollow/<int:id>')
# @login_required
# def unfollow(id):
#     user_to_unfollow = User.query.get(id)
#     current_user.unfollow(user_to_unfollow)
#     flash(f"You are no longer following {user_to_unfollow.first_name} {user_to_unfollow.last_name}", 'warning')
#     return redirect(url_for('social.show_users'))

@social.route('/edit_post/<int:id>', methods=['GET','POST'])
@login_required
def edit_post(id):

    post = Post.query.get(id)
    if request.method == 'POST':
        post.edit(request.form.get('body'))
        flash("Your post has been edited","success")
    return render_template('edit_post.html.j2', post=post)

# @main.route('/to_fight/<int:def_id>/<int:fighter_id>', methods=['GET','POST'])
# @login_required
# def to_fight(def_id, fighter_id):
#     fighter = Pokemon.query.get(id)
#     if request.method=='POST':
#         return redirect(url_for('main.show_pokemon'), fighter = fighter)
#             user_to_battle = User.query.get(id)
#     # current_user.battle(user_to_battle)
#     return render_template('battle.html.j2', defender = user_to_battle)