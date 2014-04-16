# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 21:07:38 2014

@author: dlmu__000
"""
from dbclient import DbClient
import json

class DataProcessor:
    
    def __init__(self) : 
        self.dbClient = DbClient('localhost', 27017, "SimilarQuestion")            
    
    @staticmethod
    def processQuestion(question):
         a = {}
         a["qid"] = question["_id"]
         a["title"] = question["title"]
         return a
         
    @staticmethod
    def processLinkedQuestion(question):
         a = {}
         a["qid"] = question["_id"]
         a["title"] = question["title"] 
         a["linked"] = []
         for item in question["items"]:
             b = {}
             b["qid"] = item["question_id"]
             b["title"] = item["title"] 
             print b
             a["linked"].append(b)
         return a     
    
    @staticmethod
    def processLinkedQuestion2(question):
         a = {}
         a["qid"] = question["_id"]          
         a["linked"] = []
         for item in question["items"]:
             a["linked"].append(item["question_id"])
         return a       
    
    @staticmethod
    def processRelatedQuestion(question):
         a = {}
         a["qid"] = question["_id"]
         a["title"] = question["title"] 
         a["related"] = []
         for item in question["items"]:
             b = {}
             b["qid"] = item["question_id"]
             b["title"] = item["title"] 
         #    print b
             a["related"].append(b)
         return a       
      
    
    def dumpDataToFile(self, queFun , collection, find_spec ,find_sort, fileName,pageNum):
        pageSize = 1000 
        pageNo = 1
        has_more = True
        with open(fileName, 'w') as the_file:
           # the_file.write('Hello\n')        
            while has_more and pageNo <= pageNum :
                page = self.dbClient.getPage(collection, find_spec ,find_sort, pageSize, pageNo)    
                pageNo+=1 
                count =  page.count(with_limit_and_skip = True)
                print "count=",count
                if ( count < pageSize ) :
                    has_more = False
                for item in page:
                     a = queFun(item)
                     jstr = json.dumps(a)+'\n'
                     the_file.write(jstr)
                print " page %d saved %d lines in file" %(pageNo-1, count  )
        
    def dumpPythonQuestions(self,pageNum):
        question_coll = self.dbClient.getCollection("question_test")
        fileName = "..\..\data\pyton_questions.txt"
        self.dumpDataToFile(DataProcessor.processQuestion, question_coll, fileName,pageNum)
     
    def dumpLinkedQuestions(self, collectionName, fileName, pageNum=1000):
         question_coll = self.dbClient.getCollection(collectionName)
         find_spec = { "items" : { "$exists":True},  
                  "$where" : "this.items.length > 1" }  
         find_sort = { "items" : { "$size" :-1} } 
         
         self.dumpDataToFile(DataProcessor.processLinkedQuestion2, question_coll, find_spec, find_sort ,fileName,pageNum)
    
    
    def dumpLinkedQuestions2(self,pageNum):
         question_coll = self.dbClient.getCollection("question_link_python")
         fileName = "..\..\data\python_linked.txt"
         find_spec = { "items" : { "$exists":True},  
                  "$where" : "this.items.length > 1" }  
         find_sort = { "items" : { "$size" :-1} }          
         self.dumpDataToFile(DataProcessor.processLinkedQuestion2, question_coll, find_spec, find_sort ,fileName,pageNum)
     
    def dumpRelatedQuestions(self,pageNum):
         question_coll = self.dbClient.getCollection("related_python")
         fileName = "..\..\data\question_related_python.txt"
         find_spec = { "items" : { "$exists":True},  
                  "$where" : "this.items.length > 5" } 
         find_sort = None
         
         self.dumpDataToFile(DataProcessor.processRelatedQuestion, question_coll, find_spec, find_sort ,fileName,pageNum)
     
    def dumpQuestion(self, collectionName, fileName, pageNum=1000):
          question_coll = self.dbClient.getCollection(collectionName)         
          self.dumpDataToFile(DataProcessor.processQuestion, question_coll, None, None, fileName,pageNum)
    
    
def main():
    dataProcessor = DataProcessor()    
  #  dataProcessor.dumpPythonQuestions(1000)
  #  dataProcessor.dumpLinkedQuestions(10)
  #  dataProcessor.dumpRelatedQuestions(1000)
  #  dataProcessor.dumpLinkedQuestions2(10)
    '''   
    colletionName = "english_questions" 
    fileName = "..\..\data\english_questions.txt"
    dataProcessor.dumpQuestion( colletionName, fileName ) 
    '''  
    colletionName = "english_link" 
    fileName = "..\..\data\english_link.txt"
    dataProcessor.dumpLinkedQuestions(colletionName, fileName)
   
if __name__ == "__main__": 
    main()