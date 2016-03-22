from pymongo import MongoClient
import datetime

class DB(object):
    
    def __init__(self, name, collection):
        self.name = name
        self.collection = collection
        self.db = None

        
    def add_many(self, items):
        client = MongoClient()
        
        #select db and collection 
        db = client[self.name]
        coll = db[self.collection]
        
        if coll.insert_many(items):
            return True
        else:
            return False
            
    def find(self, term):
        client = MongoClient()
        
        #select db and collection 
        db = client[self.name]
        coll = db[self.collection]
        
        data = coll.find(term)  
        return data      
        
        
         