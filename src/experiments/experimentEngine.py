#!/usr/bin/env python
# -*- coding: utf-8  -*-
#encoding=utf-8


from index import Index
import collections
from operator import itemgetter
from vectorizer import Vectorizer
import json
import sys


class ExperimentEngine():
    debug = True
    distanceMetric = 'cosine'
    
    

    def __init__(self, index, vectorizers):
        # send tweets into index
        self.index = index
        self.vectorizers = vectorizers
        
        # get documents from index
        self.documents = self.index.documents
        #print self.documents
        
        
    def getVector(self, vectorizer, documentID = False, document=False):
        if documentID:
            return vectorizer.getVector(self.documents[documentID])
        elif document:
            return vectorizer.getVector(document)
        return None
    
    
    def runExperiments(self):
        ''' there are lots of stats we want to keep track of here. so we're going to store them in a dictionary for easy returning. '''
        stats = {}
        results = {}
        
        for name in self.vectorizers:
            stats[name] = {}
            results[name] = {}
        
        for doc in self.documents:
            doc = self.documents[doc]
            print 'calculating results for',doc.getName()
            
            
            for doc2 in self.documents:
                doc2 = self.documents[doc2]
                if doc2 == doc:
                    continue
                
                for vname in self.vectorizers:
                    #we're asking for it backward (doc2&doc), since we wouldn't calculate the same one twice
                    if str(doc2.getName())+'&'+str(doc.getName()) not in results[vname]: 
                        vectorizer = self.vectorizers[vname]
                        v1 = vectorizer.getVector(doc)
                        v2 = vectorizer.getVector(doc2)
                        results[vname][str(doc2.getName())+'&'+str(doc.getName())] = self.cosineScore(v1,v2)
        
        ''' accumulate stats '''
        for vname in results:
            accum = 'sum of scores'
            stats[vname][accum] = 0
            stats[vname]['total # of scores'] = len(results[vname])
            for result in results[vname]:
                stats[vname][accum] += results[vname][result]
            
        
        print stats        
        
        return stats
        
    
            
            
    def cosineScore(self, vector1, vector2):
        # calculate dot product
        dotProduct = self.getDotProduct(vector1,vector2)
                
        # get magnitudes
        magnitudes = Vectorizer.getMagnitude(vector1) * Vectorizer.getMagnitude(vector2)
 
        if magnitudes == 0:
            magnitudes = 0 + sys.float_info.epsilon #the smallest possible value. avoid divide by zero error
        return 1 - (dotProduct/magnitudes)
        
    
    
    def getDotProduct(self, vector1, vector2):
        dotProduct = 0.0
        #print postingsDoc
        #print postingsQuery
        for term in set(vector1.keys() + vector2.keys()):
            d1 = 0
            d2 = 0
            if term in vector1 and term in vector2:
                d1 = vector1[term]
                d2 = vector2[term]
                dotProduct += d1*d2
        return dotProduct    
    

        
    def sortDictionary(self, dictionary): 
        def reverse_numeric(x, y):
            if y - x > 0:
                return 1
            if y-x < 0:
                return -1
            else:
                return 0
                        
        return collections.OrderedDict(sorted(dictionary.items(), key=itemgetter(1)))
    



def main():
    pass
    

if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    