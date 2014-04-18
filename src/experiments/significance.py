import numpy as np
from scipy import stats as st
import matplotlib.pyplot as plt
import json




''' we want plots for...

all 'all' mean results with std. dev bars
all mean results with std. dev bars (everything)
all 'all' medians
all 'all' percent @ rank 1
all 'all' times

'''


#loop through the files in ../../results
import os, os.path

allstats = {}


for root, _, files in os.walk('../../results'):
    for f in files:
        fullpath = os.path.join(root, f)
        print fullpath
        if fullpath.endswith('.txt'):
            stats = open(fullpath).readline()
            if len(stats) > 0:
                #decode the first line of each file
                stats = json.loads(stats)
                allstats.update(stats)
                

stats = {}
for i in sorted(allstats):
    s = i.split('-')
    s = [' '.join(s[0:-2]),s[-2], s[-1]]
    dataset = s[-1]
    vectorizer = s[0]
    scope = s[1]
    stats[dataset] = stats.get(dataset, {})
    stats[dataset][vectorizer] = stats[dataset].get(vectorizer,{})
    stats[dataset][vectorizer][scope] = allstats[i]
    
    
for i in stats:
    print i
    for j in stats[i]:
        print '   ',j
        for k in stats[i][j]:
            print '       ',k
            
print '\n\n------ toprank ------'            
for i in sorted(allstats):
    for j in sorted(allstats):
        if (('Python' in i and 'Python' in j) or ('English' in i and 'English' in j) or ('Combined' in i and 'Combined' in j)) and 'all' in i and 'all' in j:
            t,p = st.ttest_ind(allstats[i]['topRank'],allstats[j]['topRank'])
            if p<=.05:
                print i,j,(p<=.05),p
                
print '\n\n------ ndcg ------'            
for i in sorted(allstats):
    for j in sorted(allstats):
        if (('Python' in i and 'Python' in j) or ('English' in i and 'English' in j) or ('Combined' in i and 'Combined' in j)) and 'all' in i and 'all' in j:
            t,p = st.ttest_ind(allstats[i]['NDCG'],allstats[j]['NDCG'])
            if p<=.05:
                print i,j,(p<=.05),p                