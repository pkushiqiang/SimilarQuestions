# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 20:12:09 2014

@author: dlmu__000
"""

import urllib
import urllib2
import gzip
import cStringIO
import json
import pymongo
from dbclient import DbClient 


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
          'tagged' : tagged,
          'site' : 'stackoverflow',
          'order':'desc',
          'sort' : 'activity'}
          
    def getPage(self, pageNo):
        params = self.base_params.copy()
        params['page'] = str(pageNo)
        content = self.makeRequest(params)
        
        json_data = json.loads(content)
        items = json_data["items"]
        return items
        
        
    def makeRequest(self,params):
        param_str = urllib.urlencode(params)  
        url = self.url_pre % param_str
    #    print 'url =', url
        response = urllib.urlopen(url)
        return_data = response.read()
        s = cStringIO.StringIO(return_data)
        gz_data = gzip.GzipFile(fileobj=s, mode='rb')
        content = gz_data.read()
#        print content
        return content
        
    def savePage(self,  collection, items ):
        for question in items:
            print question["question_id"]
            question["_id"] = question["question_id"]
            try:
                collection.insert(question)
            except pymongo.errors.DuplicateKeyError as e: 
                print e
        
        
def main():
    pageSize = 100
    startPageNo = 1
    endPageNo = 1000
    dbClient = DbClient('localhost', 27017, "SimilarQuestion")
    collection = dbClient.getCollection("question_test")
    
    questionGetter = QuestionGetter(pageSize,"python")
    for  pg in range(startPageNo, endPageNo):
        items = questionGetter.getPage(pg)
        questionGetter.savePage(collection,items)          

if __name__ == "__main__": 
    main()
