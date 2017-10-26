'''
Created on Dec 22, 2012

@author: tongfei
'''
#!/usr/bin/python
#Filename:Main.py

#From system
import cPickle
import os
import time
#import Func

#From self-definition
import Tower
import FReal


def computePol(fp,p):
    if fp.deg<0:
        return 0
    if fp.deg==0:
        return float(FReal.FReal(repr(fp.coef[0])).toString())
    if fp.deg==1:
        pol=FReal.FReal(repr(fp.coef[1]))*p
        if fp.coef[0]!=0:
            return float((pol+FReal.FReal(repr(fp.coef[0]))).toString())
        else:
            return float(pol.toString())
    pol=FReal.FReal(repr(fp.coef[fp.deg]))*p**fp.deg
    for i in range(fp.deg-1,-1,-1):
        if fp.coef[i]==0:
            continue
        pol=pol+FReal.FReal(repr(fp.coef[i]))*p**i      
    return float(pol.toString())

def computePol2(fp,p):
    if fp.deg<0:
        return 0
    if fp.deg==0:
        return float(fp.coef[0])
    if fp.deg==1:
        pol=fp.coef[1]*p
        if fp.coef[0]!=0:
            return float(pol+fp.coef[0])
        else:
            return float(pol)
    pol=fp.coef[fp.deg]*p**fp.deg
    for i in range(fp.deg-1,-1,-1):
        if fp.coef[i]==0:
            continue
        pol=pol+fp.coef[i]*p**i      
    return float(pol)

def frange(x, y, jump):
    while x <= y:
        #print x
        yield x
        x += jump
    
print
print "Loading..."
print time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))
print
data_dir = '../data/'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
TdicFile=data_dir+'MNPoly_dic.data'  #data file used by this program
MNPoly_dic={} # The polynomial of M*N lattices
if os.path.isfile(TdicFile):
    f_Tdic=file(TdicFile)
    MNPoly_dic=cPickle.load(f_Tdic)
    f_Tdic.close()



layers=2
lattices=2
#exact_i=5
#exact_j=5

for i in range(1,layers+1):
    for j in range(1,lattices+1):
        l_i=i#exact_i
        l_j=j#exact_j
        name=str(l_i)+'*'+str(l_j)
        print name
        
        if name in MNPoly_dic:
            p=MNPoly_dic[name]
        else:
            T=Tower.Tower([0,0],[[0,int(l_j)] for k in range(0,int(l_i))],0)
            p=T.getPolynomial()
            MNPoly_dic[name]=p
        s=p.toString()
        print s
        print

f_Tdic=file(TdicFile,'w')
cPickle.dump(MNPoly_dic,f_Tdic)
f_Tdic.close()

print time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))

print "****************************************************************************************************************************************************************************************"
PdicFile=data_dir+'Pol_dic.data' #data file used by this program
P_dic={}
if os.path.isfile(PdicFile):
    f_Pdic=file(PdicFile)
    P_dic=cPickle.load(f_Pdic)
    f_Pdic.close()
result_dir = '../result/'
if not os.path.exists(result_dir):
    os.makedirs(result_dir)
polFile=result_dir+'Result.txt'   #get result in this file

for i in range(1,layers+1):
    for j in range(1,lattices+1):
        l_i=i#exact_i
        l_j=j#exact_i
        name=str(l_i)+'*'+str(l_j)
        print
        print name
        
        p=MNPoly_dic[name]
        pol=[computePol(p,FReal.FReal(str(k))) for k in frange(0.0,1.01,0.01)]
#        pol=computePol(p,FReal.FReal('0.95'))
#        pol1=computePol(p,FReal.FReal('0.97'))
        
#        pol1=[computePol2(p,k) for k in frange(0.0,1.01,0.01)]
        #pol=computePol2(p,0.97)
        s=MNPoly_dic[name].toString()
        P_dic[name]=[s,pol]  
        print pol
#        print pol1
        print

f_pol=file(polFile,'w')
for name,result in P_dic.items():
    f_pol.write(name)
    f_pol.write('\n\n')
    f_pol.write(result[0])
    f_pol.write('\n\n')
    f_pol.write(str(result[1]))
    f_pol.write('\n\n\n')
f_pol.close()

f_Pdic=file(PdicFile,'w')
cPickle.dump(P_dic,f_Pdic)
f_Pdic.close()

print time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))
print
print "Bye..."

