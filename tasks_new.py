import sys


from calendar_dt import current_date
#import saves
import pickle
import os






#____________________________Classes and Fns____________________________

#moved to gui
def sort_open_tasks():
    task_data["open_tasks"].sort(key=lambda task: (task.priority, task.due_date))
    #nb. you were stuck because you were using sorted, but you needed to sort in place

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

    def add_subtask(self, subtask_title, subtask_cat=None, subtask_priority=0, subtask_due=None):
        new_subtask = Subtask(subtask_title, subtask_cat, subtask_priority, subtask_due)
        self.subtasks.append(new_subtask)
        return self.subtasks.sort(key=lambda subtask: subtask.priority, reverse=True)

    def complete_subtask(self, subtask_index, completion_date):
        if self.subtasks and self.subtasks[subtask_index]:
            self.subtasks[subtask_index].complete_subtask(completion_date)
            return self.subtasks.sort(key=lambda subtask: subtask.priority, reverse=True)


def create_task_obj(title, due_date, cat=None, subtasks=None, priority=0):
    new_task = Task(title.title(), due_date=due_date, subtasks=subtasks, cat=cat, priority=priority)
    return new_task

    #NOTE: Moved to model add fn
    #task_data["open_tasks"].append(new_task)

    #NOTE:you need to scrap this as you should use data model to handle tags 
    #if new_task.cat and new_task.cat not in task_data["cats"]:
    #    task_data["cats"].append(new_task.cat)

    #return sort_open_tasks()
    #NOTE: I reckon move this to separate fn 




#NOTE:This needs implementing still
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











    
     

    
    
        