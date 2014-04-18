import math
from cache import Cache

class Vectorizer(object):
    cache = Cache(20000) # this cache (behaves just like a queue/dictionary) should be referenced static
    dataset = ''
    
    
    def __init__(self, name):
        self.name = name
    
    def getName(self):
        return self.name + '-'+ Vectorizer.dataset
    
    def getVector(self, document):
        if (str(document.getName())+'&'+self.getName()) in self.cache:
            return Vectorizer.cache[(str(document.getName())+'&'+self.getName())]
        
        vector = self.calculateVector(document)
        
        #save to cache
        Vectorizer.cache[(str(document.getName())+'&'+self.getName())] = vector
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
    
    