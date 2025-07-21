import json
import os

DATA_FILE = "user_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user(user_id):
    data = load_data()
    return data.get(str(user_id), None)

def update_user(user_id, new_data):
    data = load_data()
    user = data.get(str(user_id), {})
    user.update(new_data)
    data[str(user_id)] = user
    save_data(data)

def add_user(user_id, first_name):
    data = load_data()
    if str(user_id) not in data:
        data[str(user_id)] = {
            "coins": 0,
            "checkin_day": 0,
            "spin_count": 0,
            "name": first_name,
            "ref_by": None,
            "ref_team": [],
            "gen_rate": 0,
            "photo": None,
        }
        save_data(data)

def get_all_users():
    data = load_data()
    return [int(uid) for uid in data.keys()]
  
