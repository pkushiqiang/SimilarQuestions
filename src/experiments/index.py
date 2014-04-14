#index 'class'

#in index?

#add term to index (add optional parameter to add a post to that term)

#add post to index for term

#getPostsForTerm
from term import Term
from document import Document
from posting import Posting
import os
import math


class Index:   
    
    def __init__(self, questions):
        self.documents = {}
        self.index = {}
        
        Posting.index = self

        #questions is formatted as a list of dictionaries with attributes 'docID', 'text' and 'cluster'
        for d in range(len(questions)):
            #print questions[d]
            doc = Document(title=questions[d]['title'],body=questions[d]['body'], docID = questions[d]['qid'])
            self.documents[doc.getName()] = doc
            #print 'loading', doc.getName(), '...'
            #doc.printPostingsList()
            pl = doc.getPostingsList()
            for term in pl:
                self.addTerm(term,pl[term])
        self.setIDFForAll()

    def addTerm(self, term, posting = None):
        firstLetter = term[0]
        if firstLetter not in self.index:
            self.index[firstLetter] = {}
        if not self.inIndex(term):
            self.index[firstLetter][term] = Term(term)
        if (posting != None):
            self.index[firstLetter][term].addPosting(posting)
            
    def printIndex(self):
        for letter in sorted(self.index):
            print letter," : "
            for term in self.index[letter]:
                print "   ",term," : ",self.index[letter][term].getDocumentFrequency()
            
    def inIndex(self, term):
        firstLetter = term[0]
        if firstLetter not in self.index:
            return False
        if term not in self.index[firstLetter]:
            return False
        return True
    
    def getPostingsForTerm(self, term):
        if self.inIndex(term):
            return self.index[term[0]][term].getPostingsList()
        else:
            return []
    
    def getTerm(self, term):
        if self.inIndex(term):
            return self.index[term[0]][term]
        else:
            return None
    
    def getDocument(self, name):
        if name in self.documents:
            return self.documents[name]
        else:
            return None
        
    def getIDF(self, term):
        #print len(self.documents)
        return math.log10(float(len(self.documents))/float(self.getTerm(term).getDocumentFrequency()))
    
    def getNumDocuments(self):
        return len(self.documents)
    
    def getNumTerms(self):
        terms = 0
        for i in self.index:
            terms += len(self.index[i])
        return terms
    
    def setIDFForAll(self):
        for letter in self.index:
            for term in self.index[letter]:
                self.index[letter][term].setIDF(self.getIDF(term))
    
if __name__ == '__main__':     
    i = Index('')
    i.addTerm("hello",7)
    i.addTerm("hello",8)
    i.addTerm('world',145)
    i.printIndex();