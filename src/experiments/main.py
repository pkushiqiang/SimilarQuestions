from experimentEngine import ExperimentEngine
from index import Index
from vectorizer_TFIDF import Vectorizer_TFIDF
import json
import sys

def main():
    
    questionsFile = open('../../data/relevant_python_questions_with_body.txt')
    questions = []
    
    for q in questionsFile:
        questions += [json.loads(q)]
    
    index = Index(questions)
    
    vectorizers = {}
    # if we want to call only some of them (from commandline)...
    if len(sys.argv) > 1:
        if 'tfidf' in sys.argv:
            tfidf = Vectorizer_TFIDF()  
            vectorizers[tfidf.getName()] = tfidf
        if 'tfidf-title' in sys.argv:
            tfidf = Vectorizer_TFIDF('title')
            vectorizers[tfidf.getName()] = tfidf
        if 'tfidf-body' in sys.argv:
            tfidf = Vectorizer_TFIDF('body')
            vectorizers[tfidf.getName()] = tfidf
    else: # if we want to run all of them
        tfidf = Vectorizer_TFIDF()
        vectorizers[tfidf.getName()] = tfidf
        tfidf = Vectorizer_TFIDF('title')
        vectorizers[tfidf.getName()] = tfidf
        tfidf = Vectorizer_TFIDF('body')
        #vectorizers[tfidf.getName()] = tfidf
        
        
    linkedFile = open('../../data/full_python_linked.txt')
    f = linkedFile.read()
    #print f
    linkedDocs = makeIntIndexes(json.loads(f))
        
    #print linkedDocs 
    engine = ExperimentEngine(index, linkedDocs, vectorizers)
    
    stats = engine.runExperiments()
    

def makeIntIndexes(dictionary):
    newd = {}
    for i in dictionary:
        newd[int(i)] = dictionary[i]
    return newd

if __name__ == '__main__':     
    main()