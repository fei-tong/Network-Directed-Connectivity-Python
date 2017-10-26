'''
Created on Dec 22, 2012

@author: tongfei
'''
#!/usr/bin/python
#Filename:Func.py

import Polynomial
T_dic={} # The type of (key,value) is (str,Polynomial)
         # T: tower
def getPtl(s):
    '''Calculate polynomials of triangles and/or ladders
       ladder is one instance of stair
       
       The style of String s is 't i j' (t: triangle) or 's i' (s: ladder), where 'i' is an integer
       't i j': 'i' is the number of triangles; 
                'j' is the number of rightmost verticle lines
       's i': 'i' is the number of lattices in this ladder
    '''
    if isinstance(s,str)!=True:
      #print 'Error (In getPtl(s), Invalid arguments): %s' % str(s)
      #sys.exit()
      return False

    global T_dic #T_dic is the variable defined outside this function

    if s in T_dic:
      return T_dic[s]
    ss=s.split(' ') # current style 's/t i'
    if (ss[0]!='t' and ss[0]!='s') or (ss[0]=='t' and (len(ss)!=3 or ss[1].isalnum()!=True or ss[2].isalnum()!=True or int(ss[1])<0 or int(ss[2])<0)) or (ss[0]=='s' and (len(ss)!=2 or ss[1].isalnum()!=True or int(ss[1])<0)) :
      print 'Error (In getPtl(s), Invalid arguments): %s' % str(s)
      #sys.exit()
      return False

    if int(ss[1])==0: # i=0, 't 0 x' or 's 0', the polynomial of both is 1*p^i for triangle and 1*p^1 for ladder
      if ss[0]=='t':
        p=Polynomial.Polynomial(1,int(ss[2]))
        T_dic[s]=p
      elif ss[0]=='s':
        p=Polynomial.Polynomial(1,1)
        T_dic[s]=p
      return p
   
    if ss[0]=='t': #triangle
      st=ss[0]+' '+str(int(ss[1])-1)+' '+ss[2] # triangle: 't i-1 x'
      pt=Polynomial.Polynomial(1,1).plus(Polynomial.Polynomial(1,1).times(getPtl(st))).minus(Polynomial.Polynomial(1,2).times(getPtl(st)))
      T_dic[s]=pt
      return pt
    elif ss[0]=='s': #ladder
      sl=ss[0]+' '+str(int(ss[1])-1) #ladder: 's i-1'
      st='t'+' '+str(int(ss[1])-1)+' '+'1'# triangle: 't i-1 1'
      pl=Polynomial.Polynomial(1,int(ss[1])+1).plus(Polynomial.Polynomial(1,1).times(getPtl(sl))).minus(Polynomial.Polynomial(1,int(ss[1])+2).times(getPtl(st)))
      T_dic[s]=pl
      return pl
    return False
#endof getPtl(s)
