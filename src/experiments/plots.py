#!/usr/bin/env python
# a bar plot with errorbars
import numpy as np
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
                
for i in sorted(allstats):
    print i, allstats[i]['_NDCG_mean']
    

stats = {}
for i in sorted(allstats):
    s = i.split('-')
    s = [' '.join(s[0:-2]),s[-2], s[-1]]
    dataset = s[-1]
    vectorizer = s[0]
    scope = s[1]
    print dataset, vectorizer, scope
    stats[dataset] = stats.get(dataset, {})
    print stats
    stats[dataset][vectorizer] = stats[dataset].get(vectorizer,{})
    stats[dataset][vectorizer][scope] = allstats[i]
    print s[2], s[0], s[1]
    
    
for i in stats:
    print i
    for j in stats[i]:
        print '   ',j
        for k in stats[i][j]:
            print '       ',k
                

#----------------------------------------------------------------------------------------------------
#plot all mean results (per dataset) with std. dev bars (everything)
v = 0
for dataset in stats:
    rects = []
    vectorizers = []
    
    for vectorizer in stats[dataset]:
        vMeans = []
        vStdev = []
        vLabels = ['title','body','all']
        
        vectorizers += [vectorizer]
        
        for scope in vLabels:
            if scope in stats[dataset][vectorizer]:
                vMeans += [float(stats[dataset][vectorizer][scope]['_NDCG_mean'])]
                vStdev += [float(stats[dataset][vectorizer][scope]['_NDCG_standardDeviation'])]
            else:
                vMeans += [0.]
                vStdev += [0.]
            
    
        if v == 0:
            N = len(vLabels)
            print N
            ind = np.arange(N)  # the x locations for the groups
            width = 0.20       # the width of the bars
            fig, ax = plt.subplots()
            
        colors = ['#00b88a','#F2B844','#EA764B','#E23351']
        print '------------------------------'
        print ind+width*(v+1)
        print np.array(vMeans)
        print width
        print colors[v]
        print np.array(vStdev)
        rects += [ax.bar(ind+(width*(v)), np.array(vMeans), width, color=colors[v], yerr=np.array(vStdev))]
        
        v+=1
    
    # add some
    ax.set_ylabel('Scores')
    ax.set_title('Mean NDCG Scores For ')
    ax.set_xticks(ind+width)
    ax.set_xticklabels( ['Title Only', 'Body Only', 'All Text'] )
    print [x[0] for x in rects]
    print vectorizers
    ax.legend( [x[0] for x in rects] , vectorizers )
    
    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                    ha='center', va='bottom')
    
    for r in rects:
        autolabel(r)
    
    plt.savefig('../../results/python_ndcg_plot.png', transparent=True)
    


#plot all 'all' mean results with std. dev bars

#plot all 'all' medians

#plot all 'all' percent @ rank 1

#plot all 'all' times