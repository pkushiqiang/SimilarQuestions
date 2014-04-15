from experimentEngine import ExperimentEngine
from index import Index
from vectorizer_TFIDF import Vectorizer_TFIDF
import json
import sys

def main():
    
    questionsFile = open('../../data/python_questions_with_body_abridged.txt')
    questions = []
    
    for q in questionsFile:
        questions += [json.loads(q)]

    index = Index(questions)
    
    vectorizers = {}
    synonym = False
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
        if '-s' in sys.argv:
            synonym = True
            if sys.argv[sys.argv.index('-s')+1].isdigit():
                num_syn = sys.argv[sys.argv.index('-s')+1]
                print num_syn
            else:
                num_syn = 2
    else: # if we want to run all of them
        tfidf = Vectorizer_TFIDF()
        vectorizers[tfidf.getName()] = tfidf
        tfidf = Vectorizer_TFIDF('title')
        vectorizers[tfidf.getName()] = tfidf
        tfidf = Vectorizer_TFIDF('body')
        vectorizers[tfidf.getName()] = tfidf
        
    linkedFile = open('../../data/python_linked.txt')
    linkedDocs = {}
    for q in linkedFile:
        d = json.loads(q)
        linkedDocs[d['qid']] = d['linked']
        
    #print "linkedDocs", linkedDocs 
    engine = ExperimentEngine(index, linkedDocs, vectorizers)
    
    stats = engine.runExperiments()
    



if __name__ == '__main__':     
    main()