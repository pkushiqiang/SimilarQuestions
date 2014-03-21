# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 15:48:52 2014

@author: dlmu__000
"""

import urllib
import pymongo
from dbclient import DbClient 
 

from apiclient import ApiClient 

class LinkedQuestionGetter(ApiClient):
    
    def __init__(self, pageSize, tagged):
        ApiClient.__init__( self, pageSize, tagged)
        self.url_pre = 'http://api.stackexchange.com/2.2/questions/%s/linked?%s'
        
     
    def makeUrl(self, qid):
        param_str = urllib.urlencode(self.base_params)  
        url = self.url_pre % (qid, param_str)
        return url
    
    def getLinkedByQuestion(self, qid):
        url = self.makeUrl(qid)
        content = self.makeRequest(url)
        return content
        
    def saveContent(self,  collection, items ):
        i = 0
        for question in items:
          #  print question["question_id"]
            question["_id"] = question["question_id"]
            try:
                collection.insert(question)
                i+=1
            except pymongo.errors.DuplicateKeyError as e: 
                # print e
                ()
        print " %d question had been saved" %i
        
    def getQuestionIds(self, dbClient, pageSize, pageNo ):
         question_coll = dbClient.getCollection("question_test")
         page = dbClient.getPage(question_coll, pageSize, pageNo)    
         items=[]
         for item in page:
             items.append(item)
         #    print item["_id"], item["title"]
         return items
         
    def saveLinkedByIdPage(self, dbClient, pageSize , pageNo):
        items = self.getQuestionIds(dbClient, pageSize, pageNo)
        collection = dbClient.getCollection("question_link_python")
        i = 0       
        for item in items:
            qid = item["_id"]
            content = self.getLinkedByQuestion(qid)
            json_data = json.loads(content)
            json_data['_id'] = qid
            json_data['title'] = item["title"]
            try:
                collection.insert(json_data)
                i+=1
            except pymongo.errors.DuplicateKeyError as e: 
                # print e
                ()
        print " %d lienked question had been saved" %i
        
def main():
    pageSize = 100
    startPageNo = 1
    endPageNo = 1000
    dbClient = DbClient('localhost', 27017, "SimilarQuestion")            
    linkquestionGetter = LinkedQuestionGetter(30,"python") 
    
    
    for  pg in range(startPageNo, endPageNo):
        print "--get page at : %d -----" % pg
        linkquestionGetter.saveLinkedByIdPage(dbClient, pageSize, pg )
      
    
  
if __name__ == "__main__": 
    main()

          