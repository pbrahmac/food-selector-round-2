from app import app
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from app.models import *

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.user_role.value == 'admin':
            return True
        else:
            return False


admin = Admin(app, index_view=MyAdminIndexView())

class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.user_role.value == 'admin':
            return True
        else:
            return False

class MyUserView(MyModelView):
    column_exclude_list = ['password_hash']
    column_searchable_list = ['firstname', 'lastname', 'username']
    edit_modal = True

class MyFoodItemView(MyModelView):
    column_searchable_list = ['item']

admin.add_view(MyUserView(User, db.session))
admin.add_view(MyFoodItemView(FoodItem, db.session))
