#holds document object
#holds (at the very least) term count within that document
#holds term
import math

class Posting:
    index = None
    
    def __init__(self, term, document, occurrences=0.):
        self.term=term
        self.document = document
        self.occurrences = occurrences
        
    def incrementOccurrences(self):
        self.occurrences += 1
        
    def getOccurrences(self):
        return self.occurrences
    
    def setOccurrences(self, occurrences):
        self.occurrences = occurrences
        
    def getDocument(self):
        return self.document
    
    def getTerm(self):
        return self.term
    
    def getTF(self):
        if math.log10(self.getOccurrences()) < 0:
            return 0
        return 1 + math.log10(self.getOccurrences())
        
    def getTFIDF(self):
        return self.getTF() * Posting.index.getTerm(self.term).getIDF()
        
    # for debugging
    def printPosting(self):
        print "Posting: "
        print "  Term:        ", self.term
        print "  Document:    ", self.document
        print "  Occurrences: ", self.occurrences