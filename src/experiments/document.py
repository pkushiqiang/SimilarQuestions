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
    def __init__(self, path = None, text = None, docID = -1):
        self.postingsList = {}
        if text != None:
            self.processString(text)
            self.name = ""
            self.path = ""
        self.name = docID
        self.calculateMagnitude()
        
        
    def read(self):
        f = open(self.path)
        lines = f.readlines()
        for line in lines:
            self.processString(line)
        
    def processString(self, text):
        tokens = self._tokenizeLine(text)
        for token in tokens:
            self._addToPostingsList(token)
            #print token
        
            
    def _tokenizeLine(self, line):
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
    
    def _addToPostingsList(self, term):
        if term not in self.postingsList:
            self.postingsList[term] = Posting(term, self)
        self.postingsList[term].incrementOccurrences()
    
    def printPostingsList(self):
        print 'Magnitude: ', self.magnitude
        for term in self.postingsList:
            print self.postingsList[term].getOccurrences(), " : ", term
            
    def getName(self):
        return self.name
    
    def getPostingsList(self):
        return self.postingsList
    
    def getMagnitudeOfVector(self):
        if self.magnitude:
            return self.magnitude
        else:
            return self.calculateMagnitude()
    
    
    def calculateMagnitude(self):
        mag = 0.
        for i in self.postingsList:
            mag += self.postingsList[i].getOccurrences()**2
        mag = math.sqrt(mag)
        self.magnitude = mag
        return self.magnitude
        
            
if __name__ == '__main__':
    print "I'm running document.py"  
    print '\n\n'
    doc = Document('/Users/valentine/Dropbox/Classes/InfoStorageRetrieval/HW1/simpleFiles/testFile.txt')
    print doc.name
    doc.printPostingsList()
    
    print 
    print
    doc2 = Document(text='howdy i am stephanie. i pretty much rock. no big deal.')
    doc2.printPostingsList()
