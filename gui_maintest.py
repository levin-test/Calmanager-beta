import sys
import os
from PySide2.QtWidgets import *
import datetime
from PySide2 import QtCore
import sqlite3


class Example(QMainWindow):
    connected_dbname = ""
    def __init__(self):
        super().__init__()
        # self.connected_dbname = ""
        self.statusBar().showMessage("Ready", 5000)
        self.setGeometry(20, 20, 1080, 750)

        # メニューバーにセットするアクションを準備
        self.open_act = QAction(
            self.style().standardIcon(QStyle.SP_DialogOpenButton), "Open", self
        )
        self.open_act.setShortcut("Ctrl+O")

        self.close_act = QAction(
            self.style().standardIcon(QStyle.SP_DirClosedIcon), "Close", self
        )
        self.close_act.setShortcut("Ctrl+W")

        self.save_act = QAction(
            self.style().standardIcon(QStyle.SP_DialogSaveButton), "Save", self
        )
        self.save_act.setShortcut("Ctrl+S")

        self.quit_act = QAction("Exit", self)

        self.refresh_act = QAction("Refresh", self)
        self.refresh_act.setShortcut("Ctrl+R")

        # メニューバーを設定する
        self.menu_bar = self.menuBar()
        self.menu_file = self.menu_bar.addMenu("File")
        self.menu_action = self.menu_bar.addMenu("Action")

        # Menuをセットする
        self.menu_file.addAction(self.open_act)
        self.menu_file.addAction(self.close_act)
        self.menu_file.addAction(self.save_act)
        self.menu_file.addAction(self.quit_act)

        self.menu_action.addAction(self.refresh_act)

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(Tabtest(), "tabtest")
        self.tab_widget.addTab(TabAddData(), "AddData")
        self.setCentralWidget(self.tab_widget)

    def change_window_title(self, filename):
        Example.connected_dbname = filename
        filename = os.path.basename(filename)
        if filename != "":
            filename = "(" + filename + ")"
            self.setWindowTitle("rabit{}".format(filename))
            message = "Opened {} successfully!".format(os.path.basename(filename))
            self.statusBar().showMessage(message, 5000)
        else:
            self.setWindowTitle("rabit{}".format(filename))
            message = "Disconnected!"
            self.statusBar().showMessage(message, 5000)

    @classmethod
    def db_path(cls):
        return Example.connected_dbname

class Tabtest(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.lbl_tab1 = QLabel(str(datetime.datetime.now()))
        self.btn_refresh = QPushButton("Now")
        self.btn_refresh.move(50,50)
        self.btn_refresh.clicked.connect(self.refresher)
        horizon_box = QHBoxLayout()
        vertical_box = QVBoxLayout()
        vertical_box.addWidget(self.lbl_tab1)
        vertical_box.addWidget(self.btn_refresh)
        self.setLayout(vertical_box)

    def refresher(self):
        strdate = datetime.datetime.now()
        strdate = str(strdate)
        self.lbl_tab1.setText(strdate)

        # self.update()


class TabAddData(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        label_a = QLabel("Name")
        label_b = QLabel("kcal")
        label_c = QLabel("protein")
        label_d = QLabel("fat")
        label_e = QLabel("carbo")
        self.edit_a = QLineEdit()
        self.edit_b = QLineEdit()
        self.edit_c = QLineEdit()
        self.edit_d = QLineEdit()
        self.edit_e = QLineEdit()
        format_layout = QFormLayout()
        format_layout.addRow(label_a, self.edit_a)
        format_layout.addRow(label_b, self.edit_b)
        format_layout.addRow(label_c, self.edit_c)
        format_layout.addRow(label_d, self.edit_d)
        format_layout.addRow(label_e, self.edit_e)

        btn_register = QPushButton("Register")
        btn_register.clicked.connect(self.touroku)
        btn_register.setMaximumSize(100, 50)
        vertical_box = QVBoxLayout()
        vertical_box.addWidget(btn_register, alignment=QtCore.Qt.AlignRight)
        root = QVBoxLayout()
        root.addLayout(format_layout)
        root.addLayout(vertical_box)
        self.setLayout(root)

    def touroku(self):
        input_name = self.edit_a.text()
        input_cal = int(self.edit_b.text())
        input_pro = int(self.edit_c.text())
        input_fat = int(self.edit_d.text())
        input_carbo = int(self.edit_e.text())
        food = Food(input_name, input_cal, input_pro, input_fat, input_carbo)
        # food.save_food_info('data/pfc_manageDB.sqlite')
        food.save_food_info(Example.connected_dbname)
        self.clear_content()

    def clear_content(self):
        self.edit_a.setText(None)
        self.edit_b.setText(None)
        self.edit_c.setText(None)
        self.edit_d.setText(None)
        self.edit_e.setText(None)




class AllWithEventActions:
    def __init__(self):
        self.root_widget = Example()
        self.root_widget.show()
        self.root_widget.open_act.triggered.connect(self.open)
        self.root_widget.close_act.triggered.connect(self.close)
        self.root_widget.save_act.triggered.connect(self.save)
        self.root_widget.refresh_act.triggered.connect(self.refresh)
        self.root_widget.quit_act.triggered.connect(self.quit_app)

    def open(self):
        select_file = QFileDialog.getOpenFileName(filter="SQLite Files (*.sqlite)")
        self.root_widget.change_window_title(select_file[0])

    def close(self):
        # print("closed")
        self.root_widget.change_window_title("")

    def save(self):
        print("saved")
        print(self.root_widget.tab_widget.currentIndex())

    def refresh(self):
        # self.root_widget.tab_widget.refresher()
        self.root_widget.tab_widget.init_ui()
        self.root_widget.statusBar().showMessage("Refreshed!", 7500)

    def get_db_path(self):
        return self.root_widget.connected_dbname

    @classmethod
    def quit_app(cls):
        sys.exit()

# def set_db(db_name):
#     global curr_db_path
#     curr_path = os.getcwd()
#     curr_db_path = os.path.join(curr_path, "data", db_name)


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

    def save_food_info(self, curr_db_path):
        # TODO: Use "with"
        conn = sqlite3.connect(curr_db_path)
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
        curs.close()
        conn.close()

    # この関数は基本使用しない。将来的に削除する可能性あり。
    def show_all(self):
        for i in self.food_list:
            print(i.name, i.cal, i.protein, i.fat, i.carbohydrate)


class Meals:
    def __init__(self, date=None, food_id=0):
        self.date = date
        self.food_id = food_id
        print("Meals_class_init")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = AllWithEventActions()
    app.exec_()
