from flask import render_template, flash, redirect, url_for, request, abort, jsonify
from app import app, db
from app.forms import *
from wtforms import ValidationError
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import or_
from werkzeug.urls import url_parse
from app.models import *
import json

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = TestFoodItemDynamicForm()
    form.foods.choices = [(foods.id, foods.item) for foods in FoodItem.query.filter_by(nutrition=NutritionLevel.high).all()]
    render_item = ''
    if request.method == 'POST':
        food = FoodItem.query.filter_by(id=form.foods.data).first()
        render_item = 'Nutrition Level: {}, Food Chosen: {}'.format(form.nutrition.data, food.item)
        return render_template('index.html', title="Home", form=form, render_item=render_item)
    
    return render_template('index.html', title="Home", form=form, render_item=render_item)

@app.route('/foods/<nutrition>')
def foods(nutrition):
    foods = FoodItem.query.filter_by(nutrition=nutrition).all()
    foodArray = []

    for food in foods:
        foodObj = {}
        foodObj['id'] = food.id
        foodObj['item'] = food.item
        foodArray.append(foodObj)

    return jsonify({'foods' : foodArray})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user.check_password(form.password.data):
            flash("Incorrect password.", category="error")
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(firstname=form.firstname.data, lastname=form.lastname.data, username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Nice! You're registered.", category="info")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if not current_user.username == user.username:
        abort(403)
    users = User.query
    form = UserSearchForm()
    if form.validate():
        users = users.filter(
            or_(
                (User.username.like('%' + form.searchBox.data + '%')),
                (User.firstname.like('%' + form.searchBox.data + '%')),
                (User.lastname.like('%' + form.searchBox.data + '%'))))

    users = users.order_by(User.id).all()
    return render_template('user.html', user=user, users=users, form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    deleteForm = DeleteAccountForm()
    if form.validate_on_submit():
        if form.username.data != '':
            current_user.username = form.username.data
        
        if form.password.data != '':
            current_user.set_password(form.password.data)

        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        db.session.commit()
        flash('Your changes have been saved.', category="info")
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
    
    if deleteForm.validate_on_submit():
        db.session.delete(current_user)
        db.session.commit()
        flash('Your account has been deleted. We\'re sad to see you go!', category="warning")
        return redirect(url_for('login'))

    return render_template('edit_profile.html', title='Edit Profile', form=form, deleteForm=deleteForm)

@app.route('/my_foods')
@login_required
def my_foods():
    return render_template('my_foods.html', title='My Foods')