#document

# name
# associated postings
# vector cardinality

# calculate vector cardinality


# read the document
# tokenize
# get word lists

# read document
import string
from posting import Posting
import math

class Document:
    cluster = None
    docID = -1
    # send in either path or text, but not both.
    def __init__(self, path = None, body = None, title = None, docID = -1, gram=1):
        self.postingsListTitle = {}
        self.postingsListBody = {}
        self.gram = gram

        if title != None and body != None:
            self.processTitleString(title)
            self.processBodyString(body)
            self.name = ""
            self.path = ""
        self.name = docID     
        
    def read(self):
        f = open(self.path)
        lines = f.readlines()
        for line in lines:
            self.processString(line)
        
    def processTitleString(self, text):
        tokens = self._tokenizeLine(text)
        for token in tokens:
            self._addToPostingsListTitle(token)
            #print token
    
    def processBodyString(self, text):
        tokens = self._tokenizeLine(text)
        for token in tokens:
            self._addToPostingsListBody(token)
            #print token
    
    def _tokenizeLine(self, line):
        toekens = self._tokenizeOneGram(line)
        if self.gram == 1:
            return toekens
        result = []
  
        if   len(toekens) <  self.gram :
            return result
        
        for i in range(0,len(toekens)-self.gram+1):
            token = toekens[i]
            for j in range(1,self.gram) :
                token += " " + toekens[i+j]
            result.append(token)
        
        return toekens + result
            
    def _tokenizeOneGram(self, line):
        line = line.strip()
        line = line.lower()

        line = line.split()
        line = filter(lambda a: 'http' not in a or '.co' not in a or '/' not in a, line)
        line = " ".join(line)
        
        newl = ''
        for i in line:
            if i.isalnum() or i == '#' or i == '@':
                newl += i
            else:
                newl += ' '
        
        line = newl
        
        line= line.split()
        
        #we don't want to count the empty string or any other non alphanumeric string as a term
        line = filter(lambda a: a.isalnum(), line) 
         
        
        return line
    
    def _addToPostingsListTitle(self, term):
        if term not in self.postingsListTitle:
            self.postingsListTitle[term] = Posting(term, self)
        self.postingsListTitle[term].incrementOccurrences()
        
    def _addToPostingsListBody(self, term):
        if term not in self.postingsListBody:
            self.postingsListBody[term] = Posting(term, self)
        self.postingsListBody[term].incrementOccurrences()    
    
    def printPostingsListTitle(self):
        print 'Magnitude: ', self.magnitude
        for term in self.postingsListTitle:
            print self.postingsListTitle[term].getOccurrences(), " : ", term
            
    def getName(self):
        return self.name
    
    def getPostingsList(self):
        combined = {}
        for term in set(self.postingsListTitle.keys()+self.postingsListBody.keys()):
            if term in self.postingsListTitle and term in self.postingsListBody:
                occurrences = self.postingsListTitle[term].getOccurrences() + self.postingsListBody[term].getOccurrences()
                combined[term] = Posting(term,self,occurrences)
            elif term in self.postingsListTitle:
                combined[term] = self.postingsListTitle[term]
            elif term in self.postingsListBody:
                combined[term] = self.postingsListBody[term]
        return combined
    
    def getPostingsListTitle(self):
        return self.postingsListTitle

    def getPostingsListBody(self):
        return self.postingsListBody
            
        
            
if __name__ == '__main__':  
    doc = Document(title='juicy juice is by far the best!',body='hello my name is stephanie and i love juicy juice.',gram=3)
    print doc.getPostingsListBody()
    