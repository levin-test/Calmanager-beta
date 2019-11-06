import sqlite3

conn = sqlite3.connect("data/pfc_manageDB.sqlite")
curs = conn.cursor()

# もし既存のテーブルがあれば削除
curs.execute("DROP TABLE IF EXISTS food;")
# テーブルを作成する
curs.execute(
    """
CREATE TABLE food
(
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         STRING,
    cal          NUMERIC,
    protein      NUMERIC,
    fat          NUMERIC,
    carbohydrate NUMERIC
);
"""
)

curs.execute(
    """
INSERT INTO food(id, name, cal, protein, fat, carbohydrate)
values (1, 'Sample001', 250, 20, 10, 20);
"""
)

conn.commit()
curs.close()
conn.close()
