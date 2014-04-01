# -*- coding: utf-8 -*-
"""
Created on Tue Apr 01 16:05:51 2014

@author: dlmu__000
"""
import json

def findbilink(fileName):
    qidDict = {}
    with open(fileName, 'r') as the_file:
        for line in the_file:
            question = json.loads(line)
            qidDict[question["qid"]] = question["linked"]
    
    for qid in qidDict.keys():
        linked = qidDict[qid]
     #   print linked
        for qid2 in linked:
            if qidDict.has_key(qid2):
                if qid in qidDict[qid2]:
                    print qid,"," , qid2
            
        
        
def main():
    findbilink("..\..\data\python_linked.txt")
        
            
            
if __name__ == "__main__": 
    main()
