# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 20:12:09 2014

@author: dlmu__000
"""

import urllib
import gzip
import cStringIO
import json
import pymongo
from dbclient import DbClient 
import time


'''
page=1&
pagesize=5
&order=desc
&sort=activity
&tagged=python
&site=stackoverflow
'''

class QuestionGetter:
    
    def __init__(self, pageSize, tagged):
        self.url_pre = 'http://api.stackexchange.com/2.2/questions/?%s'
        self.base_params = {'key' : 'Fmpa7vY9rZzZgJoEz1ilEw((',
          'page' : '1',
          'pagesize' : str(pageSize),
       #   'tagged' : tagged,
          'site' : 'english.stackexchange.com',
          'order':'desc',
          'sort' : 'activity',
          'filter': '!)re8-BBbvkEcM)sDXs2P' }
          
    def getPage(self, pageNo):
        params = self.base_params.copy()
        params['page'] = str(pageNo)
        content = self.makeRequest(params)
        
        json_data = json.loads(content)    
     #   print json_data
        has_more = json_data["has_more"]
        print "has_more= " , has_more
        
        if has_more :
            if "items" in json_data:            
                return json_data["items"]
            else : 
                return "NO_ITEMS"
        else:
            return "NO_MORE"
        
    def makeRequest(self,params):
        param_str = urllib.urlencode(params)  
        url = self.url_pre % param_str
        retry = True
        print 'url =', url
        while (retry):
            try : 
                response = urllib.urlopen(url)
                return_data = response.read()
                s = cStringIO.StringIO(return_data)
                gz_data = gzip.GzipFile(fileobj=s, mode='rb')
                content = gz_data.read()
                retry = False
            except IOError as e:
                print e
    #        print content
        return content
        
    def savePage(self,  collection, items ):
        i = 0
        for question in items:
        #    print question["question_id"]
            question["_id"] = question["question_id"]
            try:
                collection.insert(question)
                i+=1
            except pymongo.errors.DuplicateKeyError as e: 
                #print e
                ()
        return i
        
def main():
    pageSize = 100
    startPageNo = 12
    endPageNo = 10000
    dbClient = DbClient('localhost', 27017, "SimilarQuestion")
    collection = dbClient.getCollection("english_questions")
    
    questionGetter = QuestionGetter(pageSize,"")
    for  pg in range(startPageNo, endPageNo):
        print "--- get page %d ---" %pg
        items = questionGetter.getPage(pg)

     #   print items
        if ( items == "NO_MORE" ) :
            print "have no more questions, quit program !!"
            break
        
        print "--- page %d has %d questions ---" %(pg,len(items))
        if ( items != "NO_ITEMS" ) :
           i = questionGetter.savePage(collection,items) 
        print "--- page %d has save %d question " %(pg,i)
    #    time.sleep(10)       
        
if __name__ == "__main__": 
    main()
