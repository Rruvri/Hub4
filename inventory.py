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

current_inventory = {}

all_items = {}


#____________________________Classes_________________________

class Item:
    def __init__(self, name, cat, stock=0):
        self.name = name
        self.cat = cat
        self.stock = stock




