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


open_tasks = {}

tasks_archive = {}



#____________________________Classes_________________________

class Task:
    def __init__(self, title, due_date, subtasks=[], cat=None):
        self.title = title
        self.due_date = due_date
        self.cat = cat
        self.subtasks = subtasks
        

        self.is_completed = False


class Subtask(Task):
    def __init__(self, title, due_date, cat=None):
        super().__init__(title, due_date, cat)




        