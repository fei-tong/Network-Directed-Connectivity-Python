'''
Created on Dec 30, 2012

@author: tongfei
'''
import sys
import copy

class FReal(object):
    '''
    Do Real Arithmetic Operations with infinite number of decimals
    '''


    def __init__(self,operand='.'):
        '''
        Parameters: 
           operand: string or float or integer
        '''
        if isinstance(operand,str)!=True:
            print "Error (In FReal Constructor): The parameter should be a string!"
            sys.exit()
        ss=str(operand).split('.')          #decimal point
        if len(ss)==1:
            ss.insert(1,'0')
        self.i=list(ss[0])                  #integer
        self.d=list(ss[1])                  #decimal
        
        self.pn='+'                         #positive/negative
        
        if len(self.i)!=0 and self.i[0]=='-':
            del self.i[0]
            self.pn='-'
        if len(self.i)==0:                   #self.i[0]==''
            self.i=['0']
        if self.i[-1]=='L':
            del self.i[-1] #delete the last one
        
        if len(self.d)==0:
            self.d=['0']
            
        self.deleteZero()
        
    def __sub__(self,freal):
        if isinstance(freal,FReal)!=True:
            print "TypeError: cannot convert %s to FReal. First Convert the %s to FReal" % (type(freal),type(freal))
            sys.exit()
        f1=copy.deepcopy(self)
        f2=copy.deepcopy(freal)
        
        if self.pn=='+' and freal.pn=='-':
            f2.pn='+'
            return f1+f2
        if self.pn=='-' and freal.pn=='+':
            f1.pn='+'
            result=f1+f2
            result.pn='-'
            return result
        if self.pn=='-' and freal.pn=='-':
            f1.pn="+"
            f2.pn='+'
            return f2-f1
        
        result=FReal()
        
        if len(self.i)<len(freal.i):
            f1=copy.deepcopy(freal)
            f2=copy.deepcopy(self)
            result.pn='-'
            for j in range(0,len(freal.i)-len(self.i)):
                f2.i.insert(0,'0')  #add zero for integer part
        elif len(self.i)==len(freal.i):
            ok=False
            for j in range(0,len(self.i)):
                if self.i[j]<freal.i[j]:
                    f1=copy.deepcopy(freal)
                    f2=copy.deepcopy(self)
                    result.pn='-'
                    ok=True
                    break
                elif self.i[j]>freal.i[j]:
                    ok=True
                    break
            if ok==False:
                min_d=min(len(self.d),len(freal.d))
                for j in range(0,min_d):
                    if self.d[j]<freal.d[j]:
                        f1=copy.deepcopy(freal)
                        f2=copy.deepcopy(self)
                        result.pn='-'
                        ok=True
                        break
                    elif self.d[j]>freal.d[j]:
                        ok=True
                        break
                if ok==False:
                    if len(self.d)==len(freal.d):
                        return result
                    else:
                        max_d=max(len(self.d),len(freal.d))
                        result.d=['0' for j in range(0,max_d)]
                        if len(self.d)>len(freal.d):
                            for j in range(min_d,max_d):
                                result.d[j]=self.d[j]
                                return result
                        else:
                            for j in range(min_d,max_d):
                                result.d[j]=freal.d[j]
                                result.pn='-'
                                return result
        else:
            for j in range(0,len(self.i)-len(freal.i)):
                f2.i.insert(0,'0')  #add zero for integer part
                
        # add zero for decimal part
        f1_d=len(f1.d)
        f2_d=len(f2.d)
        if f1_d>f2_d:
            for j in range(0,f1_d-f2_d):
                f2.d.append('0')
        elif f1_d<f2_d:
            for j in range(0,f2_d-f1_d):
                f1.d.append('0')
        
        #print f1.toString()
        #print f2.toString()
        
        #begin to calculate     
        f_i=len(f1.i)
        f_d=len(f1.d)
        result.d=['0' for j in range(0,f_d)]
        result.i=['0' for j in range(0,f_i)]
        c=0 # borrow -c from the adjacent upper bit
        for j in range(f_d-1,-1,-1):
            if int(f1.d[j])+c<int(f2.d[j]):
                result.d[j]=str(10+int(f1.d[j])+c-int(f2.d[j]))
                c=-1
            else:
                result.d[j]=str(int(f1.d[j])+c-int(f2.d[j]))
                c=0
        for j in range(f_i-1,-1,-1):
            if int(f1.i[j])+c<int(f2.i[j]):
                result.i[j]=str(10+int(f1.i[j])+c-int(f2.i[j]))
                c=-1
            else:
                result.i[j]=str(int(f1.i[j])+c-int(f2.i[j]))
                c=0
        result.deleteZero()
        return result
    
    def __add__(self,freal):
        if isinstance(freal,FReal)!=True:
            print "TypeError: cannot convert %s to FReal. First Convert the %s to FReal" % (type(freal),type(freal))
            sys.exit()
        f1=copy.deepcopy(self)
        f2=copy.deepcopy(freal)
        
        if self.pn=='+' and freal.pn=='-':
            f2.pn='+'
            return f1-f2
        if self.pn=='-' and freal.pn=='+':
            f1.pn='+'
            return f2-f1
        if self.pn=='-' and freal.pn=='-':
            f1.pn='+'
            f2.pn='+'
            result=f1+f2
            result.pn='-'
            return result
        
        #add zero to integer part
        if len(f1.i)>len(f2.i):
            for j in range(0,len(f1.i)-len(f2.i)):
                f2.i.insert(0,'0')  #add zero for integer part
        elif len(f1.i)<len(f2.i):
            for j in range(0,len(f2.i)-len(f1.i)):
                f1.i.insert(0,'0')
                
        c=0                     # carry bit
        result=FReal()
        #calculate the decimal part
        n=max(len(f1.d),len(f2.d))
        result.d=['0' for j in range(0,n)]
        for j in range(0,len(f1.d)):
            result.d[j]=f1.d[j]
        for j in range(len(f2.d)-1,-1,-1):
            temp=str(int(result.d[j])+int(f2.d[j])+c)
            c=0
            if len(temp)==2:
                c=int(temp[0])
                temp=temp[1]
            result.d[j]=temp
        
        #calculate the integer part
        n=max(len(f1.i),len(f2.i))
        result.i=['0' for j in range(0,n+1)]
        
        k=len(result.i)-1
        for j in range(len(f1.i)-1,-1,-1):
            result.i[k]=f1.i[j]
            k-=1
            
        k=len(result.i)-1
        for j in range(len(f2.i)-1,-1,-1):
            temp=str(int(result.i[k])+int(f2.i[j])+c)
            c=0
            if len(temp)==2:
                c=int(temp[0])
                temp=temp[1]
            result.i[k]=temp
            k-=1
        result.i[k]=str(int(result.i[k])+c)
        result.deleteZero()
        return result
    
    def __mul__(self,freal): #multiply
        if isinstance(freal,FReal)!=True:
            print "TypeError: cannot convert %s to FReal. First Convert the %s to FReal" % (type(freal),type(freal))
            sys.exit()
            
        result=FReal()
        if (self.i==['0'] and self.d==['0']) or (freal.i==['0'] and freal.d==['0']):
            return result
        
        f1=copy.deepcopy(self)
        f2=copy.deepcopy(freal)  
            
        s_f1=f1.i+f1.d
        s_f2=f2.i+f2.d
        c=0 # carry bit
        
        for j in range(len(s_f2)-1,-1,-1):
            s_r=''
            if s_f2[j]!='0':
                if s_f2[j]=='1':
                    for k in range(len(s_f1)-1,-1,-1):
                        s_r=s_f1[k]+s_r
                else:                    
                    for k in range(len(s_f1)-1,-1,-1):
                        temp=str(int(s_f1[k])*int(s_f2[j])+c)
                        c=0
                        if len(temp)==2:
                            c=int(temp[0])
                            temp=temp[1]
                        s_r=temp+s_r
                    if c!=0:
                        s_r=str(c)+s_r
                        c=0
                for k in range(j,len(s_f2)-1):
                    s_r=s_r+'0'
                result=result+FReal(s_r)
            
        point_n=len(self.d)+len(freal.d)
        
        if point_n<=len(result.i):
            result.d=result.i[len(result.i)-point_n:]
            result.i=result.i[:len(result.i)-point_n]
            if len(result.i)==0:
                result.i=['0']
        else:
            temp=['0' for j in range(0,point_n-len(result.i))]
            result.d=temp+result.i
            result.i=['0']
        
        if (self.pn=='+' and freal.pn=='-') or (self.pn=='-' and freal.pn=='+'):
            result.pn='-'
        result.deleteZero()
        return result
        
            
    def __pow__(self,p): #**
        if p==0:
            return FReal('1')
        if p<0:
            print "Error: the exponent should be larger than zero"
            sys.exit()
        origin=copy.deepcopy(self)
        result=copy.deepcopy(self)    
        for j in range(1,p):
            result=result*origin
        
        return result
        
    
    def deleteZero(self):
        #delete 0 in the front of the integer and in the end of the decimal
        while(self.i[0]=='0' and len(self.i)>1):
            del self.i[0]
        
        for j in range(len(self.d)-1,0,-1): #for decimal, keep the first one result.d[0]
            if self.d[j]!='0':
                break
            del self.d[j]
    
    def toString(self):
        s=''
        if self.pn=='-':
            s='-'
        for j in range(0,len(self.i)):
            s=s+self.i[j]
        s=s+'.'
        for j in range(0,len(self.d)):
            s=s+self.d[j]
        return s
    

        