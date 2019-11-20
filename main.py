import os
import datetime
import sqlite3


class Food:
    def __init__(self, name="", cal=0, protein=0, fat=0, carbohydrate=0):
        self.name = name
        self.cal = cal
        self.protein = protein
        self.fat = fat
        self.carbohydrate = carbohydrate
        # テスト用メッセージ
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


class FoodToday:
    def __init__(self):
        self.food_list = []
        # 今日付けの食事データをすべて取得する
        conn = sqlite3.connect(
            "data/pfc_manageDB.sqlite",
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()

        curs.execute(
            """
            SELECT * FROM meals
            LEFT OUTER JOIN food
            ON meals.food_id = food.id
            WHERE meals.date = ?
            """,
            [datetime.date.today()],
        )
        temp_dict = curs.fetchall()
        for one_row in temp_dict:
            item = Food()
            item.name = one_row["name"]
            item.cal = one_row["cal"]
            item.protein = one_row["protein"]
            item.fat = one_row["fat"]
            item.carbohydrate = one_row["carbohydrate"]
            self.food_list.append(item)

    # この関数は基本使用しない。将来的に削除する可能性あり。
    def show_all(self):
        for i in self.food_list:
            print(i.name, i.cal, i.protein, i.fat, i.carbohydrate)
