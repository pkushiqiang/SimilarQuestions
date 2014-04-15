import sys
sys.path.append("/usr/local/lib/python2.7/site-packages/")
import nltk
from nltk.corpus import wordnet as wn


#for ss in wn.synsets('python'):
   #print ss.lemma_names
   #for sim in ss.similar_tos():
      #sim
      #print('    {}'.format(sim.name))

vehicle = wn.synset('python.n.01')
print vehicle
typesOfVehicles = list(set([w for s in vehicle.closure(lambda s:s.hyponyms()) for w in s.lemma_names]))        
print typesOfVehicles
      