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
from PyQt6.QtCore import (QDate, QDateTime, QAbstractListModel, Qt, QModelIndex)
from PyQt6.QtGui import (QColor, QBrush, QImage)

from calendar_dt import current_date
#import saves
import pickle
import os






#____________________________Classes and Fns____________________________

#moved to gui
def sort_open_tasks():
    task_data["open_tasks"].sort(key=lambda task: (task.priority, task.due_date))
    #nb. you were stuck because you were using sorted, but you needed to sort in place

def date_to_qdate(datetimeobj):
    return QDate(datetimeobj.year, datetimeobj.month, datetimeobj.day)

def complete_task_main(task_index, completion_date):
    if completion_date not in task_data["tasks_archive"].keys():
            task_data["tasks_archive"][completion_date] = []
    
    task_data["tasks_archive"][completion_date].append(task_data["open_tasks"].pop(task_index))




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
        self.priority = -1
        '''
        if completion_date not in task_data["tasks_archive"].keys():
            task_data["tasks_archive"][completion_date] = []
        task_data["tasks_archive"][completion_date].append
        '''
    def add_subtask(self, subtask_title, subtask_cat=None, subtask_priority=0, subtask_due=None):
        new_subtask = Subtask(subtask_title, subtask_cat, subtask_priority, subtask_due)
        self.subtasks.append(new_subtask)
        return self.subtasks.sort(key=lambda subtask: subtask.priority, reverse=True)

    def complete_subtask(self, subtask_index, completion_date):
        if self.subtasks and self.subtasks[subtask_index]:
            self.subtasks[subtask_index].complete_subtask(completion_date)
            return self.subtasks.sort(key=lambda subtask: subtask.priority, reverse=True)


def create_task(title, due_date, subtasks=None, cat=None, priority=0):
    new_task = Task(title.title(), due_date=due_date, subtasks=subtasks, cat=cat, priority=priority)
    task_data["open_tasks"].append(new_task)
    if new_task.cat and new_task.cat not in task_data["cats"]:
        task_data["cats"].append(new_task.cat)

    return sort_open_tasks()



class Subtask:
    def __init__(self, title, cat=None, priority=0, due_date=None):
        self.title = title
        self.cat = cat
        self.priority = priority
        self.due_date = due_date


    def complete_subtask(self, completion_date): 
        self.is_complete = True
        self.completion_date = completion_date
        self.priority = -1


#____________________________Save Data_________________________


SAVE_FILE = 'tasks_save_data.pkl'

def load_data():
    if not os.path.exists(SAVE_FILE):
        return {"open_tasks": [], "cats": [], "tasks_archive":{}}
    with open(SAVE_FILE, "rb") as f:
        return pickle.load(f)
        
    
def save_data():
    save_data = task_data
    print(save_data)
    with open(SAVE_FILE, 'wb') as f:
        pickle.dump(save_data, f)



task_data = load_data()
print(task_data)










#____________________________GUI____________________________

class ActiveTaskModel(QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, *kwargs)

        self.tasks = task_data["open_tasks"]

    def data(self, index, role):
        target = self.tasks[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            return target.title

    def rowCount(self, index=QModelIndex()):
        return len(self.tasks)

    def add(self, task):
        self.tasks.append(task)
        sort_open_tasks()
        return self.layoutChanged.emit()
    
    


class TaskWidget(QWidget):
    def __init__(self):
        super().__init__()

        

        task_layout = QHBoxLayout()
        self.active_tasks_model = ActiveTaskModel()
        



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


        RAVI YOU WERE HERE REJIGGING TO MODEL

        #task list _________________________________
        #self.task_list_view = QListWidget()
        #self.refresh_task_gui()
        self.active_tasks_view = QListView()
        self.active_tasks_view.setModel(self.active_tasks_model)
        self.active_tasks_selection_model = self.active_tasks_view.selectionModel()

        #self.task_list_view.currentItemChanged.connect(self.display_task)
        

        task_layout.addLayout(self.task_entry_form)
        #task_layout.addWidget(self.task_list_view)
        task_layout.addWidget(self.active_tasks_view)

        self.setLayout(task_layout)
        print(task_data["cats"])

    
    def submit_task(self):
        task_title = self.task_entry.text().title()
        task_cat = self.task_cat_entry.currentText().title()
        if task_cat == '':
            task_cat = None
        task_date = self.task_date_entry.date().toPyDate()

        if task_title == '':
            return self.task_entry.setPlaceholderText("Enter task to save!")

        i = self.task_list_view.currentRow()

        if i != 0:
            task_data["open_tasks"][i-1].title = task_title
            task_data["open_tasks"][i-1].cat = task_cat
            task_data["open_tasks"][i-1].due_date = task_date 
            
            
        else:
            if task_title in [task.title for task in task_data["open_tasks"]]:
                self.task_entry.clear()
                return self.task_entry.setPlaceholderText("Task already exists!")
            else:                
                create_task(task_title, task_date, cat=task_cat)
                
                if task_cat and (task_cat not in task_data["cats"]):
                    task_data["cats"].append(task_cat)    
        return self.refresh_task_gui()

    

    def refresh_task_gui(self):
        self.clear_entry_screen()
        self.task_list_view.clear()
        self.task_list_view.addItem("<select for new entry>")
        self.task_list_view.setCurrentRow(0)
        if task_data["open_tasks"]:
            sort_open_tasks() #this is doubled from create task fn, but it's fine 
            
            #print([(task.title, task.priority, task.due_date) for task in open_tasks]) --- debugger
            
            
            self.task_list_view.addItems([task.title for task in task_data["open_tasks"]])
            self.task_cat_entry.addItems(task_data["cats"])
            

    def clear_entry_screen(self):
        self.task_entry.clear()
        self.task_cat_entry.clearEditText()
        self.task_date_entry.setDate(date_to_qdate(current_date))

    def display_task(self):
        self.clear_entry_screen()
        i = self.task_list_view.currentRow()
        
        if i > 0:
            item = task_data['open_tasks'][i-1]
            self.task_entry.setText(item.title)
            if item.cat:
                self.task_cat_entry.setCurrentText(item.cat)
            self.task_date_entry.setDate(date_to_qdate(item.due_date))
            

        

        
             


    def save_all(self):
        return save_data()
        



    
     

    
    
        