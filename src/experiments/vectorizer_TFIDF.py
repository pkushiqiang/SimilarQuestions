from vectorizer import Vectorizer

class Vectorizer_TFIDF(Vectorizer):
    
    # the only thing you'd change in this function is the string 'name' of the vectorizer. 
    # here the 'name' is 'TFIDF'
    def __init__(self):
        super(type(self),self).__init__('TFIDF')
    
    # this is the function that creates the vector. Since the TFIDF code is already written into
    # the document/posting objects, this is a very simple function. others will necessarily be more complex.
    def calculateVector(self, document):
        postingsList = document.getPostingsList()
        vector = {}
        for term in postingsList:
            
            
            # this is the ONLY line in this function that is tfidf specific. Most likely, everything
            # else in this function should stay the same for all vectorizers
            vector[term] = postingsList[term].getTFIDF()
            
        return vector