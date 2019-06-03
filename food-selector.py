import os
from app import app, db
from app.models import *

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'NutritionLevel': NutritionLevel, 'UserRoles': UserRoles, 'CoItemType': CoItemType, 'MealTimes': MealTimes, 'User': User, 'CoItem': CoItem, 'FoodItem': FoodItem, 'FoodItemsCoItemSet': FoodItemsCoItemSet, 'ScheduleCoItems': ScheduleCoItems, 'CalendarEntry': CalendarEntry}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 33507))
    app.run(debug=True, port=port, host='0.0.0.0')
