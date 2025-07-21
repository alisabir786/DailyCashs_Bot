```python
from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["dailycashs"]
users = db["users"]


def get_user(user_id):
    user = users.find_one({"_id": user_id})
    if not user:
        user = {
            "_id": user_id,
            "coins": 0,
            "ref_by": None,
            "ref_count": 0,
            "ref_earn": 0,
            "checkin": 0,
            "spin_left": 5,
            "tasks_done": [],
            "name": "",
            "photo": ""
        }
        users.insert_one(user)
    return users.find_one({"_id": user_id})


def update_user(user_id, data):
    users.update_one({"_id": user_id}, {"$set": data})


def add_coins(user_id, coins):
    users.update_one({"_id": user_id}, {"$inc": {"coins": coins}})
```
