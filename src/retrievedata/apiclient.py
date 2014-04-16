# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 15:02:30 2014

@author: dlmu__000
"""

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
import time 
import sys


'''
page=1&
pagesize=5
&order=desc
&sort=activity
&tagged=python
&site=stackoverflow
'''
#key 1 U4DMV*8nvpm3EOpvf69Rxw((
#key 2 Se74ZqQ*GozLe6md0RE4UA((
#key 3 EbLWZXUAdGFwspI2B3pnzQ((

class ApiClient:
    
    def __init__(self, pageSize, tagged=None):
        self.url_pre = 'http://api.stackexchange.com/2.2/questions/?%s'
        self.base_params = {'key' : 'EbLWZXUAdGFwspI2B3pnzQ((',
          'page' : '1',
          'pagesize' : str(pageSize),          
          'site' : 'stackoverflow',
          'order':'desc',
          'sort' : 'activity'}
        if  tagged is not None: 
           self.base_params['tagged'] = tagged
          
    def getPage(self, pageNo):
        params = self.base_params.copy()
        params['page'] = str(pageNo)
        content = self.makeRequest(params)
        
        json_data = json.loads(content)
        if "items" in json_data:
            items = json_data["items"]
            return items
        else :
            print json_data
            #sys.exit()
            return "NO_ITEMS"
        
    def makeUrl(self,params):
        param_str = urllib.urlencode(params)  
        url = self.url_pre % param_str
        return url
        
    def makeRequest(self,url):
        
    #    print 'url =', url
        response = urllib.urlopen(url)
        return_data = response.read()
       # print return_data
        s = cStringIO.StringIO(return_data)
        gz_data = gzip.GzipFile(fileobj=s, mode='rb')
        content = gz_data.read()
#        print content
        return content
        

        
def main():
    pageSize = 100
    startPageNo = 13
    endPageNo = 10000
    dbClient = DbClient('localhost', 27017, "SimilarQuestion")
    collection = dbClient.getCollection("question_test")
    
    questionGetter = QuestionGetter(pageSize,"python")
    for  pg in range(startPageNo, endPageNo):
        print "--get page at : %d -----" % pg
        items = questionGetter.getPage(pg)
        if items == "NO_ITEMS":
            break
        print "--page at : %d have %d questions--" % (pg, len(items))
        questionGetter.savePage(collection,items)   
        time.sleep(10)

if __name__ == "__main__": 
    main()
