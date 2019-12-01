import sys
import os
from PySide2.QtWidgets import *
from PySide2 import QtCore


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connected_dbname = ""
        self.statusBar().showMessage("Ready", 5000)
        self.setGeometry(20, 20, 1080, 750)

        # メニューバーにセットするアクションを準備
        self.open_act = QAction(
            self.style().standardIcon(QStyle.SP_DialogOpenButton), "Open", self
        )

        self.close_act = QAction(
            self.style().standardIcon(QStyle.SP_DirClosedIcon), "Close", self
        )

        self.save_act = QAction(
            self.style().standardIcon(QStyle.SP_DialogSaveButton), "Save", self
        )
        self.save_act.setShortcut('Ctrl+S')

        self.quit_act = QAction("Exit", self)

        self.refresh_act = QAction("Refresh", self)
        self.refresh_act.setShortcut('Ctrl+R')

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

        self.tab_widget = Tabtest()
        self.setCentralWidget(self.tab_widget)

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


class Tabtest(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")
        self.tabs.addTab(self.tab3, "Tab test")
        self.tab1.label = QLabel("test")
        self.tab1.hbox = QHBoxLayout()
        self.tab1.hbox.addWidget(self.tab1.label)
        self.tab1.setLayout(self.tab1.hbox)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


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
        print(self.root_widget.tab_widget.tabs.currentIndex())

    def refresh(self):
        self.root_widget.statusBar().showMessage("Refreshed!", 7500)

    @classmethod
    def quit_app(cls):
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = AllWithEventActions()
    app.exec_()
