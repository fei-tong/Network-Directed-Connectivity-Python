'''
Created on Dec 22, 2012

@author: tongfei
'''
#!/usr/bin/python
#Filename:polynomial.py

class Polynomial:
  '''Represents a Polynomial'''
#  def __init__(self,coef):
#    '''Initializes a Polynomial with coefficient 
#    (the maximum power of this Polynomial)'''
#    self.coef=coef[:]
#    self.deg=self.degree()

  def __init__(self,a,b):
    '''Initializes a Polynomial a*p^b'''
    self.coef=[0 for i in range(0,b+1)]
    self.coef[b]=a
    self.deg=b

  def degree(self):
    '''calculate the degree of this Polynomial'''
    d=-1
    for i in range(len(self.coef)-1,-1,-1):
      if self.coef[i]==0 and i!=0:
        del self.coef[i]
      else:
        d=i
        break
    return d

  def plus(self,b):
    '''b is a Polynomial. Return Polynomial: (self+b)'''
    #c=[0 for i in range(0,max(self.deg,b.deg)+1)]
    c=Polynomial(0,max(self.deg,b.deg))
    for i in range(0,self.deg+1):
      c.coef[i]+=self.coef[i]
    for i in range(0,b.deg+1):
      c.coef[i]+=b.coef[i]
    c.deg=c.degree()
    return c

  def minus(self,b):
    '''b is a Polynomial. Return Polynomial: (self-b)'''
    #c=[0 for i in range(0,max(self.deg,b.deg)+1)]
    c=Polynomial(0,max(self.deg,b.deg))
    for i in range(0,self.deg+1):
      c.coef[i]+=self.coef[i]
    for i in range(0,b.deg+1):
      c.coef[i]-=b.coef[i]
    c.deg=c.degree()
    return c

  def times(self,b):
    '''b is a Polynomial. Return Polynomial: (self*b)'''
    c=Polynomial(0,self.deg+b.deg)
    for i in range(0,self.deg+1):
      for j in range(0,b.deg+1):
        c.coef[i+j]+=self.coef[i]*b.coef[j]
    c.deg=c.degree()
    return c

  def equal(self,b):
    '''b is a Polynomial. Do a and b represent the same polynomial?'''
    if self.deg != b.deg:
      return False
    for i in range(self.deg,-1,-1):
      if self.coef[i] != b.coef[i]:
        return False
    return True

  def toString(self):
    '''Print out this Polynomial'''
    if self.deg<0:
      return ''
    if self.deg==0:
      return str(self.coef[0])
    if self.deg==1:
      s=str(self.coef[1])+'*p'
      if self.coef[0]!=0:
        return s+' + '+str(self.coef[0])
      else:
        return s
    s=str(self.coef[self.deg])+'*p^'+str(self.deg)
    for i in range(self.deg-1,-1,-1):
      if self.coef[i]==0:
        continue
      elif self.coef[i]>0:
        s=s+' + '+str(self.coef[i])
      elif self.coef[i]<0:
        s=s+' - '+str(-self.coef[i])
      if i>1:
        s=s+'*p^'+str(i)
      elif i==1:
        s=s+'*p'
    return s
  
#  def computePol(self,p):
#    if self.deg<0:
#      return 0
#    if self.deg==0:
#      return float(self.coef[0])
#    if self.deg==1:
#      pol=self.coef[1]*p
#      if self.coef[0]!=0:
#        return float(pol+self.coef[0])
#      else:
#        return float(pol)
#    pol=self.coef[self.deg]*p**self.deg
#    for i in range(self.deg-1,-1,-1):
#      if self.coef[i]==0:
#        continue
#      pol=pol+self.coef[i]*p**i      
#    return float(pol)

#coef=[0,1]
#a=Polynomial(coef)
'''
c=Polynomial(2,3)
a=Polynomial(1,2)
c=a.plus(c)
c=c.times(c)
print 'c='+ c.toString()

print 'a=' +a.toString()
'''
