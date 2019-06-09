import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from app.models import *
from app import app, db

def importFoodItems(df):
    concat_items = df['Concat_Items']
    concat_coitems = df['CoItem_Concats']
    for i in df.index:
        db.session.add(eval(concat_items[i]))
        db.session.commit()

def main():
    df = pd.read_excel('Meals.xlsx', sheet_name='Items')
    importFoodItems(df)

if __name__ == "__main__":
    main()