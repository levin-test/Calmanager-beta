import sqlite3
from datetime import *

conn = sqlite3.connect(
    "data/pfc_manageDB.sqlite",
    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
)

curs = conn.cursor()

# もし既存のテーブルがあれば削除
curs.execute("DROP TABLE IF EXISTS food;")
curs.execute("DROP TABLE IF EXISTS meals;")

# テーブルを作成する
curs.execute(
    """
    CREATE TABLE food
    (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        name         TEXT,
        cal          NUMERIC,
        protein      NUMERIC,
        fat          NUMERIC,
        carbohydrate NUMERIC
    );
    """
)

curs.execute(
    """
    CREATE TABLE meals
    (
        date         DATE,
        food_id      INTEGER,
        PRIMARY KEY (date, food_id)
    );
    """
)


# サンプルデータを一つ登録する
curs.execute(
    """
    INSERT INTO food(name, cal, protein, fat, carbohydrate)
    values ('Sample001', 250, 20, 10, 20);
    """
)

curs.execute(
    """
    INSERT INTO meals(date, food_id)
    VALUES (?, 1);
    """,
    [date.today()],
)

conn.commit()
curs.close()
conn.close()
