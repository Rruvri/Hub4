import sys
from PyQt6.QtWidgets import (QApplication, QLabel,
                             QWidget, QGridLayout,
                             QFormLayout, QLineEdit,
                             QDialog, QHBoxLayout,
                             QDialogButtonBox, QMainWindow,
                             QStackedLayout, QComboBox,
                             QCalendarWidget, QDateEdit,
                             QDateTimeEdit, QCheckBox,
                             QVBoxLayout, QListWidget, 
                             QPushButton)
from PyQt6.QtCore import (QDate, QDateTime)




#____________________________Save Data_________________________

current_accounts = []

current_cash = 0


#____________________________Classes_________________________


#____________Adjustments____________
class Adjustment:
    def __init__(self, name, amount, date_occured=None):
        self.name = name
        self.amount = int(amount)
        self.date_occured = date_occured

class Spend(Adjustment):
    def __init__(self, name, amount, date_occured=None):
        super().__init__(name, amount, date_occured)

class Gain(Adjustment):
    def __init__(self, name, amount, date_occured=None):
        super().__init__(name, amount, date_occured)

#____________Accounts____________

class Account:
    def __init__(self, name, current_balance=0, sub_accounts=[]):
        self.name = name
        self.current_balance = current_balance
        self.sub_accounts = sub_accounts

class SubAccount(Account):
    def __init__(self, name, current_balance=0):
        super().__init__(name, current_balance)