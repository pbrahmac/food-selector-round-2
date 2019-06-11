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

    edit_modal = True
    create_modal = True

# sub-classes of MyModelView (specific for each table)
class MyUserView(MyModelView):
    column_exclude_list = ['password_hash']
    form_excluded_columns = ['password_hash', 'created', 'last_modified']
    column_searchable_list = ['firstname', 'lastname', 'username']

class MyFoodItemView(MyModelView):
    column_searchable_list = ['item', 'nutrition']
    column_filters = ['breakfast', 'lunch', 'dinner']
    # column_editable_list = ['item', 'breakfast', 'lunch', 'dinner', 'nutrition']

class MyUserFoodItemsView(MyModelView):
    pass

class MyCoItemView(MyModelView):
    column_searchable_list = ['name']
    column_filters = ['item_type']

class MyFoodItemsCoItemSetView(MyModelView):
    pass
class MyScheduleCoItemsView(MyModelView):
    pass

class MyScheduleView(MyModelView):
    pass

admin.add_view(MyUserView(User, db.session))
admin.add_view(MyUserFoodItemsView(UserFoodItems, db.session))
admin.add_view(MyFoodItemView(FoodItem, db.session))
admin.add_view(MyCoItemView(CoItem, db.session))
admin.add_view(MyFoodItemsCoItemSetView(FoodItemsCoItemSet, db.session))
admin.add_view(MyScheduleCoItemsView(ScheduleCoItems, db.session))
admin.add_view(MyScheduleView(Schedule, db.session))