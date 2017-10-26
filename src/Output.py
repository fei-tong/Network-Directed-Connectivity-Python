'''
Created on Jan 2, 2013

@author: tongfei
'''
import os
import cPickle
#!/usr/bin/python
#Filename:Output.py

PdicFile='../data/Pol_dic.data' #data file used by this program
P_dic={}
if os.path.isfile(PdicFile):
    f_Pdic=file(PdicFile)
    P_dic=cPickle.load(f_Pdic)
    f_Pdic.close()

output=[]

layers=10
lattices=10    
for i in range(1,layers+1):
    for j in range(i,lattices+1):
        l_i=i#exact_i
        l_j=j#exact_i
        name=str(l_i)+'*'+str(l_j)
        print
        print name
        if name in P_dic:
            pol=P_dic[name][1]
            output.append(pol)

print output