# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 15:48:52 2014

@author: dlmu__000
"""

import urllib
import pymongo
from dbclient import DbClient 
import time
import sys
import json
 

from apiclient import ApiClient 

class LinkedQuestionGetter(ApiClient):
    
    def __init__(self, pageSize, dbClient, collectionName , tagged=None):
        ApiClient.__init__( self, pageSize, tagged)
        self.url_pre = 'http://api.stackexchange.com/2.2/questions/%s/linked?%s'
        self.dbClient = dbClient
        self.collection =  self.dbClient.getCollection(collectionName)
     
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
         print dbClient
         question_coll = dbClient.getCollection("english_questions")
         page = dbClient.getPage(question_coll,  None , None ,pageSize, pageNo)    
         items=[]
         for item in page:
             items.append(item)
         #    print item["_id"], item["title"]
         return items
         
    def saveResultByIdPage(self,  pageSize , pageNo):
        items = self.getQuestionIds(self.dbClient, pageSize, pageNo)
       
        i = 0       
        for item in items:
            qid = item["_id"]
            
            retry = True           
            while retry:
                try:
                    content = self.getLinkedByQuestion(qid)
                    retry = False
                except IOError as e: 
                    print " "
                    print "meet IO error when get NO. %d, qid=%s" %(i,qid)
                    print e                    
                    time.sleep(10)
                    
            json_data = json.loads(content)
            json_data['_id'] = qid
            json_data['title'] = item["title"]
         #   print len(json_data["items"])
            if len(json_data["items"]) > 0 :
                print len(json_data["items"])
                try:
                    self.collection.insert(json_data)
                    i+=1       
                except pymongo.errors.DuplicateKeyError as e: 
                    # print e
                    ()
        #    if (i%5 == 0 ) :
        #        sys.stdout.write('.')
            time.sleep(0.2)
            
        print " "
        return i
        
class RelatedQuestionGetter(LinkedQuestionGetter):
    def __init__(self, pageSize, tagged):
        ApiClient.__init__( self, pageSize, tagged)
        self.url_pre = 'http://api.stackexchange.com/2.2/questions/%s/related?%s'
        self.collectionName = "related_python"
        
def main():
    pageSize = 100
    startPageNo = 1
    endPageNo = 10000
    dbClient = DbClient('localhost', 27017, "SimilarQuestion")            
    
    linkquestionGetter = LinkedQuestionGetter(100,dbClient, "english_link") 
 
    for  pg in range(startPageNo, endPageNo):
        print "--get page at : %d -----" % pg
        i = linkquestionGetter.saveResultByIdPage( pageSize, pg )
        print " %d lienked question had been saved" %i
    
  
if __name__ == "__main__": 
    main()

          