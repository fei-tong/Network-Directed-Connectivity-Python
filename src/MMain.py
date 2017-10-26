'''
Created on Dec 22, 2012

@author: tongfei
'''
#!/usr/bin/python
#Filename:Main.py
import Tower
import cPickle
import os
#import decimal

#def frange(x, y, jump):
#  x1=decimal.Decimal(str(x))
#  y1=decimal.Decimal(str(y))
#  jump1=decimal.Decimal(str(jump))
#  while x1 <= y1:
    #print x1
#    yield x1
#    x1 += jump1

#PdicFile='data/Pol_dic.data' #data file used by this program
#P_dic={}
#if os.path.isfile(PdicFile):
#  f_Pdic=file(PdicFile)
#  P_dic=cPickle.load(f_Pdic)
#  f_Pdic.close()
#polFile='result/Result.txt'   #get result in this file

while (True):
  layers=raw_input('Please enter the number of layers:')
  lattices=raw_input('Please enter the number of lattices on each layer:')
  print
  print "%s * %s" % (layers,lattices)
  print
  T=Tower.Tower([0,0],[[0,int(lattices)] for i in range(0,int(layers))],0)
  p=T.getPolynomial()
  #print p.computePol(0.99)
  s=p.toString()
  print s
  print

  name=layers+'*'+lattices

  #pol=[p.computePol(i) for i in frange(0.00,1.00,0.01)]
  #P_dic[name]=[s,pol]
#  if name in P_dic:
#    pol=P_dic[name][1]
#  else:
#    pol=[p.computePol(i) for i in frange(0.0,1.01,0.01)]
#    P_dic[name]=[s,pol]  
#  print pol
  print

  c=raw_input('Do you want to continue [(Y/y) or (N/n)]?')
  if c=='N' or c=='n':
    break
  print

#f_Pdic=file(PdicFile,'w')
#cPickle.dump(P_dic,f_Pdic)
#f_Pdic.close()

#f_pol=file(polFile,'w')
#for name,result in P_dic.items():
#  f_pol.write(name)
#  f_pol.write('\n\n')
#  f_pol.write(result[0])
#  f_pol.write('\n\n')
#  f_pol.write(str(result[1]))
#  f_pol.write('\n\n\n')
#f_pol.close()

print
print "Bye..."


