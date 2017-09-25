from pymongo import MongoClient


class MongoConnection(object):
    
    def __init__(self):
        client = MongoClient('localhost', 27017, maxPoolSize=50)
        self.db = client['collegereview']
    
    def get_collection(self, name):
        self.collection = self.db[name]
