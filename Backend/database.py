from pymongo import MongoClient
client = MongoClient(
    'mongodb+srv://mohamedmotaz:oVxmDmRXPhIwyyaW@cluster0.iia6ivy.mongodb.net/')
db = client['liftology']
users_col = db['users']
