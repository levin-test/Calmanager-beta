import os
import datetime
from db_manager import *


class Food:
    def __init__(self, name="", cal=0, protein=0, fat=0, carbohydrate=0):
        self.name = name
        self.cal = cal
        self.protein = protein
        self.fat = fat
        self.carbohydrate = carbohydrate
        print("food_init")

    def get_all_nutrition(self):
        return self.protein, self.fat, self.carbohydrate

    def save_food_info(self):
        # TODO: Use "with"
        conn = sqlite3.connect("data/pfc_manageDB.sqlite")
        curs = conn.cursor()

        curs.execute(
            """
            INSERT INTO food(name, cal, protein, fat, carbohydrate) 
            VALUES (?, ?, ?, ?, ?);
            """,
            [self.name, self.cal, self.protein, self.fat, self.carbohydrate],
        )
        conn.commit()
        curs.close()
        conn.close()

    def used_coefficient(self, coefficient):
        self.cal *= coefficient
        self.protein *= coefficient
        self.fat *= coefficient
        self.carbohydrate *= coefficient

    # この関数は基本使用しない。将来的に削除する可能性あり。
    def temp_use_coefficient(self, coefficient):
        result = list(
            map(
                lambda x: x * coefficient,
                [self.cal, self.protein, self.fat, self.carbohydrate],
            )
        )
        return [self.name] + result


class Meals:
    def __init__(self, date=None, food_id=0):
        self.date = date
        self.food_id = food_id
        print("Meals_class_init")
