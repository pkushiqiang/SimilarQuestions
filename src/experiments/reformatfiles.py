import json
# make new file - be sure we're only indexing documents we have linked lists for

linkedFile = open('../../data/english_linked.txt')
linkedDocs = {}
for q in linkedFile:
    d = json.loads(q)
    linkedDocs[int(d['qid'])] = d['linked']
        

#open linkedlist
newlinkedlist = {}
for linked in linkedDocs:
    for q in linkedDocs[linked]:
        newlinkedlist[linked] = newlinkedlist.get(linked,[])
        newlinkedlist[linked] += [int(q)]
        
        newlinkedlist[int(q)] = newlinkedlist.get(int(q), [])
        if linked not in newlinkedlist[int(q)]:
            newlinkedlist[int(q)] += [linked]
            
linkedlist = newlinkedlist

for i in linkedlist:
    print type(i), i, linkedlist[i]

print len(linkedlist)

newlfile = open('../../data/full_english_linked.txt','w')
newlfile.write(json.dumps(linkedlist)+'\n')
#print json.dumps(linkedlist)

#open document of questions

questionsfile = open("../../data/english_questions_with_body.txt")
newqfile = open('../../data/relevant_english_questions_with_body.txt','w')

for q in questionsfile:
    qobj = json.loads(q)
    #print qobj['qid']
    if qobj['qid'] in linkedlist:
        newqfile.write(q)
    
newqfile.close()
newlfile.close()
