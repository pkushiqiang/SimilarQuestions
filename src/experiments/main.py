from experimentEngine import ExperimentEngine
from index import Index
from vectorizer_TFIDF import Vectorizer_TFIDF
from vectorizer_Synonym import Vectorizer_Synonym
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

        if 'synonym' in sys.argv:
            if sys.argv[-1].isdigit():
                num_syn = sys.argv[-1]
            else:
                num_syn = 2 
            synonym = Vectorizer_Synonym(num_syn)  
            vectorizers[synonym.getName()] = synonym                
        if 'synonym-title' in sys.argv:
            if sys.argv[-1].isdigit():
                num_syn = sys.argv[-1]
            else:
                num_syn = 2 
            synonym = Vectorizer_Synonym(num_syn, 'title')  
            vectorizers[synonym.getName()] = synonym     
        if 'synonym-body' in sys.argv:
            if sys.argv[-1].isdigit():
                num_syn = sys.argv[-1]
            else:
                num_syn = 2 
            synonym = Vectorizer_Synonym(num_syn, 'body')  
            vectorizers[synonym.getName()] = synonym             

    else: # if we want to run all of them
        tfidf = Vectorizer_TFIDF()
        vectorizers[tfidf.getName()] = tfidf
        tfidf = Vectorizer_TFIDF('title')
        vectorizers[tfidf.getName()] = tfidf
        tfidf = Vectorizer_TFIDF('body')
<<<<<<< HEAD
        vectorizers[tfidf.getName()] = tfidf

=======
        #vectorizers[tfidf.getName()] = tfidf
        
>>>>>>> FETCH_HEAD
        
    linkedFile = open('../../data/full_python_linked.txt')
    f = linkedFile.read()
    #print f
    linkedDocs = makeIntIndexes(json.loads(f))
        
    #print "linkedDocs", linkedDocs 
    engine = ExperimentEngine(index, linkedDocs, vectorizers)
    
    stats = engine.runExperiments()
    

def makeIntIndexes(dictionary):
    newd = {}
    for i in dictionary:
        newd[int(i)] = dictionary[i]
    return newd

if __name__ == '__main__':     
    main()