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
        self.ui.addExpensesToDBBtn.clicked.connect(self.addExpensesToDBBtn_click)
        self.ui.addExpensesToColumns.clicked.connect(self.addExpensesToColumns_click)
        self.ui.calcDebtBtn.clicked.connect(self.calcDebtBtn_click)

        current_date = datetime.now()

        #dbWeeksCreating
        if not textParser.last_date_req():
            textParser.year_generator(current_date.year)

        #currentWeekLabel
        w_cur, y_cur, dates_cur = textParser.get_full_week(current_date)
        self.ui.chosenWeekLbl.setText(f"{y_cur} - {w_cur} ({dates_cur})")

        #currentDayLabel
        self.ui.dateLabel.setText(f"{current_date.date().strftime("%A")} {str(current_date.date())}")

        #currentMonthlabel
        first_date_of_month, last_date_of_month = textParser.get_month_dates(y_cur, w_cur)
        self.ui.monthDatesLabel.setText(f"{first_date_of_month} - {last_date_of_month}")

        #todaysCurrencylabels
        self.ui.GEL_value_label.setText(str(round(textParser.get_rate('EUR', 'GEL'), 4)))
        self.ui.USD_value_label.setText(str(round(textParser.get_rate('EUR', 'USD'), 4)))
        self.ui.RUB_value_label.setText(str(round(textParser.get_rate('EUR', 'RUB'), 4)))

        #currentWeekExpensesLabel
        self.updateCurrentExpensesLbls()

        #currentDebtandRent
        rent_list = textParser.update_monthly_rent()
        self.ui.monthlyRentNum.setText(str(rent_list[0]))
        self.ui.monthlyRentCurrencyComboBox.setCurrentIndex(rent_list[1])
        self.ui.remainDebtNum.setText(f"{str(rent_list[2])}")

    def updateCurrentExpensesLbls(self):
        #currentWeekExpensesLabel
        current_info_week_year = self.ui.chosenWeekLbl.text().split()
        p = textParser.get_expense_amount(current_info_week_year[0], current_info_week_year[2], 1)
        self.ui.paidOutThisWeekNum.setText(f"{str(round(p, 2))} €")

        #RemainBalanceLabel
        exp = self.ui.paidOutThisWeekNum.text().split()
        self.ui.remainedThisWeekNum.setText(f"{round(150 - float(exp[0]), 2)} €")

        #UnfixExpensesLabel
        p = textParser.get_expense_amount(current_info_week_year[0], current_info_week_year[2], 0)
        self.ui.unfixExpensesThisWeekNum.setText(f"{str(round(p, 2))} €")

        #LizaExpensesLabel
        p = textParser.get_expense_amount(current_info_week_year[0], current_info_week_year[2], 2)
        self.ui.lizaExpensesThisWeekNum.setText(f"{str(round(p, 2))} €")

        #MonthExpensesLabel
        unfix_sum, fix_sum, liza_sum = textParser.get_month_expenses(current_info_week_year[0], current_info_week_year[2])
        self.ui.ExpensesThisMonthNum.setText(f"Учетные траты: {round(fix_sum, 2)} €\n"
                                             f"Внеучетные траты: {round(unfix_sum, 2)} €\n"
                                             f"Траты Лизочки: {round(liza_sum, 2)} €")

        self.ui.ExpensesThisMonthNumOverall.setText(f"{round(fix_sum, 2)} + {round(unfix_sum, 2)} = {round(fix_sum + unfix_sum, 2)} €")



    def addExpensesTextBtn_click(self):
        blocks = textParser.text_parser(self.ui.addExpensesTextEdit.toPlainText())
        operations = textParser.blocks_parser(blocks)
        self.ui.addExpensesTextEdit.clear()
        self.expensesToBtn(operations)

    def expensesToBtn(self, operation_list):
        for item in operation_list:
            if item[1] == 'GEL':
                eur_amount = float(item[0]) / float(self.ui.GEL_value_label.text())
            elif item[1] == 'USD':
                eur_amount = float(item[0]) / float(self.ui.USD_value_label.text())
            elif item[1] == 'RUB':
                eur_amount = float(item[0]) / float(self.ui.RUB_value_label.text())

            year, week = textParser.expense_distributor(item[2])

            if year == 0 or week == 0:
                QMessageBox.critical(None, "Ошибка", "Неправильная дата. Такой траты быть не могло, либо мы не вносим"
                                                     " доисторические траты")
                continue

            btn = QPushButton(f"Сумма: {item[0]} {item[1]}, {item[4]}")
            btn.setToolTip(f"Год: {year}\nНеделя: {week}\nСумма: {item[0]}\nВалюта: {item[1]}\nEUR: {str(round(eur_amount, 2))}\n"
                           f"Дата: {item[2]}\nВремя: {item[3]}\nМесто: {item[4]}")
            btn.setCheckable(True)
            btn.setFixedSize(320, 22)

            if item[5] == 0:
                self.layout_unfix.addWidget(btn)
            elif item[5] == 1:
                self.layout_fix.addWidget(btn)
            else:
                QMessageBox.warning(self, "Предупреждение", f"Трата в {item[4]}  на сумму {item[0]} сохранилась неправильно. "
                                                    f"Она не будет учтена.")


    def rightToolSwitchWeek_click(self):
        QMessageBox.warning(self, "Предупреждение", "Gay")

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


    def addExpensesToDBBtn_click(self):
        dialog = AddExpenseDialog(self, self.ui.GEL_value_label.text(), self.ui.USD_value_label.text(), self.ui.RUB_value_label.text())

        dialog.dataOut.connect(self.expensesToBtn)
        dialog.triggerUpdate.connect(self.updateCurrentExpensesLbls)
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

        #RefreshCurrentExpenseSum
        self.updateCurrentExpensesLbls()

    def calcDebtBtn_click(self):
        p = self.ui.ExpensesThisMonthNumOverall.text().split()
        r = self.ui.ExpensesThisMonthNum.text().split()
        was = float(self.ui.remainDebtNum.text())
        new_debt = was - float(p[4])/2 - float(r[10])
        self.ui.remainDebtNum.setText(str(round(new_debt, 2)))

    def save_useful_data(self):
        textParser.save_monthly_rent_to_DB(self.ui.monthlyRentNum.text(), self.ui.monthlyRentCurrencyComboBox.currentText(),
                                           self.ui.remainDebtNum.text())

    def closeEvent(self, event):
        self.save_useful_data()
        event.accept()

class AddExpenseDialog(QDialog):
    dataOut = Signal(list)
    triggerUpdate = Signal()

    def __init__(self, parent=None, gel="", usd="", rub=""):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.gel_rate = gel
        self.usd_rate = usd
        self.rub_rate = rub

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
        if currency == 'GEL':
            eur_amount = float(sum) / float(self.gel_rate)
        elif currency == 'USD':
            eur_amount = float(sum) / float(self.usd_rate)
        elif currency == 'RUB':
            eur_amount = float(sum) / float(self.rub_rate)
        else:
            eur_amount = float(sum)
        date = self.ui.dateEdit.date().toPython().strftime("%d/%m/%Y")
        place = self.ui.lineEditPlace.text()
        if not place:
            place = "Неизвестно"


        if self.ui.checkBoxLiza.isChecked():
            year, week = textParser.expense_distributor(date)
            operation.append([year, week, sum, currency, eur_amount, date, None, place, 2])

            textParser.add_expense(operation)

            self.triggerUpdate.emit()

            self.accept()

        else:
            if self.ui.checkBox.isChecked():
                operation.append([sum, currency, date, None, place, 0])
                self.dataOut.emit(operation)

                self.accept()
            else:
                operation.append([sum, currency, date, None, place, 1])
                self.dataOut.emit(operation)

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
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()
