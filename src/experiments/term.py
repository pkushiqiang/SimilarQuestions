# term

# hold string of term
# hold postings list
# hold df

class Term:
    
    def __init__(self, term):
        self.term = term
        self.postingsList = []
        self.idf = 0
        
    def getPostingsList(self):
        return self.postingsList
    
    # right now, we're just going to return the count of postings, but this 
    #   will need to change if we choose to complicate the index by including
    #   positions of words in the document
    def getDocumentFrequency(self):
        return len(self.postingsList)
    
    
    def addPosting(self, posting):
        #eventually, we might want to make this more complex
        self.postingsList += [posting]
        return True 
    
    def setIDF(self, idf): #this is actually df
        self.idf = idf
        
    def getIDF(self): #this is actually df
        return self.idf