# This Python file uses the following encoding: utf-8
import dbInit
import textParser

import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.addExpensesTextBtn.clicked.connect(self.addExpensesTextBtn_click)

    def addExpensesTextBtn_click(self):
        blocks = textParser.text_parser(self.ui.addExpensesTextEdit.toPlainText())
        operations = textParser.blocks_parser(blocks)
        self.ui.addExpensesTextEdit.clear()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()

    sys.exit(app.exec())
