import sys
sys.path.append("/usr/local/lib/python2.7/site-packages/") #PYTHONPATH
import nltk
from nltk.corpus import wordnet as wn
from vectorizer import Vectorizer

class Vectorizer_NV(Vectorizer):
    
    # the only thing you'd change in this function is the string 'name' of the vectorizer. 
    # here the 'name' is 'NounVerb'
    def __init__(self, scope='all'):
        super(type(self),self).__init__('NounVerb'+'-'+scope)
        self.scope = scope
    
    # this is the function that creates the vector. Since the TFIDF code is already written into
    # the document/posting objects, this is a very simple function. others will necessarily be more complex.
    def calculateVector(self, document):
        postingslist = None

        if self.scope == 'title':
            postingsList = document.getPostingsListTitle()
        elif self.scope == 'body':
            postingsList = document.getPostingsListBody()
        else:
            postingsList = document.getPostingsList()
            
        vector = {}
        testingVector={}
        NVlist = ['NN','NNP','NNPS','NNS','VB','VBD','VBG','VBN','VBP','VBZ']
        for term in postingsList:
                    
            # this is the ONLY line in this function that is tfidf specific. Most likely, everything
            # else in this function should stay the same for all vectorizers
            tag = nltk.pos_tag([term])
            if tag[0][1] in NVlist:
                vector[term] = postingsList[term].getTFIDF() * 1.2
            else:
                vector[term] = postingsList[term].getTFIDF()           
            testingVector[term] = postingsList[term].getTFIDF()     
            
            # Another version
            #if tag[0][1] in NVlist:
                #vector[term] = 1.2
            #else:
                #vector[term] = 1         
             
        #print vector
        #print
        #print testingVector
        #exit(0)    
        return vector