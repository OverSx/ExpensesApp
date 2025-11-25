# This Python file uses the following encoding: utf-8
import dbInit
import textParser

import sys
sys.setswitchinterval(0.01)

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QScrollArea, QVBoxLayout
from PySide6.QtGui import QPalette
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.layout = QVBoxLayout(self.ui.gridLayoutExpenses)


        self.ui.addExpensesTextBtn.clicked.connect(self.addExpensesTextBtn_click)

    def addExpensesTextBtn_click(self):
        blocks = textParser.text_parser(self.ui.addExpensesTextEdit.toPlainText())
        operations = textParser.blocks_parser(blocks)
        self.ui.addExpensesTextEdit.clear()
        self.expensesToBtn(operations)

    def expensesToBtn(self, operation_list):
        for item in operation_list:
            btn = QPushButton(f"Сумма: {item[0]} {item[1]}, {item[4]}")
            btn.setToolTip(f"Сумма: {item[0]} {item[1]}\nМесто: {item[4]}\nДата: {item[2]}\nВремя: {item[3]}")
            btn.setCheckable(True)
            btn.setFixedSize(320, 22)

            self.layout.addWidget(btn)




if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()

    app.exec()
