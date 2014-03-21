# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 20:55:46 2014

@author: dlmu__000
"""

from pymongo import MongoClient

class DbClient:
    
    def __init__(self, host, port, dbName):
         self.client = MongoClient(host, port)
         self.db = self.client[dbName]
    
    def getCollection(self, collection_name):
        return self.db[collection_name]
        
    def getPage(self, collection, pageSize, pageNo):
        _skip = (pageNo-1) * pageSize
        page = collection.find(skip = _skip, limit=pageSize)
        return page        
        
         
 