# This Python file uses the following encoding: utf-8
import dbInit
import textParser

import sys
sys.setswitchinterval(0.01)

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QScrollArea, QVBoxLayout
from PySide6.QtWidgets import QMessageBox
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.layout_fix = QVBoxLayout(self.ui.gridLayoutExpenses)
        self.layout_unfix = QVBoxLayout(self.ui.gridLayoutExtraExpenses)


        self.ui.addExpensesTextBtn.clicked.connect(self.addExpensesTextBtn_click)
        self.ui.rightToolSwitchWeek.clicked.connect(self.rightToolSwitchWeek_click)

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

            if item[5] == 0:
                self.layout_unfix.addWidget(btn)
            elif item[5] == 1:
                self.layout_fix.addWidget(btn)
            else:
                QMessageBox(self, "Предупреждение", f"Трата в {item[4]}  на сумму {item[0]} сохранилась неправильно. "
                                                    f"Она не будет учтена")


    def rightToolSwitchWeek_click(self):
        weeks = textParser.year_generator(2025)
        print(weeks)



if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()

    app.exec()
