#!/usr/bin/env python
# -*- coding: utf-8  -*-
#encoding=utf-8


from index import Index
import collections
from operator import itemgetter
from vectorizer import Vectorizer
import json
import sys
import math
from time import time
import numpy
from scipy import stats as st


class ExperimentEngine():
    debug = False
    distanceMetric = 'cosine'
    onlyDoN = -1
    
    

    def __init__(self, index, linkedDocs, vectorizers):
        # send tweets into index
        self.index = index
        self.linkedDocs = linkedDocs
        self.vectorizers = vectorizers
        
        # get documents from index
        self.documents = self.index.documents
        #print self.documents
        
        
    def getVector(self, vectorizer, documentID=False, document=False):
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
            stats[name]['time'] = self.currentMilliTime()
            results[name] = {}
<<<<<<< HEAD

            
=======
        
        numDocs = 0
        
>>>>>>> FETCH_HEAD
        for doc in set(self.linkedDocs).intersection(set(self.documents)): #we only need to calculate pairs for docs we know links for
            numDocs += 1
            
            #this allows us to shortcut through all the stuff to test the statistics functions
            if self.onlyDoN > 0 and numDocs >= self.onlyDoN: 
                continue
            
            if doc not in self.documents:
                print 'doc not in documents', doc
                continue
            oneIn = False
            for i in self.linkedDocs[doc]:
                if i in self.documents:
                    oneIn = True
                    
            if not oneIn:
                continue
            
            doc = self.documents[doc]
            if self.debug:
                print 'calculating results for',doc.getName()
            
            for name in self.vectorizers:
                results[name] = {}            
            
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
                        results[vname][str(doc.getName())+'&'+str(doc2.getName())] = self.cosineScore(v1,v2)
            for vname in self.vectorizers:
                ndcg,topRank = self.NDCG(results[vname])
                if ndcg != None:
                    stats[vname]['NDCG'] = stats[vname].get('NDCG',[]) + [ndcg]
                    stats[vname]['topRank'] = stats[vname].get('topRank',[]) + [topRank]
        
        ''' accumulate stats '''
        
        for vname in results:            
            stats[vname]['time'] = int(self.currentMilliTime() - stats[vname]['time'])
            ndcg = numpy.array(stats[vname]['NDCG'])
            stats[vname]['_NDCG_max'] = max(stats[vname]['NDCG'])
            stats[vname]['_NDCG_min'] = min(stats[vname]['NDCG'])
            stats[vname]['_NDCG_mean'] = numpy.mean(ndcg)
            stats[vname]['_NDCG_median'] = numpy.median(ndcg)
            stats[vname]['_NDCG_mode']= min(st.mode(ndcg)[0])
            stats[vname]['_NDCG_standardDeviation'] = numpy.std(ndcg, axis = 0)
            topRank = numpy.array(stats[vname]['topRank'])
            stats[vname]['_TopRank_max'] = max(stats[vname]['topRank'])
            stats[vname]['_TopRank_min'] = min(stats[vname]['topRank'])
            stats[vname]['_TopRank_mean'] = numpy.mean(topRank)
            stats[vname]['_TopRank_median'] = numpy.median(topRank)
            stats[vname]['_TopRank_mode']= min(st.mode(topRank)[0])
            stats[vname]['_TopRank_standardDeviation'] = numpy.std(topRank, axis = 0)
            stats[vname]['_Percent@Rank1'] = float(stats[vname]['topRank'].count(1))/len(stats[vname]['topRank'])

        print json.dumps(stats)
        print '\n\n\n\n'
        
        
        for i in stats:
            print i
            for k in sorted(stats[i]):
                print ' ', k+":", stats[i][k]       
        
        return stats
        
    
    def NDCG(self, results):
        def reverse_numeric(x, y):
            if y - x > 0:
                return 1
            if y-x < 0:
                return -1
            else:
                return 0
        
        results = sorted(results.items(), key=itemgetter(1), cmp=reverse_numeric)
        

        rank = 0
        dcg = 0
        numRelevant = 0
        topRank = -1
        
        for i in results:
            #print i
            rank += 1
            docs = i[0].split('&')
            d1 = int(docs[0])
            d2 = int(docs[1])
            if d2 in self.linkedDocs[d1]:
                if topRank == -1:
                    topRank = rank
                numRelevant += 1
                dcg += 1 / math.log(1+rank) #normally dcg is 2**rel -1 /... but since our rel values are 1...
        if numRelevant > 0:       
            return dcg / self.IDCG(numRelevant), topRank

        return None, None
    
    def IDCG(self, numRelevantDocs):
        idcg = 0
        for i in range(1,numRelevantDocs+1):
            idcg += 1/math.log(1+i)
        return idcg
            
    def cosineScore(self, vector1, vector2):
        # calculate dot product
        dotProduct = self.getDotProduct(vector1,vector2)
                
        # get magnitudes
        magnitudes = Vectorizer.getMagnitude(vector1) * Vectorizer.getMagnitude(vector2)
 
        if magnitudes == 0:
            magnitudes = 0 + sys.float_info.epsilon #the smallest possible value. avoid divide by zero error
        return dotProduct/magnitudes
        
    
    
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
    
    def currentMilliTime(self):
        return int(round(time() * 1000))


def main():
    pass
    

if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    