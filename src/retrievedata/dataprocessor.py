# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 21:07:38 2014

@author: dlmu__000
"""

class DataProcessor:
    
    def __init__(self) : 
        self.dbClient = DbClient('localhost', 27017, "SimilarQuestion")            
    
    def dumpDataToFile(self, collection, fileName,pageNum):
        pageSize = 1000 
        pageNo = 1
        has_more = True
        with open(fileName, 'w') as the_file:
           # the_file.write('Hello\n')        
            while has_more and pageNo <= pageNum :
                page = self.dbClient.getPage(collection, pageSize, pageNo)    
                pageNo+=1 
                count =  page.count(with_limit_and_skip = True)
                if ( count < pageSize ) :
                    has_more = False
                for item in page:
                     a = {}
                     a["qid"] = item["_id"]
                     a["title"] = item["title"]
                     jstr = json.dumps(a)+'\n'
                     the_file.write(jstr)
                print " page %d saved %d lines in file" %(pageNo-1, count  )
        
    def dumpPythonQuestions(self,pageNum):
        question_coll = self.dbClient.getCollection("question_test")
        fileName = "..\..\data\pyton_questions.txt"
        self.dumpDataToFile(question_coll, fileName,pageNum)
        

def main():
    dataProcessor = DataProcessor()    
    dataProcessor.dumpPythonQuestions(1000)
   
if __name__ == "__main__": 
    main()