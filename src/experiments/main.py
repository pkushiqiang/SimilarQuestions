from experimentEngine import ExperimentEngine
from index import Index
from vectorizer_TFIDF import Vectorizer_TFIDF
from vectorizer_Synonym import Vectorizer_Synonym
from vectorizer_NV import Vectorizer_NV
from vectorizer import Vectorizer
import json
import sys

def main():
    
    
    if 'Python' in sys.argv:
        Vectorizer.dataset = 'Python'    
        questionsfilename = '../../data/relevant_python_questions_with_body.txt'
        linkedfilename = '../../data/full_python_linked.txt'
    if 'English' in sys.argv:
        Vectorizer.dataset = 'English'
        questionsfilename = '../../data/relevant_english_questions_with_body.txt'
        linkedfilename = '../../data/full_english_linked.txt'
    if 'Combined' in sys.argv:
        Vectorizer.dataset = 'Combined'   
        questionsfilename = '../../data/relevant_combined_questions_with_body.txt'    
        linkedfilename = '../../data/full_combined_linked.txt'

    questionsFile = open(questionsfilename)
    
    questions = []
    
    for q in questionsFile:
        questions += [json.loads(q)]


    if 'n-gram' in sys.argv:
        gram = int(sys.argv[-1])
    else:
        gram = 1
    index = Index(questions,gram)
    
    
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
        
        if 'nounverb' in sys.argv:
            nounverb = Vectorizer_NV()  
            vectorizers[nounverb.getName()] = nounverb
        if 'nounverb-title' in sys.argv:
            nounverb = Vectorizer_NV('title')
            vectorizers[nounverb.getName()] = nounverb
        if 'nounverb-body' in sys.argv:
            nounverb = Vectorizer_NV('body')
            vectorizers[nounverb.getName()] = nounverb 
            
        if 'n-gram' in sys.argv:
            if sys.argv[-1].isdigit():
                grams = int(sys.argv[-1])
            else:
                grams = 2 
            ngram = Vectorizer_NGram(grams)  
            vectorizers[ngram.getName()] = synonym        
        if 'n-gram-title' in sys.argv:
            if sys.argv[-1].isdigit():
                grams = int(sys.argv[-1])
            else:
                grams = 2 
            ngram = Vectorizer_NGram(grams,'title')  
            vectorizers[ngram.getName()] = synonym  
        if 'n-gram-body' in sys.argv:
            if sys.argv[-1].isdigit():
                grams = int(sys.argv[-1])
            else:
                grams = 2 
            ngram = Vectorizer_NGram(grams,'body')  
            vectorizers[ngram.getName()] = synonym                

    else: # if we want to run all of them
        tfidf = Vectorizer_TFIDF()
        vectorizers[tfidf.getName()] = tfidf
        tfidf = Vectorizer_TFIDF('title')
        vectorizers[tfidf.getName()] = tfidf
        tfidf = Vectorizer_TFIDF('body')
        vectorizers[tfidf.getName()] = tfidf
        
    linkedFile = open(linkedfilename)
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
