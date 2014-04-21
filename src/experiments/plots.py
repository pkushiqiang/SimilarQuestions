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
        if fullpath.endswith('.txt') and 'synonym3' not in fullpath:
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
    
    
'''for i in stats:
    #print i
    for j in stats[i]:
        #print '   ',j
        for k in stats[i][j]:
            #print '       ',k'''
                

#----------------------------------------------------------------------------------------------------
#plot all mean results (per dataset) with std. dev bars (everything)

for dataset in stats:
    v = 0
    rects = []
    vectorizers = []
    
    for vectorizer in sorted(stats[dataset]):
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
            #print N
            ind = np.arange(N)  # the x locations for the groups
            width = 0.15       # the width of the bars
            fig, ax = plt.subplots()
            plt.ylim(0,.8)    
            
            
        colors = ['#008ab8','#00b88a','#F2B844','#EA764B','#e24244', '#bf5d95', '#bf5d95']
        rects += [ax.bar(ind+(width*(v)), np.array(vMeans), width, color=colors[v], yerr=np.array(vStdev),error_kw=dict(ecolor='gray', lw=1, capsize=5, capthick=2))]
        
        v+=1
    
    # add some
    ax.set_ylabel('Scores')
    ax.set_title('Mean NDCG Scores For '+dataset+' Dataset')
    ax.set_xticks(ind+width)
    ax.set_xticklabels( ['Title Only', 'Body Only', 'Title+Body'] )
    #print [x[0] for x in rects]
    #print vectorizers
    ax.legend( [x[0] for x in rects] , vectorizers, loc='upper left' )
    
    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, ('%.2f'%height).lstrip('0'),
                    ha='center', va='bottom')
    
    for rect in rects:
        autolabel(rect)    
    
    plt.savefig('../../results/'+dataset+'_every-means_plot.pdf', transparent=True)
    


#plot all 'all' median results with std. dev bars grouped by vectorizer

plt.figure()


for dataset in stats:
    v = 0
    rects = []
    
    vMeans = []

    scopes = ['title','body','all']
    for i in range(len(scopes)):
        vMeans+= [[]]
        
    #print vMeans
    
    vLabels = sorted(stats[dataset].keys())
        
    for vectorizer in sorted(stats[dataset]):
        
        
        for scope in scopes:
            if scope in stats[dataset][vectorizer]:
                vMeans[scopes.index(scope)] += [float(stats[dataset][vectorizer][scope]['_NDCG_median'])]
            else:
                vMeans[scopes.index(scope)] += [0.]
        v+=1   
    
    N = len(vLabels)
    #print vMeans
    ind = np.arange(N)  # the x locations for the groups
    width = 0.25       # the width of the bars
    fig, ax = plt.subplots()    
    colors = ['#008ab8','#00b88a','#F2B844','#EA764B','#e24244', '#bf5d95']

    v=0
    for scope in scopes:    
        rects += [ax.bar(ind+(width*(v)), np.array(vMeans[scopes.index(scope)]), width, color=colors[v])]
        v+=1
        
        
    
    # add some
    ax.set_ylabel('Scores')
    ax.set_title('Median NDCG Scores For '+dataset+' Dataset')
    ax.set_xticks(ind+width)
    ax.set_xticklabels( vLabels )
    ax.legend( [x[0] for x in rects] , ['Title Only', 'Body Only', 'Title+Body'], loc='upper left' )
    
    plt.ylim(0,.8) 
    
    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, ('%.2f'%height).lstrip('0'),
                    ha='center', va='bottom')
    
    for rect in rects:
        autolabel(rect)    
    
    plt.savefig('../../results/'+dataset+'_all-medians_plot.pdf', transparent=True)
    

#plot all median results with std. dev bars grouped by vectorizer
plt.figure()

datasets = ['Python','English','Combined']
vMeans = []
vStdev = []
vectorizers = []
for vectorizer in sorted(stats['Python']):
    
    vectorizers += [vectorizer]
    
    vMeans += [[]]
    vStdev += [[]]    

#print vMeans
v = 0
rects = []
    
    
for vectorizer in vectorizers:  
    for dataset in datasets:
        if dataset in stats and vectorizer in stats[dataset] and 'all' in stats[dataset][vectorizer]:
            vMeans[vectorizers.index(vectorizer)] += [float(stats[dataset][vectorizer][scope]['_NDCG_mean'])]
            vStdev[vectorizers.index(vectorizer)] += [float(stats[dataset][vectorizer][scope]['_NDCG_standardDeviation'])]
        else:
            vMeans[vectorizers.index(vectorizer)] += [0.]
            vStdev[vectorizers.index(vectorizer)] += [0.]
                
#print vMeans    
    
N = len(datasets)
#print N
ind = np.arange(N)  # the x locations for the groups
width = 0.15       # the width of the bars
fig, ax = plt.subplots()
plt.ylim(0,.8)    
        
        
colors = ['#008ab8','#00b88a','#F2B844','#EA764B','#e24244', '#bf5d95']
    
v=0  

for i in range(len(vMeans)):
    #print 'vmeansi',vMeans[i]
    rects += [ax.bar(ind+(width*(v)), np.array(vMeans[i]), width, color=colors[v], yerr=np.array(vStdev[i]),error_kw=dict(ecolor='gray', lw=1, capsize=5, capthick=2))]
    v+=1

# add some
ax.set_ylabel('Scores')
ax.set_title('Mean NDCG Scores for Title+Body Across Datasets')
ax.set_xticks(ind+width)
ax.set_xticklabels( datasets )
ax.legend( [x[0] for x in rects] , vectorizers, loc='upper left' )

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, ('%.2f'%height).lstrip('0'),
                ha='center', va='bottom')

for rect in rects:
    autolabel(rect)


plt.savefig('../../results/all-means-by-dataset_plot.pdf', transparent=True)




#plot all 'all' medians
plt.figure()


for dataset in stats:
    v = 0
    rects = []
    vectorizers = []
    
    for vectorizer in sorted(stats[dataset]):
        vMeans = []
        vLabels = ['title','body','all']
        
        vectorizers += [vectorizer]
        
        for scope in vLabels:
            if scope in stats[dataset][vectorizer]:
                vMeans += [float(stats[dataset][vectorizer][scope]['_NDCG_median'])]
            else:
                vMeans += [0.]
            
    
        if v == 0:
            N = len(vLabels)
            #print N
            ind = np.arange(N)  # the x locations for the groups
            width = 0.15      # the width of the bars
            fig, ax = plt.subplots()
            plt.ylim(0,.8)    
            
            
        colors = ['#008ab8','#00b88a','#F2B844','#EA764B','#e24244', '#bf5d95', '#bf5d95']
        rects += [ax.bar(ind+(width*(v)), np.array(vMeans), width, color=colors[v])]
        
        v+=1
    
    # add some
    ax.set_ylabel('Scores')
    ax.set_title('Median NDCG Scores By Vectorizer For '+dataset+' Dataset')
    ax.set_xticks(ind+width)
    ax.set_xticklabels( ['Title Only', 'Body Only', 'Title+Body'] )
    #print [x[0] for x in rects]
    #print vectorizers
    ax.legend( [x[0] for x in rects] , vectorizers, loc='upper left' )
    
    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, ('%.2f'%height).lstrip('0'),
                    ha='center', va='bottom')
    
    for rect in rects:
        autolabel(rect)    
    
    plt.savefig('../../results/'+dataset+'_every-medians_plot.pdf', transparent=True)
    
    
    
#plot all 'all' percent @ rank 1
plt.figure()

for dataset in stats:
    v = 0

    rects = []
    vectorizers = []
    
    for vectorizer in sorted(stats[dataset]):
        vMeans = []
        vLabels = ['title','body','all']
        
        vectorizers += [vectorizer]
        
        for scope in vLabels:
            if scope in stats[dataset][vectorizer]:
                vMeans += [float(stats[dataset][vectorizer][scope]['_Percent@Rank1'])]
            else:
                vMeans += [0.]
            
    
        if v == 0:
            N = len(vLabels)
            #print N
            ind = np.arange(N)  # the x locations for the groups
            width = 0.15       # the width of the bars
            fig, ax = plt.subplots()
            plt.ylim(0)    
            
            
        colors = ['#008ab8','#00b88a','#F2B844','#EA764B','#e24244', '#bf5d95', '#bf5d95']
        #print '------------------------------'
        #print ind+width*(v+1)
        #print np.array(vMeans)
        #print width
        #print colors[v]
        #print np.array(vStdev)
        rects += [ax.bar(ind+(width*(v)), np.array(vMeans), width, color=colors[v])]
        
        v+=1
    
    # add some
    ax.set_ylabel('Scores')
    ax.set_title('Percentage of Similarity Rankings at Position 1 For '+dataset+' Dataset')
    ax.set_xticks(ind+width)
    ax.set_xticklabels( ['Title Only', 'Body Only', 'Title+Body'] )
    #print [x[0] for x in rects]
    #print vectorizers
    ax.legend( [x[0] for x in rects] , vectorizers, loc='upper left' )
    
    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, ('%.2f'%height).lstrip('0'),
                    ha='center', va='bottom')
    
    for rect in rects:
        autolabel(rect)    
    
    plt.savefig('../../results/'+dataset+'_every-Percent@Rank1_plot.pdf', transparent=True)
    


#plot all 'all' times


#plot all topRank results with std. dev bars grouped by vectorizer & across all datasets
plt.figure()

datasets = ['Python','English','Combined']
vMeans = []
vStdev = []
vectorizers = []
for vectorizer in sorted(stats['Python']):
    
    vectorizers += [vectorizer]
    
    vMeans += [[]]
    vStdev += [[]]    

#print vMeans
v = 0
rects = []
    
    
for vectorizer in vectorizers:  
    for dataset in datasets:
        if dataset in stats and vectorizer in stats[dataset] and 'all' in stats[dataset][vectorizer]:
            vMeans[vectorizers.index(vectorizer)] += [float(stats[dataset][vectorizer][scope]['_TopRank_median'])]
            vStdev[vectorizers.index(vectorizer)] += [float(stats[dataset][vectorizer][scope]['_TopRank_standardDeviation'])]
        else:
            vMeans[vectorizers.index(vectorizer)] += [0.]
            vStdev[vectorizers.index(vectorizer)] += [0.]
                
#print vMeans    
    
N = len(datasets)
#print N
ind = np.arange(N)  # the x locations for the groups
width = 0.15       # the width of the bars
fig, ax = plt.subplots()
        
        
colors = ['#008ab8','#00b88a','#F2B844','#EA764B','#e24244', '#bf5d95']
    
v=0  

for i in range(len(vMeans)):
    #print 'vmeansi',vMeans[i]
    #rects += [ax.bar(ind+(width*(v)), np.array(vMeans[i]), width, color=colors[v], yerr=np.array(vStdev[i]))]
    rects += [ax.bar(ind+(width*(v)), np.array(vMeans[i]), width, color=colors[v], yerr=0,error_kw=dict(ecolor='black', lw=1, capsize=5, capthick=1))]
    v+=1

# add some
ax.set_ylabel('Scores')
ax.set_title('Median Rank of First Similar Question for Title+Body Across Datasets')
ax.set_xticks(ind+width)
ax.set_xticklabels( datasets )
ax.legend( [x[0] for x in rects] , vectorizers, loc='upper left' )
plt.ylim(0,55)    

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

for rect in rects:
    autolabel(rect)

plt.savefig('../../results/all-median-topRanks-by-dataset_plot.pdf', transparent=True)



#plot all topRank results with std. dev bars grouped by vectorizer & across all datasets
plt.figure()

datasets = ['Python','English','Combined']
vMeans = []
vStdev = []
vectorizers = []
for vectorizer in sorted(stats['Python']):
    
    vectorizers += [vectorizer]
    
    vMeans += [[]]
    vStdev += [[]]    

#print vMeans
v = 0
rects = []
    
    
for vectorizer in vectorizers:  
    for dataset in datasets:
        if dataset in stats and vectorizer in stats[dataset] and 'all' in stats[dataset][vectorizer]:
            vMeans[vectorizers.index(vectorizer)] += [float(stats[dataset][vectorizer][scope]['_TopRank_mean'])]
            vStdev[vectorizers.index(vectorizer)] += [float(stats[dataset][vectorizer][scope]['_TopRank_standardDeviation'])]
        else:
            vMeans[vectorizers.index(vectorizer)] += [0.]
            vStdev[vectorizers.index(vectorizer)] += [0.]
                
#print vMeans    
    
N = len(datasets)
#print N
ind = np.arange(N)  # the x locations for the groups
width = 0.15       # the width of the bars
fig, ax = plt.subplots()
        
        
colors = ['#008ab8','#00b88a','#F2B844','#EA764B','#e24244', '#bf5d95']
    
v=0  

for i in range(len(vMeans)):
    #print 'vmeansi',vMeans[i]
    #rects += [ax.bar(ind+(width*(v)), np.array(vMeans[i]), width, color=colors[v], yerr=np.array(vStdev[i]))]
    rects += [ax.bar(ind+(width*(v)), np.array(vMeans[i]), width, color=colors[v], yerr=np.array(vStdev[i]),error_kw=dict(ecolor='gray', lw=1, capsize=5, capthick=2))]
    v+=1

# add some
ax.set_ylabel('Scores')
ax.set_title('Mean Rank of First Similar Question for Title+Body Across Datasets')
ax.set_xticks(ind+width)
ax.set_xticklabels( datasets )
ax.legend( [x[0] for x in rects] , vectorizers, loc='upper left' )
plt.ylim(0)    

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

for rect in rects:
    autolabel(rect)

plt.savefig('../../results/all-mean-topRanks-by-dataset_plot.pdf', transparent=True)





#plot all 'all' topRank results with std. dev bars grouped by vectorizer

plt.figure()


for dataset in stats:
    v = 0
    rects = []
    
    vMeans = []

    for i in range(len(stats[dataset])):
        vMeans+= [[]]
        
    #print vMeans
    scopes = ['title','body','all']
    
    vLabels = sorted(stats[dataset].keys())
        
    for vectorizer in sorted(stats[dataset]):
        
        
        for scope in scopes:
            if scope in stats[dataset][vectorizer]:
                vMeans[scopes.index(scope)] += [float(stats[dataset][vectorizer][scope]['_TopRank_median'])]
            else:
                vMeans[scopes.index(scope)] += [0.]
        v+=1   
    
    N = len(vLabels)
    #print vMeans
    ind = np.arange(N)  # the x locations for the groups
    width = 0.15       # the width of the bars
    fig, ax = plt.subplots()    
    colors = ['#008ab8','#00b88a','#F2B844','#EA764B','#e24244', '#bf5d95']

    v=0
    for scope in scopes:    
        rects += [ax.bar(ind+(width*(v)), np.array(vMeans[scopes.index(scope)]), width, color=colors[v])]
        v+=1
        
        
    
    # add some
    ax.set_ylabel('Scores')
    ax.set_title('Median Rank of First Similar Question For '+dataset+' Dataset')
    ax.set_xticks(ind+width)
    ax.set_xticklabels( vLabels )
    ax.legend( [x[0] for x in rects] , ['Title Only', 'Body Only', 'Title+Body'], loc='upper left' )
    
    plt.ylim(0)    
    
    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                    ha='center', va='bottom')
    
    for rect in rects:
        autolabel(rect)    
    
    plt.savefig('../../results/'+dataset+'_all-toprank-medians_plot.pdf', transparent=True)
    

    
#plot all topRank results with std. dev bars grouped by vectorizer & across all datasets
plt.figure()

datasets = ['Python','English','Combined']
vMeans = []
vStdev = []
vectorizers = []
for vectorizer in sorted(stats['Python']):
    
    vectorizers += [vectorizer]
    
    vMeans += [[]]   

#print vMeans
v = 0
rects = []
    
    
for vectorizer in vectorizers:  
    for dataset in datasets:
        if dataset in stats and vectorizer in stats[dataset] and 'all' in stats[dataset][vectorizer]:
            vMeans[vectorizers.index(vectorizer)] += [float(stats[dataset][vectorizer][scope]['_Percent@Rank1'])]
        else:
            vMeans[vectorizers.index(vectorizer)] += [0.]
                
#print vMeans    
    
N = len(datasets )
#print N
ind = np.arange(N)  # the x locations for the groups
print ind
width = 0.15       # the width of the bars
fig, ax = plt.subplots()
        
        
colors = ['#008ab8','#00b88a','#F2B844','#EA764B','#e24244', '#bf5d95']
    
v=0  

for i in range(len(vMeans)):
    #print 'vmeansi',vMeans[i]
    #rects += [ax.bar(ind+(width*(v)), np.array(vMeans[i]), width, color=colors[v], yerr=np.array(vStdev[i]))]
    rects += [ax.bar(ind+(width*(v)), np.array(vMeans[i]), width, color=colors[v], yerr=0,error_kw=dict(ecolor='black', lw=1, capsize=5, capthick=1))]
    v+=1

# add some
ax.set_ylabel('Scores')
ax.set_title('Mean % Questions With Similar Ranked 1 For Title+Body Across Datasets')
ax.set_xticks(ind+width)
ax.set_xticklabels( datasets )
ax.legend( [x[0] for x in rects] , vectorizers, loc='upper left' )
plt.ylim(0,.5)    

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, ('%.2f'%height).lstrip('0'),
                ha='center', va='bottom')

for rect in rects:
    autolabel(rect)

plt.savefig('../../results/all-percent@rank1-by-dataset_plot.pdf', transparent=True)

