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

current_account_balances = {}

current_cash = 0