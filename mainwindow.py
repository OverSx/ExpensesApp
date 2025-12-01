# This Python file uses the following encoding: utf-8
import dbInit
import textParser

import sys
sys.setswitchinterval(0.01)

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QScrollArea, QVBoxLayout
from PySide6.QtWidgets import QMessageBox, QDialog, QLineEdit
from PySide6.QtCore import QDate, Signal
from PySide6.QtGui import QDoubleValidator
from ui_form import Ui_MainWindow
from ui_dialog import Ui_Dialog
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #scrollAreas
        self.layout_fix = QVBoxLayout(self.ui.gridLayoutExpenses)
        self.layout_unfix = QVBoxLayout(self.ui.gridLayoutExtraExpenses)

        #buttons
        self.ui.addExpensesTextBtn.clicked.connect(self.addExpensesTextBtn_click)
        self.ui.rightToolSwitchWeek.clicked.connect(self.rightToolSwitchWeek_click)
        self.ui.rightToolButton.clicked.connect(self.rightToolButton_click)
        self.ui.leftToolButton.clicked.connect(self.leftToolButton_click)
        self.ui.removeExpensesBtn.clicked.connect(self.removeExpensesBtn_click)
        self.ui.addExpensesFileBtn.clicked.connect(self.addExpensesFileBtn_click)
        self.ui.addExpensesToDBBtn.clicked.connect(self.addExpensesToDBBtn_click)
        self.ui.addExpensesToColumns.clicked.connect(self.addExpensesToColumns_click)

        #currentWeekLabel
        current_date = datetime.now()
        w_cur, y_cur, dates_cur = textParser.get_full_week(current_date)
        self.ui.chosenWeekLbl.setText(f"{y_cur} - {w_cur} ({dates_cur})")

        #currentDayLabel
        self.ui.dateLabel.setText(f"{current_date.date().strftime("%A")} {str(current_date.date())}")

        #todaysCurrencylabels
        self.ui.EUR_value_label.setText(str(textParser.get_rate('GEL', 'EUR')))
        self.ui.USD_value_label.setText(str(textParser.get_rate('GEL', 'USD')))
        self.ui.RUB_value_label.setText(str(textParser.get_rate('GEL', 'RUB')))

        #currentWeekExpensesLabel
        current_info_week_year = self.ui.chosenWeekLbl.text().split()
        p = textParser.get_expense_amount(current_info_week_year[0], current_info_week_year[2], 1, self.ui.EUR_value_label.text(),
                                          self.ui.USD_value_label.text(), self.ui.RUB_value_label.text())
        self.ui.paidOutThisWeekNum.setText(f" {str(p)}")



    def addExpensesTextBtn_click(self):
        blocks = textParser.text_parser(self.ui.addExpensesTextEdit.toPlainText())
        operations = textParser.blocks_parser(blocks)
        self.ui.addExpensesTextEdit.clear()
        self.expensesToBtn(operations)

    def expensesToBtn(self, operation_list):
        for item in operation_list:
            year, week = textParser.expense_distributor(item[2])
            btn = QPushButton(f"Сумма: {item[0]} {item[1]}, {item[4]}")
            btn.setToolTip(f"Год: {year}\nНеделя: {week}\nСумма: {item[0]}\nВалюта: {item[1]}\nДата: {item[2]}\nВремя: {item[3]}\nМесто: {item[4]}")
            btn.setCheckable(True)
            btn.setFixedSize(320, 22)

            if item[5] == 0:
                self.layout_unfix.addWidget(btn)
            elif item[5] == 1:
                self.layout_fix.addWidget(btn)
            else:
                QMessageBox(self, "Предупреждение", f"Трата в {item[4]}  на сумму {item[0]} сохранилась неправильно. "
                                                    f"Она не будет учтена.")


    def rightToolSwitchWeek_click(self):
        QMessageBox(self, "", "Gay")

    def rightToolButton_click(self):
        widgets = []

        for i in range(self.layout_fix.count()):
            item = self.layout_fix.itemAt(i)
            widget = item.widget()
            if widget is not None:
                widgets.append(widget)

        for widget in widgets:
            if hasattr(widget, "isChecked") and widget.isChecked():
                widget.setChecked(False)
                self.layout_fix.removeWidget(widget)
                self.layout_unfix.addWidget(widget)

    def leftToolButton_click(self):
        widgets = []

        for i in range(self.layout_unfix.count()):
            item = self.layout_unfix.itemAt(i)
            widget = item.widget()
            if widget is not None:
                widgets.append(widget)

        for widget in widgets:
            if hasattr(widget, "isChecked") and widget.isChecked():
                widget.setChecked(False)
                self.layout_unfix.removeWidget(widget)
                self.layout_fix.addWidget(widget)

    def removeExpensesBtn_click(self):
        widgets = []

        for i in range(self.layout_unfix.count()):
            item = self.layout_unfix.itemAt(i)
            widget = item.widget()
            if widget is not None:
                widgets.append(widget)

        for i in range(self.layout_fix.count()):
            item = self.layout_fix.itemAt(i)
            widget = item.widget()
            if widget is not None:
                widgets.append(widget)

        for widget in widgets:
            if hasattr(widget, "isChecked") and widget.isChecked():
                self.layout_fix.removeWidget(widget)
                self.layout_unfix.removeWidget(widget)
                widget.setParent(None)


    def addExpensesFileBtn_click(self):
        textParser.year_generator(2025)

    def addExpensesToDBBtn_click(self):
        dialog = AddExpenseDialog(self)

        dialog.dataEntered.connect(self.expensesToBtn)
        dialog.exec()

    def addExpensesToColumns_click(self):
        widgets = []
        operations = []

        for i in range(self.layout_unfix.count()):
            item = self.layout_unfix.itemAt(i)
            widget = item.widget()
            if widget is not None:
                widgets.append(widget)

        for widget in widgets:
            operation = []

            toolTip_text = widget.toolTip().splitlines()
            for line in toolTip_text:
                l = line.split()
                if l[0] == "Место:":
                    place = " ".join(l[1:])
                    operation.append(place)
                else:
                    operation.append(l[1])

            operation.append(0)
            operations.append(operation)
            self.layout_unfix.removeWidget(widget)
            widget.setParent(None)

        widgets = []

        for i in range(self.layout_fix.count()):
            item = self.layout_fix.itemAt(i)
            widget = item.widget()
            if widget is not None:
                widgets.append(widget)

        for widget in widgets:
            operation = []

            toolTip_text = widget.toolTip().splitlines()
            for line in toolTip_text:
                l = line.split()
                if l[0] == "Место:":
                    place = " ".join(l[1:])
                    operation.append(place)
                else:
                    operation.append(l[1])

            operation.append(1)
            operations.append(operation)
            self.layout_fix.removeWidget(widget)
            widget.setParent(None)

        textParser.add_expense(operations)

class AddExpenseDialog(QDialog):
    dataEntered = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        #element settings
        self.ui.dateEdit.setDate(QDate.currentDate())
        self.ui.lineEditAmount.setPlaceholderText("Обязательное поле")
        self.ui.lineEditAmount.setStyleSheet("border: 1px solid red;")
        self.ui.lineEditAmount.textChanged.connect(self.validate_amount)
        self.ui.lineEditAmount.setValidator(QDoubleValidator(0.0, 9999999.99, 2))
        self.ui.pushButtonAdd.setEnabled(False)

        #buttons
        self.ui.pushButtonCancel.clicked.connect(self.close)
        self.ui.pushButtonAdd.clicked.connect(self.pushButtonAdd_click)


    def pushButtonAdd_click(self):
        operation = []

        sum = self.ui.lineEditAmount.text()
        currency = self.ui.comboBox.currentText()
        date = self.ui.dateEdit.date().toPython().strftime("%d/%m/%Y")
        place = self.ui.lineEditPlace.text()
        if not place:
            place = "Неизвестно"


        if self.ui.checkBoxLiza.isChecked():
            year, week = textParser.expense_distributor(date)
            operation.append([year, week, sum, currency, date, None, place, 2])

            textParser.add_expense(operation)

            self.accept()

        else:
            if self.ui.checkBox.isChecked():
                operation.append([sum, currency, date, None, place, 0])
                self.dataEntered.emit(operation)

                self.accept()
            else:
                operation.append([sum, currency, date, None, place, 1])
                self.dataEntered.emit(operation)

                self.accept()


    def validate_amount(self):
        text = self.ui.lineEditAmount.text()

        if not text:
            self.ui.lineEditAmount.setStyleSheet("border: 1px solid red;")
            self.ui.pushButtonAdd.setEnabled(False)
        else:
            self.ui.lineEditAmount.setStyleSheet("")
            self.ui.pushButtonAdd.setEnabled(True)


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()

    app.exec()
