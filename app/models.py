from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import enum

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#enums
class NutritionLevel(enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"

class UserRoles(enum.Enum):
    user = "user"
    admin = "admin"

class CoItemType(enum.Enum):
    shaak = "shaak"
    daal = "daal"
    sweet = "sweet"

class MealTimes(enum.Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"

#tables
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), index=True)
    lastname = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    user_role = db.Column(db.Enum(UserRoles), default=UserRoles.user)

    created = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    last_modified = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    
    #link between User and UserFoodItems tables
    user_food_items = db.relationship('UserFoodItems', backref='user', lazy='dynamic')

    #password hash stuff
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    #print function
    def __repr__(self):
        return "{} {}, {}".format(self.firstname, self.lastname, self.username)

class UserFoodItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    food_items_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), index=True)

    created = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    last_modified = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    #link between UserFoodItems and Schedule tables
    user_food_item_schedule = db.relationship('Schedule', backref='user_food_item', lazy='dynamic')

    def __repr__(self):
        return "{}, {}".format(User.query.filter_by(id=self.user_id).first().firstname, FoodItem.query.filter_by(id=self.food_items_id).first().item)

class CoItem(db.Model):
    __tablename__ = 'co_items'

    id = db.Column(db.Integer, primary_key=True)
    item_type = db.Column(db.Enum(CoItemType))
    name = db.Column(db.String(64), index=True, unique=True)

    created = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    last_modified = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    #link between CoItem and FoodItemCoItemsSet tables
    compatible_foods = db.relationship('FoodItemsCoItemSet', backref='co_items', lazy='dynamic')

    #print function
    def __repr__(self):
        return "{}, {}".format(self.name, self.item_type.value)

class FoodItem(db.Model):
    __tablename__ = 'food_items'

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(128), index=True, unique=True)
    breakfast = db.Column(db.Boolean)
    lunch = db.Column(db.Boolean)
    dinner = db.Column(db.Boolean)
    nutrition = db.Column(db.Enum(NutritionLevel))

    created = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    last_modified = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    #link between FoodItem and FoodItemsCoItemSet tables
    compatible_co_items = db.relationship('FoodItemsCoItemSet', backref='food_items', lazy='dynamic')
    #link between FoodItem and UserFoodItems tables
    users = db.relationship('UserFoodItems', backref='user_food_item_food', lazy='dynamic')

    #print function
    def __repr__(self):
        return "{}".format(self.item)

class FoodItemsCoItemSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), index=True)
    co_item_id = db.Column(db.Integer, db.ForeignKey('co_items.id'), index=True)

    #link between FoodItemsCoItemSet and ScheduleCoItems tables
    all_food_items_co_item_set_ids = db.relationship('ScheduleCoItems', backref='related_food_item_set_id', lazy='dynamic')

    #print function
    def __repr__(self):
        return "<Helper table for food_items and co_items. food_item_id: {}, co_item_id: {}>".format(self.food_item_id, self.co_item_id)

class ScheduleCoItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), index=True)
    food_items_co_item_set_id = db.Column(db.Integer, db.ForeignKey('food_items_co_item_set.id'), index=True)

    #print function
    def __repr__(self):
        return "<Helper table for schedule and food_items_co_item_set. schedule_id: {}, food_items_co_item_set_id: {}>".format(self.schedule_id, self.food_items_co_item_set_id)

class Schedule(db.Model):
    __tablename__ = "schedule"

    id = db.Column(db.Integer, primary_key=True)
    user_food_items_id = db.Column(db.Integer, db.ForeignKey('user_food_items.id'), index=True)
    entry_date = db.Column(db.DateTime, index=True, unique=True, default=datetime.utcnow())
    meal_time = db.Column(db.Enum(MealTimes))

    #link between Schedule and ScheduleCoItems tables
    all_co_items = db.relationship('ScheduleCoItems', backref='co_item_serving_entry', lazy='dynamic')

    #print function
    def __repr__(self):
        return "<\Schedule Entry: \nDate: {}\nMealtime: {}\nUser Food Item ID: {}\n>".format(self.entry_date, self.meal_time.value, self.user_food_items_id)
