from experimentEngine import ExperimentEngine
from index import Index
from vectorizer_TFIDF import Vectorizer_TFIDF
import json

def main():
    questionsFile = open('../../data/python_questions_with_body_abridged.txt')
    questions = []
    
    for q in questionsFile:
        questions += [json.loads(q)]
    
    index = Index(questions)
    
    vectorizers = {}
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
        
    #print linkedDocs 
    engine = ExperimentEngine(index, linkedDocs, vectorizers)
    
    stats = engine.runExperiments()
    



if __name__ == '__main__':     
    main()