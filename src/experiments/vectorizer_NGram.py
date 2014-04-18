from vectorizer import Vectorizer

class Vectorizer_NGram(Vectorizer):
    
    # the only thing you'd change in this function is the string 'name' of the vectorizer. 
    # here the 'name' is 'TFIDF'
    def __init__(self, grams=1,scope='all'):
        super(type(self),self).__init__('NGram-'+str(grams)+'-'+scope)
        self.grams = grams
        self.scope = scope
    
    def calculateVector(self, document):
        postingslist = None

        if self.scope == 'title':
            postingsList = document.getPostingsListTitle()
        elif self.scope == 'body':
            postingsList = document.getPostingsListBody()
        else:
            postingsList = document.getPostingsList()
            
        vector = {}
        for term in postingsList: #terms are actually ngrams
            
            
            vector[term] = postingsList[term].getTFIDF()

        return vector