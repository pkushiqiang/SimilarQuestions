from vectorizer import Vectorizer

class Vectorizer_TFIDF(Vectorizer):
    
    # the only thing you'd change in this function is the string 'name' of the vectorizer. 
    # here the 'name' is 'TFIDF'
    def __init__(self,scope='all'):
        super(type(self),self).__init__('TFIDF'+'-'+scope)
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
            
            
            # this is the ONLY line in this function that is tfidf specific. Most likely, everything
            # else in this function should stay the same for all vectorizers
            vector[term] = postingsList[term].getTFIDF()
            
        return vector