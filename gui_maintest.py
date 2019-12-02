import sys
import os
from PySide2.QtWidgets import *
import datetime
from PySide2 import QtCore
import sqlite3


class Start:
    def __init__(self):
        self.root_window = Example()
        self.root_window.show()


class EnvInfo:
    __connected_db_path = ""
    @classmethod
    def set_db_path(cls, db_path):
        """
        :param db_path: DB's full path
        :type db_path: str
        :return: None
        """
        cls.__connected_db_path = db_path

    @classmethod
    def get_db_path(cls):
        """
        :return: current db's full path
        :rtype: str
        """
        return cls.__connected_db_path


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.statusBar().showMessage("Ready", 15000)
        self.setGeometry(20, 20, 1080, 750)

        # メニューバーにセットするアクションを準備
        self.open_act = QAction(
            self.style().standardIcon(QStyle.SP_DialogOpenButton), "Open", self
        )
        self.open_act.setShortcut("Ctrl+O")

        self.open_recent_act = QAction(
            self.style().standardIcon(QStyle.SP_DialogOpenButton), "Open Recent", self
        )
        self.open_recent_act.setShortcut("Ctrl+O")

        self.close_act = QAction(
            self.style().standardIcon(QStyle.SP_DirClosedIcon), "Close", self
        )
        self.close_act.setShortcut("Ctrl+W")

        self.save_act = QAction(
            self.style().standardIcon(QStyle.SP_DialogSaveButton), "Save", self
        )
        self.save_act.setShortcut("Ctrl+S")

        self.quit_act = QAction("Exit", self)
        self.quit_act.setShortcut("Ctrl+Q")

        self.refresh_act = QAction("Refresh", self)
        self.refresh_act.setShortcut("Ctrl+R")

        # メニューバーを設定する
        self.menu_bar = self.menuBar()
        self.menu_file = self.menu_bar.addMenu("File")
        self.menu_action = self.menu_bar.addMenu("Action")

        # Menuをセットする
        self.menu_file.addAction(self.open_act)
        self.open_act.triggered.connect(self.open)

        self.menu_file.addAction(self.close_act)
        self.close_act.triggered.connect(self.close)

        self.menu_file.addAction(self.save_act)
        self.save_act.triggered.connect(self.save)

        self.menu_file.addAction(self.quit_act)
        self.quit_act.triggered.connect(self.quit)

        self.menu_action.addAction(self.refresh_act)
        self.refresh_act.triggered.connect(self.refresh)

        # タブを準備
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(TabAddData(), "AddData")
        self.tab_widget.setTabEnabled(0, False)
        self.setCentralWidget(self.tab_widget)


    def change_window_title(self, file_path):
        EnvInfo.set_db_path(file_path)
        db_name = os.path.basename(file_path)
        if db_name != "":
            db_name = "(" + db_name + ")"
            self.setWindowTitle("rabit{}".format(db_name))
            message = "Opened {} successfully!".format(os.path.basename(db_name))
            self.statusBar().showMessage(message, 15000)
        else:
            self.setWindowTitle("rabit{}".format(db_name))
            message = "Disconnected!"
            self.statusBar().showMessage(message, 15000)

    def open(self):
        select_file = QFileDialog.getOpenFileName(filter="SQLite Files (*.sqlite)")
        self.change_window_title(select_file[0])
        self.tab_widget.setTabEnabled(0, True)

    def close(self):
        self.change_window_title("")
        a = self.tab_widget.findChild(TabAddData)
        a.clear_content()
        self.tab_widget.setTabEnabled(0, False)

    def save(self):
        print(self.currentIndex())

    def refresh(self):
        self.statusBar().showMessage("Refreshed!", 10000)

    @staticmethod
    def quit():
        sys.exit()


class Tabtest(QWidget):
    def __init__(self):
        super().__init__()
        self.lbl_tab1 = QLabel(str(datetime.datetime.now()))

        self.btn_refresh = QPushButton("Now")
        self.btn_refresh.move(50, 50)
        self.btn_refresh.clicked.connect(self.refresher)

        vertical_box = QVBoxLayout()
        vertical_box.addWidget(self.lbl_tab1)
        vertical_box.addWidget(self.btn_refresh)

        self.setLayout(vertical_box)

    def refresher(self):
        str_date = datetime.datetime.now()
        str_date = str(str_date)
        self.lbl_tab1.setText(str_date)


class TabAddData(QWidget):
    def __init__(self):
        super().__init__()
        self.label_a = QLabel("Name")
        self.label_b = QLabel("kcal")
        self.label_c = QLabel("protein")
        self.label_d = QLabel("fat")
        self.label_e = QLabel("carbo")
        self.edit_a = QLineEdit()
        self.edit_b = QLineEdit()
        self.edit_c = QLineEdit()
        self.edit_d = QLineEdit()
        self.edit_e = QLineEdit()
        format_layout = QFormLayout()
        format_layout.addRow(self.label_a, self.edit_a)
        format_layout.addRow(self.label_b, self.edit_b)
        format_layout.addRow(self.label_c, self.edit_c)
        format_layout.addRow(self.label_d, self.edit_d)
        format_layout.addRow(self.label_e, self.edit_e)

        btn_register = QPushButton("Register")
        btn_register.clicked.connect(self.register)
        btn_register.setMaximumSize(100, 50)

        btn_clear = QPushButton("Clear")
        btn_clear.clicked.connect(self.clear_content)

        vertical_box = QVBoxLayout()
        vertical_box.addWidget(btn_register, alignment=QtCore.Qt.AlignRight)

        root = QVBoxLayout()
        root.addLayout(format_layout)
        root.addLayout(vertical_box)
        self.setLayout(root)

    def register(self):
        input_name = self.edit_a.text()
        input_cal = int(self.edit_b.text())
        input_pro = int(self.edit_c.text())
        input_fat = int(self.edit_d.text())
        input_carbo = int(self.edit_e.text())
        food = Food(input_name, input_cal, input_pro, input_fat, input_carbo)
        food.save_food_info(EnvInfo.get_db_path())
        self.clear_content()

    def clear_content(self):
        self.edit_a.setText(None)
        self.edit_b.setText(None)
        self.edit_c.setText(None)
        self.edit_d.setText(None)
        self.edit_e.setText(None)


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
        """
        :param curr_db_path: target db path
        :type curr_db_path: str
        :return: None
        """
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
        # 今日の食事を格納するためのリストを準備
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
        """
        :return: None
        """
        for i in self.food_list:
            print(i.name, i.cal, i.protein, i.fat, i.carbohydrate)


class Meals:
    def __init__(self, date=None, food_id=0):
        self.date = date
        self.food_id = food_id


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Start()
    app.exec_()
