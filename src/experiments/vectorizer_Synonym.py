import sys
sys.path.append("/usr/local/lib/python2.7/site-packages/") #PYTHONPATH
import nltk
from nltk.corpus import wordnet as wn
from vectorizer import Vectorizer

class Vectorizer_Synonym(Vectorizer):
    
    # the only thing you'd change in this function is the string 'name' of the vectorizer. 
    # here the 'name' is 'Synonym'
    def __init__(self, num_syn, scope='all'):
        super(type(self),self).__init__('Synonym'+'-'+scope)
        self.num_syn = int(num_syn)
        
        if self.num_syn == 3:
            print 'we are not running synonym 3 for now.'
            exit(0)
        
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
        
        for term in postingsList:
            
            index = postingsList[term].index
                    
            # this is the ONLY line in this function that is tfidf specific. Most likely, everything
            # else in this function should stay the same for all vectorizers
            vector[term] = postingsList[term].getTFIDF()

            synonymSet = set()

            savedSyns = index.getTerm(term).getSynonyms()
            if savedSyns != None:
                for score, term2 in savedSyns:
                    if term2 not in vector:
                        score = postingsList[term].getTFIDF() * score
                        vector[term2] = score  
                continue # discontinue the current loop iteration
                
            
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
                index.getTerm(term).setSynonyms(additionalTerms)
                
                for score, term2 in additionalTerms:
                    if term2 not in vector:
                        score = postingsList[term].getTFIDF() * score
                        vector[term2] = score
        
                
        return vector