import os
from app import app, db
from app.models import *

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'NutritionLevel': NutritionLevel, 'UserRoles': UserRoles, 'CoItemType': CoItemType, 'MealTimes': MealTimes, 'User': User, 'CoItem': CoItem, 'FoodItem': FoodItem, 'FoodItemsCoItemSet': FoodItemsCoItemSet, 'ScheduleCoItems': ScheduleCoItems, 'Schedule': Schedule, 'UserFoodItems': UserFoodItems}

if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 33507))
    app.run(debug=False, port=port, host=host)
