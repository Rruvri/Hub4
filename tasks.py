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

from calendar_dt import current_date



#____________________________Save Data_________________________


open_tasks = {}

tasks_archive = {}



#____________________________Classes____________________________

class Task:
    def __init__(self, title, due_date, subtasks=[], cat=None, priority=0):
        self.title = title
        self.due_date = due_date
        self.cat = cat
        self.subtasks = subtasks
        self.priority = priority
        
        self.is_completed = False
    
    def complete_task(self, completion_date):
        self.is_completed = True
        self.completion_date = completion_date
        self.priority = 0

    def add_subtask(self, subtask):
        self.subtasks.append(subtask)
        sorted(self.subtasks, lambda subtask: subtask.priority, reverse=True)





class Subtask(Task):
    def __init__(self, title, due_date, cat=None, priority=0):
        super().__init__(title, due_date, cat, priority)

    
    def add_subtask(self): #this is janky so maybe see if you need  this as a child class
        pass



#____________________________GUI____________________________


#This needs a check as it's come from Hub3

class TaskWidget(QWidget):
    def __init__(self):
        super().__init__()

        task_layout = QHBoxLayout()


        #task entry/creation _________________________________
        self.task_entry_form = QFormLayout()

        self.task_entry = QLineEdit()
        self.task_entry_form.addRow(QLabel("Enter Task"), self.task_entry)

        self.task_cat_entry = QComboBox()
        self.task_cat_entry.setEditable(True)
        self.task_entry_form.addRow(QLabel("Enter Category"), self.task_cat_entry)




        self.task_date_entry = QDateEdit()
        self.task_date_entry.setDate(QDate(current_date.year, current_date.month, current_date.day))
        self.task_entry_form.addRow(QLabel("Enter Due Date"), self.task_date_entry)

        self.submit_task_btn = QPushButton("Submit Task")

        self.submit_task_btn.clicked.connect(self.submit_task)
        self.task_entry_form.addRow(self.submit_task_btn)


        #task list _________________________________
        self.task_list_view = QListWidget()

        task_layout.addLayout(self.task_entry_form)
        task_layout.addWidget(self.task_list_view)

        self.setLayout(task_layout)
    
    
        