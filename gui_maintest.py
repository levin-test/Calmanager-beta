import sys
import os
from PySide2.QtWidgets import *
import main
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QTableWidget


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connected_dbname = ""
        self.statusBar().showMessage("Ready", 5000)
        self.setGeometry(20, 20, 900, 600)

        self.open_act = QAction(
            self.style().standardIcon(QStyle.SP_DialogOpenButton), "Open", self
        )

        self.close_act = QAction(
            self.style().standardIcon(QStyle.SP_DirClosedIcon), "Close", self
        )

        self.save_act = QAction(
            self.style().standardIcon(QStyle.SP_DialogSaveButton), "Save", self
        )

        self.quit_act = QAction("Exit", self)

        menu_bar = self.menuBar()
        menu = menu_bar.addMenu("File")

        # Menuをセットする
        menu.addAction(self.open_act)
        menu.addAction(self.close_act)
        menu.addAction(self.save_act)
        menu.addAction(self.quit_act)

    def change_window_title(self, filename):
        self.connected_dbname = filename
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

        print(filename)


class AllWithEventActions:
    def __init__(self):
        self.root_widget = Example()
        self.root_widget.show()
        self.root_widget.open_act.triggered.connect(self.open)
        self.root_widget.close_act.triggered.connect(self.close)
        self.root_widget.save_act.triggered.connect(self.save)
        self.root_widget.quit_act.triggered.connect(self.quit_app)

    def open(self):
        # print("opened")
        select_file = QFileDialog.getOpenFileName(filter="SQLite Files (*.sqlite)")
        self.root_widget.change_window_title(select_file[0])

    def close(self):
        # print("closed")
        self.root_widget.change_window_title("")

    @classmethod
    def save(cls):
        print("saved")

    @classmethod
    def quit_app(cls):
        sys.exit()
        