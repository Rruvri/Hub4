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
                             QPushButton, QTabWidget,
                             QTextEdit, QListWidgetItem,
                             QListView, QLayoutItem, QLayout)
from PyQt6.QtCore import (QDate, QDateTime, QAbstractListModel, QAbstractItemModel, QAbstractTableModel, Qt, QModelIndex)
from PyQt6.QtGui import (QColor, QBrush, QImage)
from calendar_dt import current_date

import tasks_new


def date_to_qdate(datetimeobj):
    return QDate(datetimeobj.year, datetimeobj.month, datetimeobj.day)




#_________________TASKS_GUI_________________
class ActiveTaskModel(QAbstractListModel):
    def __init__(self, task_data, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.task_data = task_data
        self.tasks = task_data["open_tasks"]

    def data(self, index, role):
        target = self.tasks[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            #space = len(target.title)
            #white_space = " "*(50-space)
            #return f"{target.title}{white_space}| {target.cat}"
            #NOTE: need to add a strf convert to display dates

            return target.title
            #NOTE: this is barebones, decide RE dates displayed etc

    def rowCount(self, index=QModelIndex()):
        return len(self.tasks)

    def add(self, task_obj):
        self.tasks.append(task_obj)
        tasks_new.sort_open_tasks()
        return self.layoutChanged.emit()

    def complete(self):
        pass

    #def __getitem__ WHAT WAS THIS FROM?
    


class TaskWidget(QWidget):
    def __init__(self):
        super().__init__()

        
        task_layout = QHBoxLayout()
        self.active_tasks_model = ActiveTaskModel(task_data=tasks_new.task_data)
        



        #task entry/creation _________________________________
        self.task_entry_form = QFormLayout()

        self.task_entry = QLineEdit()
        self.task_entry_form.addRow(QLabel("Enter Task"), self.task_entry)

        self.task_cat_entry = QComboBox()
        self.task_cat_entry.setEditable(True)
        self.task_entry_form.addRow(QLabel("Enter Category"), self.task_cat_entry)


        self.task_date_entry = QDateEdit()
        self.task_date_entry.setDate(date_to_qdate(current_date))
        self.task_entry_form.addRow(QLabel("Enter Due Date"), self.task_date_entry)

        self.submit_task_btn = QPushButton("Submit Task")

        self.submit_task_btn.clicked.connect(self.submit_task)
        self.task_entry_form.addRow(self.submit_task_btn)

        self.save_tasks_btn = QPushButton("Save All")
        self.save_tasks_btn.clicked.connect(self.save_all)
        self.task_entry_form.addRow(self.save_tasks_btn)


        #RAVI YOU WERE HERE REJIGGING TO MODEL

        #task list _________________________________
        
        self.active_tasks_view = QListView()
        self.active_tasks_view.setModel(self.active_tasks_model)
        self.active_tasks_selection_model = self.active_tasks_view.selectionModel()
        self.active_tasks_selection_model.selectionChanged.connect(self.display_task)
        
        
        

        task_layout.addLayout(self.task_entry_form)
        
        task_layout.addWidget(self.active_tasks_view)

        self.setLayout(task_layout)
        

    
    def submit_task(self):
        task_title = self.task_entry.text().title()
        task_cat = self.task_cat_entry.currentText().title()
        if task_cat == '':
            task_cat = None
        task_date = self.task_date_entry.date().toPyDate()

        if task_title == '':
            return self.task_entry.setPlaceholderText("Enter task to save!")


        
        self.active_tasks_model.add(tasks_new.create_task_obj(task_title, task_date, task_cat))
        self.clear_entry_screen()

    
    
            

    def clear_entry_screen(self):
        self.task_entry.clear()
        self.task_cat_entry.clearEditText()
        self.task_date_entry.setDate(date_to_qdate(current_date))

    def display_task(self):
        self.clear_entry_screen()
        task_obj = self.active_tasks_model.tasks[self.active_tasks_selection_model.currentIndex().row()]
        self.task_entry.setText(task_obj.title)
        if task_obj.cat:
                self.task_cat_entry.setCurrentText(task_obj.cat)
        self.task_date_entry.setDate(date_to_qdate(task_obj.due_date))
        

        
             


    def save_all(self):
        return tasks_new.save_data()
