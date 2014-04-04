#!/usr/bin/env python
# -*- coding: utf-8  -*-
#encoding=utf-8


from tweetcollector import TweetCollector
import math
import random
from index import Index
import collections
from operator import itemgetter
import json
import sys


class Cluster():
    documents = []
    dVectors = []
    numTrials = 50
    debug = True
    distanceMetric = 'cosine'
    
    def testing__init__(self):
        doc1 = {"music":2,"katyperry":2,"artpop":1,"ladygaga":1}
        doc2 = {"music":1,"johnny":1,"football":3,"basketball":2,"aggies":4}
        print self.distanceBetween(doc1,doc2)

    def __init__(self, tweets):
        # send tweets into index
        self.index = Index(tweets)
        
        # get documents from index
        self.documents = self.index.documents
        #print self.documents
        
        self.dVectors = [None]*len(self.documents)
        
        ''' we want a slightly easier way to deal with the documents, so we're translating them
        from what we had before (document objects) to dictionaries of words -> tfidf values
        so we don't have to recompute tfidf values again and again and again... '''
        for d in sorted(self.documents.keys()):
            doc = self.documents[d]
            vecs = {}
            for posting in doc.getPostingsList().values():
                vecs[posting.getTerm()] = self.getTFIDF(posting)
            
            
            ''' so now we have vectors of all words in the document... but maybe we just want the top x '''
            #vecs = self.reduceDimensionality(vecs)
            
            self.dVectors[d] = vecs
        
        ''' just for testing '''
        #self.dVectors = createDummyData()
        #self.documents = None        
        
        print self.cosineScore(self.dVectors[1],self.dVectors[1])
        
        ''' run kmeans for k = 2 '''
        statsFor2 = self.runKMeans(2)
        ''' run kmeans for k = 4 '''
        statsFor4 = self.runKMeans(4)
        ''' run kmeans for k = 6 '''
        statsFor6 = self.runKMeans(6)
        ''' run kmeans for k = 8 '''
        statsFor8 = self.runKMeans(8)
        
        ''' start printing stats '''
        print "-------------------------------------------------------------------"
        distanceFromOrigin = 0
        for document in self.dVectors:
            if self.distanceMetric == 'euclidean':
                distanceFromOrigin += self.distanceBetween({},document)
            elif self.distanceMetric == 'cosine':
                distanceFromOrigin += self.cosineScore({}, document)
            else:
                print 'you have not defined a distance metric'
            
        print 'STATISTICS REPORT FOR K = 1, WHERE THE CENTER IS THE ORIGIN:'
        print "  RSS:", distanceFromOrigin        
        
        self.printStats(statsFor2)        
        self.printStats(statsFor4)        
        self.printStats(statsFor6)        
        self.printStats(statsFor8)        
        
        
    def printStats(self, stats):
        print "-------------------------------------------------------------------"
        print 'STATISTICS REPORT FOR K =',stats['k']        
        print "  AVERAGE # ITERATIONS:", stats['avgIterations']
        print "  BEST RSS (RESTART #",str(stats['bestRestartID'])+"):", stats['bestRSS']
        print "  BEST PURITY (RESTART #",str(stats['bestRestartID'])+"):", stats['bestPurity']        
        print "  BEST ORIGINAL RANDOM MEANS (RESTART #",str(stats['bestRestartID'])+"):", stats['bestRandomCenters']
        print "  BEST CLUSTERING (RESTART #",str(stats['bestRestartID'])+"):"
        for clusterID, cluster in enumerate(stats['bestClustering']):
            print "  ", clusterID, cluster         
        
    def calculatePurity(self, clustering):
        purity = 0.
        numDocuments = 0.
        for cluster in clustering:
            classesInCluster = []
            for documentID in cluster:
                numDocuments += 1
                classesInCluster += [self.documents[documentID].cluster]
            mostPopularClass = max(set(classesInCluster), key=classesInCluster.count)
            purity += classesInCluster.count(mostPopularClass)
                
        purity = purity / numDocuments
        
        return purity
        
    def runKMeans(self, k, numRestarts = 1000, maxIterations = 10):
        ''' there are lots of stats we want to keep track of here. so we're going to store them in a dictionary for easy returning. '''
        stats = {}
        stats['k'] = k
        
        ''' we only want to return the residual sum of scores value for the best clustering we find, so we keep track of it here. '''
        stats['bestRSS'] = float('inf')
        totalIterationCount = 0
        
        ''' some randomness isn't so great, so we try it many many times! '''
        for restart in range(numRestarts):
            if self.debug:
                print "-------------------------------------------------------------------"
                print "k =",k
                print "RANDOM RESTART #"+str(restart)
            
            ''' find k random centers '''
            randomCenters, randomNumbers = self.getKRandomCenters(k)
            centers = randomCenters
        
            docsInCluster = []
            oldDocsInCluster = []
            oldRSS = float('inf')
            iterationCount = 0
            converged = False
            
            while not converged and iterationCount < maxIterations:
                iterationCount += 1.
            
                ''' create a data structure to find which documents belong to which cluster '''
                docsInCluster=[[] for x in range(k)] #this will hold a list of k lists        
                
                ''' for each document, find the center that's closest '''
                for documentID, document in enumerate(self.dVectors):
                    closestCluster = self.findClosestCenterToDocument(document, centers)
                    docsInCluster[closestCluster] += [documentID]
                    
                ''' calculate the residual sum of squares '''
                rss = self.residualSumOfSquares(centers, docsInCluster)
                if rss < stats['bestRSS']:
                    stats['bestRSS'] = rss
                    stats['bestClustering'] = docsInCluster
                    stats['bestRandomCenters'] = randomNumbers
                    stats['bestRestartID'] = restart
                    
                ''' for each cluster, move the cluster center '''
                newcenters = []
                for docs in docsInCluster:
                    newcenters += [self.findNewClusterCenter(docs)]
                            
                ''' update centers to be the new list we just created '''
                centers = list(newcenters)
                
                ''' print cluster assignments (for debugging)'''
                if self.debug:
                    print "FOR ITERATION #"+str(iterationCount)+", the RSS is:",rss,"and the distribution is:"
                    for clusterID, cluster in enumerate(docsInCluster):
                        print " ", clusterID, cluster

                
                converged = self.converged(docsInCluster,oldDocsInCluster)
                
                if rss > oldRSS:
                    if(self.debug):
                        print 'RSS INCREASED THIS ITERATION, ROLLING BACK TO OLD RSS'
                    converged = True
                
                print "Center that's closest to zero:",self.findClosestCenterToDocument({}, centers)
                
                oldDocsInCluster = docsInCluster
                oldRSS = rss
                
                
            totalIterationCount += iterationCount
            
        stats['avgIterations'] = totalIterationCount/numRestarts
        stats['bestPurity'] = self.calculatePurity(stats['bestClustering'])
                
        return stats
        
    def residualSumOfSquares(self, centers, clusterMembers):
        ''' loop through each cluster '''
        rss = 0.
        for clusterID in range(len(centers)):
            
            ''' increment rss by the distances between a document and its cluster center '''
            for documentID in clusterMembers[clusterID]:
                if self.distanceMetric == 'euclidean':
                    rss += self.distanceBetween(self.dVectors[documentID],centers[clusterID])**2
                elif self.distanceMetric == 'cosine':
                    rss += self.cosineScore(self.dVectors[documentID],centers[clusterID])**2
                else:
                    print 'you have not defined a distance metric'
        return rss
    
    def findNewClusterCenter(self, clusterMembers):
        ''' create dictionary to contain the new list of all words in the cluster '''
        newcenter = {}
        newcenterCounts = {}
        
        ''' loop through each member of the cluster '''
        for documentID in clusterMembers:
            document = self.dVectors[documentID]
            
            ''' loop through term word in the document '''
            for term in document:
                
                ''' add the term's value in the document to its corresponding term in newcenter '''
                newcenter[term] = newcenter.get(term, 0) + document[term]
                #newcenterCounts[term] = newcenterCounts.get(term, 0.) + 1
                #newcenter[term] = min(newcenter.get(term, float('inf')), document[term])
        
        ''' normalize each term by the total number of items in the cluster '''        
        for term in newcenter:
            newcenter[term] = float(newcenter[term])/len(clusterMembers)
            #newcenter[term] = float(newcenter[term])/newcenterCounts[term]        
            #print term, newcenter[term]            

        return newcenter
            
    def converged(self, clustering1, clustering2):
        if len(clustering1) != len(clustering2):
            return False
        for clusterID in range(len(clustering2)): #could have used either
            if not set(clustering1[clusterID]) == set(clustering2[clusterID]):
                return False
        return True
        
    def findClosestCenterToDocument(self, document, centers):
        ''' calculate the k distances '''
        distances = []
        for center in centers:
            if self.distanceMetric == 'euclidean':
                distances += [self.distanceBetween(document,center)]
            elif self.distanceMetric == 'cosine':
                distances += [self.cosineScore(document, center)]
            else:
                print 'you have not defined a distance metric'
        
        ''' return the index of the minimum distance '''
        return distances.index(min(distances))
    
    def getKRandomCenters(self, k):
        ''' find k unique numbers (will be indexes of our centers) '''
        kRandomNumbers = []
        while len(kRandomNumbers)<k:
            randomNumber = random.randint(0,len(self.dVectors)-1)
            if randomNumber not in kRandomNumbers:
                kRandomNumbers += [randomNumber]
                
        if self.debug:
            print 'ORIGINAL RANDOM MEANS:', kRandomNumbers
        
        ''' get those k random items into array (in increasing order) '''
        kRandomCenters = []
        for index in sorted(kRandomNumbers)[::-1]:
            kRandomCenters += [self.dVectors[index]]
        
        return kRandomCenters, kRandomNumbers
    
    
    
    def distanceBetween(self,postings1,postings2): #squared euclidian distance
        
        distance=0.
        
        for i in set(postings1.keys() + postings2.keys()):
            value1 = 0.
            value2 = 0.
            #print i,
            if i in postings1:
                value1 = postings1[i]
            if i in postings2:
                value2 = postings2[i]
                
            # get difference, square it, 
            distance += abs(value1 - value2)**2
            
        #print distance
        return distance
            
            
    def cosineScore(self, document1, document2):
        # calculate dot product
        dotProduct = self.getDotProduct(document1,document2)
        
        # get magnitudes
        magnitudes = self.calculateMagnitudeOfVector(document1) * self.calculateMagnitudeOfVector(document2)
 
        if magnitudes == 0:
            magnitudes = 0 + sys.float_info.epsilon #the smallest possible value. avoid divide by zero error
        return 1 - (dotProduct/magnitudes)
        
    def calculateMagnitudeOfVector(self, vector):
        mag = 0.
        for term in vector:
            mag += vector[term]**2
        mag = math.sqrt(mag)
        return mag
    
    def getDotProduct(self, document1, document2):
        dotProduct = 0.0
        #print postingsDoc
        #print postingsQuery
        for term in set(document1.keys() + document2.keys()):
            d1 = 0
            d2 = 0
            if term in document1 and term in document2:
                d1 = document1[term]
                d2 = document2[term]
                dotProduct += d1*d2
        return dotProduct    
    
    
    def getTFIDF(self, posting):
        tf = posting.getTF()
        idf = self.index.getIDF(posting.getTerm())
        
        '''
        if self.debug:
            print 'tfidf for', posting.getTerm()
            print 'TF:   ', tf
            print 'DF:   ', self.index.getTerm(posting.getTerm()).getDocumentFrequency()
            print 'IDF:  ', idf
            print 'TFIDF:', tf*idf 
        '''
        
        #return tf*idf #* 10   # multiply by some number because values < 1 square differently... just wanted to exaggerate the distances
        return tf
        #return random.randint(0,50)
        
    def sortDictionary(self, dictionary): 
        def reverse_numeric(x, y):
            if y - x > 0:
                return 1
            if y-x < 0:
                return -1
            else:
                return 0
                        
        return collections.OrderedDict(sorted(dictionary.items(), key=itemgetter(1)))
    
    def reduceDimensionality(self, dictionary, numItemsToKeep=20):
        sorteddict = self.sortDictionary(dictionary)
        newdict = {}
        for i in range(numItemsToKeep):
            term = sorteddict.popitem()
            newdict[term[0]] = term[1] #term[0] is the term and term[1] is the tfidf value
        
        return newdict

def createDummyData():
    tweets = []
    tweets += [{'please':1., 'work':1.}]
    tweets += [{'please':1.5, 'work':2.}]
    tweets += [{'please':3., 'work':4.}]
    tweets += [{'please':5., 'work':7.}]
    tweets += [{'please':3.5, 'work':5.}]
    tweets += [{'please':4.5, 'work':5.}]
    tweets += [{'please':3.5, 'work':4.5}]
    return tweets
    

def collectTweets():
    tc = TweetCollector()
    queries={}
    queries['facebook'] =['"Jan Koum"', '"WhatsApp"', '"#SEO"', '"facebook"', '"#socialmedia"', '"Zuckerberg"', '"user privacy"', '"#Instagram"']
    queries['music']=['"#katyperry"', '"#katycats"', '"#darkhorse"', '"#iHeartRadio"', '"#ladygaga"', '"#TaylorSwift"', '"#sxsw"', '"Rolling Stone"']
    queries['rockets']=['"@DwightHoward"', '"#rockets"', '"jeremy lin"', '"toyota center"', '"kevin mchale"', '"houston nba"', '"James Harden"', '"linsanity"']
    queries['ukraine'] = ['"Ukraine"', '"#tcot"', '"Obama"', '"Russia"', '"Putin"', '"White House"', '"Rand Paul"', '"foreign policy"' ]
    
    
    #queries['music']=['"#katyperry"']
    #queries['rockets']=['"@DwightHoward"']
    #queries['facebook'] =['"Jan Koum"']
    #queries['ukraine'] = ['"Obama"']       
       
    totalTweets = []
    
    for i in sorted(queries.keys()):
        for j in queries[i]:
            tweets = tc.search_tweets(j)
            totalTweetsForJ = ''
            for tweet in tweets:
                totalTweetsForJ += tweet["text"] + " "
    
            totalTweets += [{"cluster": i,"text":totalTweetsForJ }]

    for i in range(len(totalTweets)):
        print i, totalTweets[i]
        
    print len(totalTweets), "Total Tweets Matching Provided Queries"
    
    
    #print totalTweets
    
    return totalTweets


def testingMain():
    #test distance function:
    Cluster()

def main():
    tweets = json.loads(open("tweets.txt").read())
    #tweets = collectTweets()
    
    '''
    tweetsFile = open('tweets.txt', 'w+')
    tweetsFile.write(json.dumps(tweets))
    tweetsFile.close()
    '''
    
    cluster = Cluster(tweets)

if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    