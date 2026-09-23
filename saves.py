import pickle
import os






SAVE_FILE = 'save_data.pkl'

def load_data():
    if not os.path.exists(SAVE_FILE):
        return {}
    with open(SAVE_FILE, "rb") as f:
        return pickle.load(f)
    
def save_module_data(data_dict, module_name_str):
    master_data = load_data()
    master_data[module_name_str] = data_dict
    with open(SAVE_FILE, 'wb') as f:
        pickle.dump(master_data, f)








