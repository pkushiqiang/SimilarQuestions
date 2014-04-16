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
        for term in postingsList:
                    
            # this is the ONLY line in this function that is tfidf specific. Most likely, everything
            # else in this function should stay the same for all vectorizers
            vector[term] = postingsList[term].getTFIDF()
            testingVector[term] = postingsList[term].getTFIDF()

            synonymSet = set()
            for synset in wn.synsets(term):
                #print synset.lemma_names
                for synonym in synset.lemma_names:
                    if not term == synonym:
                        synonymSet.add(synonym)
            #print synonymSet
            
            synonymList = []
            scoreList = []
            additionalTerms = []
            tmpterms = wn.synsets(term)
            if len(tmpterms) > 0:
                term1 = tmpterms[0]
                for synonym1 in synonymSet:
                    syn = wn.synsets(synonym1)[0]
                    sim_score = term1.wup_similarity(syn)
                    synonymList.append(synonym1)
                    scoreList.append(sim_score)
                #print zip(scoreList, synonymList)   
                additionalTerms = sorted(zip(scoreList, synonymList), reverse=True)
                additionalTerms = filter(lambda x: x[0]!=None, additionalTerms)
                additionalTerms = additionalTerms[:self.num_syn]            
                
                for score, term2 in additionalTerms:
                    if term2 not in vector:
                        score = postingsList[term].getTFIDF() * score
                        vector[term2] = score
        print vector
        print testingVector
        exit(0)
                
        return vector