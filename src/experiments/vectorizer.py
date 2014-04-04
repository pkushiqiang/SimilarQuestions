import math
from cache import Cache

class Vectorizer(object):
    cache = Cache(10000) # this cache (behaves just like a queue/dictionary) should be referenced as static
    
    def __init__(self, name):
        self.name = name
    
    def getName(self):
        return self.name
    
    def getVector(self, document):
        if (document.getName(),self.getName()) in self.cache:
            return Vectorizer.cache[(document.getName(),self.getName())]
        
        vector = self.calculateVector(document)
        
        #save to cache
        Vectorizer.cache[(document.getName(),self.getName())] = vector
        return vector
        
    ''' this is the function that will be overwritten by all subclasses '''   
    def calculateVector(self, document):
        pass
    
    @staticmethod
    def getMagnitude(vector):
        mag = 0.
        for term in vector:
            mag += vector[term]**2
        mag = math.sqrt(mag)
        return mag
    
    