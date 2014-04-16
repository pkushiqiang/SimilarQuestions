import sys
sys.path.append("/usr/local/lib/python2.7/site-packages/")
import nltk
from nltk.corpus import wordnet as wn


#for ss in wn.synsets('sky'):
   #print "ss", ss.lemma
   #for sim in ss.similar_tos():
      #print sim
      #print('    {}'.format(sim.name))

#vehicle = wn.synset('python.n.01')
#print vehicle.closure
#typesOfVehicles = list(set([w for s in vehicle.closure(lambda s:s.hyponyms()) for w in s.lemma_names]))        
#print typesOfVehicles
if len(wn.synsets('korea')) < 2:
   print wn.synsets('korea')[0].lemma_names


term = 'computer'
synonymSet = set()
for synset in wn.synsets(term):
   print synset.lemma_names
   for synonym in synset.lemma_names:
      if not term == synonym:
         synonymSet.add(synonym)
print synonymSet

synonymList = []
scoreList = []
resultList = []
term = wn.synsets(term)[0]
for synonym1 in synonymSet:
   syn = wn.synsets(synonym1)[0]
   sim_score = term.wup_similarity(syn)
   synonymList.append(synonym1)
   scoreList.append(sim_score)
print zip(scoreList, synonymList)   
resultList = sorted(zip(scoreList, synonymList), reverse=True)[:3]
print resultList
for x, y in resultList:
   print x
   print y


   