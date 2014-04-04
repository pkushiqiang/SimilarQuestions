from experimentEngine import ExperimentEngine
from index import Index
from vectorizer_TFIDF import Vectorizer_TFIDF
import json

def main():
    questionsFile = open('../../data/python_questions_abridged.txt')
    questions = []
    
    for q in questionsFile:
        questions += [json.loads(q)]
    
    index = Index(questions)
    
    vectorizers = {}
    tfidf = Vectorizer_TFIDF()
    
    vectorizers[tfidf.getName()] = tfidf
    
    
    engine = ExperimentEngine(index, vectorizers)
    
    stats = engine.runExperiments()
    



if __name__ == '__main__':     
    main()