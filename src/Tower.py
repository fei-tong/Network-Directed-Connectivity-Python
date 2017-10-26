'''
Created on Dec 22, 2012

@author: tongfei
'''
#!/usr/bin/python
#Filename:Tower.py

import Polynomial
import Func
import copy

class Tower:
  def getPolynomial(self):
    ''' Calculate the polynomial of this Tower
    '''
    debug=False
    #1. Have been calculated before, stored in "dic"
    if self.toString() in Func.T_dic:
      return Func.T_dic[self.toString()]

    #2. the current shape only has top and base, no intermediate layer
    if len(self.layer)==0:
      p = Polynomial.Polynomial(1,self.margin).times(Func.getPtl('t '+str(self.top[0])+' '+str(self.top[1])));
      Func.T_dic[self.toString()]=p
      return p
    
    #3. ladder (horizontal or vertical or special tower:stair)
    if self.top[0]==0 and self.top[1]==0 and self.margin==0:
      if len(self.layer)==1: # 3.1 horizontal ladder
        p=Func.getPtl('s '+str(self.layer[0][1]))
        if p!=False:
          return p
      else:
        onerec=True #only one rectangle on each layer
        for i in range(0,len(self.layer)):
          if self.layer[i][1]>1: #self.layer[i][0]:triangle; self.layer[i][1]: rectangle
            onerec=False
            break
        if onerec==True:  # 3.2 vertical ladder
          p=Func.getPtl('s '+str(len(self.layer)))
          if p!=False:
            #self.ifdebug(debug)
            return p
        else: # 3.3 Special Tower: Stair
          self.ifdebug(debug)
          p=self.getStairPolynomial()
          if p!=False:
            Func.T_dic[self.toString()]=p
            #self.ifdebug(debug)
            return p

    #4. tower like "T (0,x) layer y"
    if (self.top[0]==0 and self.top[1]>0) or (self.margin>0):
      #print "#4. tower like (0,x) layer y"
      p=Polynomial.Polynomial(1,0) # p=1
      t=copy.deepcopy(self.top)
      m=self.margin
      if self.top[0]==0 and self.top[1]>0:
        p=p.times(Polynomial.Polynomial(1,self.top[1]))
        t=[0,0]
      if m>0:
        p=p.times(Polynomial.Polynomial(1,m))
        m=0
      l=copy.deepcopy(self.layer)
      t_temp=Tower(t,l,m)

      p_temp=t_temp.getPolynomial()
      Func.T_dic[t_temp.toString()]=p_temp

      p=p.times(p_temp)
      #Func.T_dic[self.toString()]=p
      #self.ifdebug(debug)
      return p
    
    #5. Tower decomposition
    #Find the first layer to start
    firstTrgLyr=-1
    for k in range(len(self.layer)-1,-1,-1):
      if self.layer[k][0]!=0:
        firstTrgLyr = k
        break

    #the length of left-topmost path "A", we call it critical path here
    # Find which layer each edge on critical path is in, and the distance to the rightmost: (x,l,d)
    # x: the type of edge
        # 'b': bevel edge; 'h': horizontal edge; 'v': vertical edge
    # l: the layer 'l'
    # d: the distance (the number of rectangles+triangles) to the rightmost
    stpLyr=[] # list of list. The type [...,[x,l,d],...].
    numOfCrtclPth = 0
    if firstTrgLyr==-1: #the top has triangles, no triangles on each layer
      stpLyr.append(['b',-1,self.top[0]])
      numOfCrtclPth+=1
      for k in range(0,len(self.layer)):
        if k==0:
          temp=self.layer[k][1]-self.top[0]
          numOfCrtclPth+=temp+1
          for n in range(1,temp+1):
            stpLyr.append(['h',0,self.top[0]+n])
          stpLyr.append(['v',0,self.top[0]+temp])
        else: #(k>0)
          temp=self.layer[k][1]-self.layer[k-1][1]
          numOfCrtclPth+=temp+1
          for n in range(1,temp+1):
            stpLyr.append(['h',k,self.layer[k-1][1]+n])
          stpLyr.append(['v',k,self.layer[k-1][1]+temp])
    else: # firstTrgLyr!=-1
      stpLyr.append(['b',firstTrgLyr,self.layer[firstTrgLyr][0]+self.layer[firstTrgLyr][1]])
      numOfCrtclPth+=1
      for k in range(firstTrgLyr+1,len(self.layer)):
        temp=self.layer[k][1]-(self.layer[k-1][0]+self.layer[k-1][1])
        numOfCrtclPth+=temp+1
        for n in range(1,temp+1):
          stpLyr.append(['h',k,self.layer[k-1][0]+self.layer[k-1][1]+n])
        stpLyr.append(['v',k,self.layer[k-1][0]+self.layer[k-1][1]+temp])
    if debug==True:
      print "numOfCrtclPth=%d" % numOfCrtclPth
      for i in range(0,len(stpLyr)): #for test
        print "%d:(%s,%d,%d)" % (i,stpLyr[i][0],stpLyr[i][1],stpLyr[i][2])   #for test
      print
    
    # calculate each intermediate Tower
    fnlRslt=Polynomial.Polynomial(1,numOfCrtclPth) #Initially it equals to P(A), and it records final result
    temp_top=copy.deepcopy(self.top)
    temp_layer=copy.deepcopy(self.layer)
    temp_margin=self.margin
    interTwr=Tower(temp_top,temp_layer,temp_margin) # Tower:self
    for i in range(0,numOfCrtclPth):
      if debug==True:
        print 
        print "Begin(Tower): i=%d,interTwr = %s." % (i,interTwr.toString())
      # S(i)=(1-p)*p^i
      Si=Polynomial.Polynomial(1,0).minus(Polynomial.Polynomial(1,1)).times(Polynomial.Polynomial(1,i))
      #.1
      if stpLyr[i][0]=='b': # bevel line, the first line
        if stpLyr[i][1]==-1: # at 'top'
          interTwr.top[0]=interTwr.top[0]-1 # set top: the # of trgs minus 1
        else:                # at 'layer'
          pre_trg=interTwr.layer[stpLyr[i][1]][0]
          interTwr.layer[stpLyr[i][1]][0]=pre_trg-1
          if stpLyr[i][1]==len(interTwr.layer)-1: # at the bottommost layer
            interTwr.margin=interTwr.margin+1 # set margin
      #.2
      elif stpLyr[i][0]=='h': # horizontal line
        if stpLyr[i][1]==len(self.layer)-1: # the current layer is the last layer
          interTwr.margin=self.layer[stpLyr[i][1]][1]-stpLyr[i][2]+1
        #.2.pre.1
        if stpLyr[i-1][0]=='b': # the previous line is a bevel line
          if stpLyr[i-1][1]==-1: # the previous bevel line is at 'top'
            if stpLyr[i-1][2]==1: # the prevous bevel line contains only one triangle
              interTwr.top[0]=1
              interTwr.top[1]=interTwr.top[1]+1 # set top: the height of the top plus 1
              del interTwr.layer[0] # delete the first layer
            else:  # the prevous bevel line contains more than one triangle
              #interTwr.top[0]=interTwr.top[0]-1 # set top: the # of trgs minus 1
              loffset = stpLyr[i][1]-(interTwr.top[1]-self.top[1])
              interTwr.layer[loffset][0]=1
              interTwr.layer[loffset][1]=stpLyr[i][2]-2
          else: # the previous bevel line is at 'layer'
            loffset = stpLyr[i][1]-(interTwr.top[1]-self.top[1])
            #current layer
            pre_trg=interTwr.layer[loffset][0]
            pre_rec=stpLyr[i][2]
            interTwr.layer[loffset]=[pre_trg+1,pre_rec-2]
        #.2.pre.2
        elif stpLyr[i-1][0]=='h': # the previous line is a horizontal line
          loffset = stpLyr[i][1]-(interTwr.top[1]-self.top[1])
          if loffset>=0:
            pre_trg=interTwr.layer[loffset][0]
            interTwr.layer[loffset][0]=pre_trg+1
          else:
            interTwr.top[0]=interTwr.top[0]+1
        #.2.pre.3
        elif stpLyr[i-1][0]=='v': # the previous line is a vertical line
          if stpLyr[i-1][2]==1 : # the prevous vertical line contains only one rectangle
            interTwr.top=[interTwr.top[0]+1,interTwr.top[1]+1] # set top
            del interTwr.layer[0] # delete the first layer
          else: # the prevous vertical line contains more than one rectangle
            loffset = stpLyr[i][1]-(interTwr.top[1]-self.top[1])
            interTwr.layer[loffset][0]=1
            interTwr.layer[loffset][1]=stpLyr[i][2]-2
      #.3
      elif stpLyr[i][0]=='v': # vertical line
        if i==numOfCrtclPth-1: # the last edge on the critical path
          interTwr.margin=1
        #.3.pre.1
        if stpLyr[i-1][0]=='b': # the previous line is a bevel line
          if stpLyr[i-1][1]==-1: # the previous bevel line is at 'top'
            if stpLyr[i-1][2]==1: # the prevous bevel line contains only one triangle
              interTwr.top=[0,interTwr.top[1]+1] # set top: the height of the top plus 1
              del interTwr.layer[0] # delete the first layer
            else: # the prevous bevel line contains more than one triangle
              loffset = stpLyr[i][1]-(interTwr.top[1]-self.top[1])
              pre_rec = interTwr.layer[loffset][1]
              interTwr.layer[loffset][1]=pre_rec-1
          else: # the previous bevel line is at 'layer'
            loffset = stpLyr[i][1]-(interTwr.top[1]-self.top[1])
            #current layer
            pre_rec=interTwr.layer[loffset][1]
            interTwr.layer[loffset][1]=pre_rec-1
        #.3.pre.2
        elif stpLyr[i-1][0]=='v': # the previous line is a vertical line
          if stpLyr[i-1][2]==1: # with only one rectangle
            interTwr.top=[0,interTwr.top[1]+1] # set top
            del interTwr.layer[0] # delete the first layer
          else: # with more than one rectangle
            loffset = stpLyr[i][1]-(interTwr.top[1]-self.top[1])
            pre_rec=interTwr.layer[loffset][1]
            interTwr.layer[loffset][1]=pre_rec-1
          
      BSi=interTwr.getPolynomial()
      fnlRslt=fnlRslt.plus(Si.times(BSi))
      if debug==True:
        print "After(Tower): i=%d,interTwr = %s." % (i,interTwr.toString())
        print "(Tower)i=%d,Si=%s,BSi=%s." % (i,Si.toString(),BSi.toString())
        print "       i=%d,Si*BSi=%s." % (i,Si.times(BSi).toString())
        print "P(A)+Sum(Si*BSi)=%s." % fnlRslt.toString()
        print
        print
      Func.T_dic[self.toString()]=fnlRslt
    return fnlRslt
    #return False 
#endof Tower.getPolynomial(self)


  def getStairPolynomial(self):
    '''Calculate the polynomial of Stair
    '''
    debug=False
    if debug==True:
      print
      print "**********In Stair*****************"
    
    #1. Have been calculated before, stored in "dic"
    if self.toString() in Func.T_dic:
      return Func.T_dic[self.toString()]

    #2. Decomposition
    # the length of left-topmost path "A", we call it critical path here
    numOfCrtclPth = self.layer[len(self.layer)-1][1] + len(self.layer)
    if debug==True:
      print "numOfCrtclPth=%d" % numOfCrtclPth

    # Find which layer each edge on critical path is in, and the distance to the rightmost: (x,l,d)
    # x: the type of edge
        # 'f': the first horizontal edge; 'h': horizontal edge; 'v': vertical edge
    # l: the layer 'l'
    # d: the distance (the number of rectangles) to the rightmost
    stpLyr=[] # list of list. The type [...,[x,l,d],...].
    for i in range(0,len(self.layer)):
      if i==0: #the first layer
        for j in range(0,self.layer[0][1]+1):
          if j<self.layer[0][1]:
            if j>0:
              stpLyr.append(['h',i,j+1]) # horizontal edge
            elif j==0: #the first edge on the first layer
              stpLyr.append(['f',i,j+1]) # the first horizontal edge
          else:
            stpLyr.append(['v',i,j]) # vertical edge
      else:
        for j in range(0,self.layer[i][1]-self.layer[i-1][1]+1):
          if j<self.layer[i][1]-self.layer[i-1][1]:
            stpLyr.append(['h',i,j+1+self.layer[i-1][1]]) # horizontal edge
          else:
            stpLyr.append(['v',i,j+self.layer[i-1][1]]) # vertical edge
    if debug==True:
      for i in range(0,len(stpLyr)): #for test
        print "%d:(%s,%d,%d)" % (i,stpLyr[i][0],stpLyr[i][1],stpLyr[i][2])   #for test

    # calculate each intermediate Tower
    fnlRslt=Polynomial.Polynomial(1,numOfCrtclPth) #Initially it equals to P(A), and it records final result
    temp_top=copy.deepcopy(self.top)
    temp_layer=copy.deepcopy(self.layer)
    temp_margin=self.margin
    interTwr=Tower(temp_top,temp_layer,temp_margin) # Tower:self

    # break the steps one by one to find the intermediate shapes along the critical path
    for i in range(0,numOfCrtclPth):
      if debug==True:
        print 
        print "Begin(Stair): i=%d,interTwr = %s." % (i,interTwr.toString())
      # S(i)=(1-p)*p^i
      Si=Polynomial.Polynomial(1,0).minus(Polynomial.Polynomial(1,1)).times(Polynomial.Polynomial(1,i))
      #print "fnlRslt:"+fnlRslt.toString()
      #.1
      # interTwr.top[1]+len(interTwr.layer)==len(self.layer)
      if stpLyr[i][0]=='f': # the first edge
        if stpLyr[i][1]==len(self.layer)-1: # the current layer is the last layer
          interTwr.margin=self.layer[stpLyr[i][1]][1]-stpLyr[i][2]+1
        interTwr.top[1]=1 # set top
        del interTwr.layer[0] # delete the first layer
      #.2
      elif stpLyr[i][0]=='h': # horizontal edge
        if stpLyr[i][1]==len(self.layer)-1: # the current layer is the last layer
          interTwr.margin=self.layer[stpLyr[i][1]][1]-stpLyr[i][2]+1
        #.2.pre.1
        if stpLyr[i-1][0]=='f': # the previous edge is the first edge
          interTwr.top[0]=interTwr.top[0]+1 # set top: the # of triangles plus 1
        #.2.pre.2
        elif stpLyr[i-1][0]=='h': # the previous edge is a horizontal edge
          loffset = stpLyr[i][1]-interTwr.top[1]
          if loffset>=0:
            pre_trg=interTwr.layer[loffset][0]
            interTwr.layer[loffset][0]=pre_trg+1
          else:
            interTwr.top[0]=interTwr.top[0]+1
        #.2.pre.3
        elif stpLyr[i-1][0]=='v': # the previous edge is a vertical edge
          if stpLyr[i-1][2]==1: # with only one rectangle
            interTwr.top=[interTwr.top[0]+1,interTwr.top[1]+1] # set top
            del interTwr.layer[0] # delete the first layer
          else: # with more than one rectangle
            loffset = stpLyr[i][1]-interTwr.top[1]
            interTwr.layer[loffset][0]=1
            interTwr.layer[loffset][1]=stpLyr[i][2]-2
      #.3
      elif stpLyr[i][0]=='v':# vertical edge
        if i==numOfCrtclPth-1: # the last edge on the critical path
          interTwr.margin=1
        #.3.pre.0
        #if stpLyr[i-1][0]=='f': # the previous edge is the first edge
          
        #.3.pre.1
        if stpLyr[i-1][0]=='v': # the previous edge is a vertical edge
          if stpLyr[i-1][2]==1: # with only one rectangle
            interTwr.top=[0,interTwr.top[1]+1] # set top
            del interTwr.layer[0] # delete the first layer
          else: # with more than one rectangle
            loffset = stpLyr[i][1]-interTwr.top[1]
            pre_rec=interTwr.layer[loffset][1]
            interTwr.layer[loffset][1]=pre_rec-1
          
      BSi=interTwr.getPolynomial()
      fnlRslt = fnlRslt.plus(Si.times(BSi))
      if debug==True:
        print "After(Stair): i=%d,interTwr = %s." % (i,interTwr.toString())
        print "(Stair)i=%d,Si=%s,BSi=%s." % (i,Si.toString(),BSi.toString())
        print "       i=%d,Si*BSi=%s." % (i,Si.times(BSi).toString())
        print "P(A)+Sum(Si*BSi)=%s." % fnlRslt.toString()
        print
      
        print "***********out STAIR*********"
        print
    return fnlRslt                
    #return False    
#endof Tower.getStairPolynomial(self)

  def __init__(self,top=[0,0],layer=[],margin=0):
    self.top=copy.deepcopy(top) #len(top)=2, top[0]: the number of triangles on the topmost layer, 
                             #top[1]: the number of rightmost verticle lines
    self.margin=margin #the number of margin lines on the base
    if isinstance(layer,list): #layer is a list of list [trg,rec]
      self.layer=copy.deepcopy(layer)
    elif isinstance(layer,str):#layer is a string like '2-3 0-3 ...'
      ss=layer.split(' ')
      self.layer=[]
      for i in range(0,len(ss)):
        self.layer.append([ss[i].split('-')[0],ss[i].split('-')[1]])
#endof Tower.__init__(self,top,layer,margin)

  def ifdebug(self,debug): 
    if debug==True:
      print  self.toString()
      #pass
#endof Tower.ifdebug(self,debug)

#  def setTop(self,top):
#    self.top=copy.deepcopy(top)
#endof Tower.setTop(self,top)

#  def setMargin(self,margin):
#    self.margin=copy.deepcopy(margin)
#endof Tower.setMargin(self,margin)

#  def getTop(self):
#    return copy.deepcopy(self.top)
#endof Tower.getTop(self)

#  def getMargin(self):
#    return copy.deepcopy(self.margin)
#endof Tower.getMargin(self)

#  def delLyr(self,lyr):
    '''Delete one layer'''
#    del self.layer[lyr]

#  def setLyrTr(self,lyr,trg):
    '''Set the number of triangles ('trg') in layer "lyr". '''
#    self.layer[lyr][0]=trg
#endof Tower.setLyrTr(self,lyr,trg)

#  def setLyrRc(self,lyr,rec):
    '''Set the number of rectangles ('rec') in layer "lyr". '''
#    self.layer[lyr][1]=rec
#endof Tower.setLyrRc(self,lyr,rec)

#  def getLyrTr(self,lyr):
    '''Get the number of triangles ('trg') in layer "lyr". '''
#    return self.layer[lyr][0]
#endof Tower.getLyrTr(self,lyr)

#  def getLyrRc(self,lyr):
    ''' Get the number of rectangles ('rec') in layer "lyr". '''
#    return self.layer[lyr][1]
#endof getLyrRc(self,lyr)

  def toString(self):
    '''Return the string of this Tower in style: "T top layer margin", where
       T: a char, means tower;
       top: the number of triangles on the topmost layer;
       layer: a list of list like "[[0,3] ...]" (zero triangles and 3 rectangles);
       margin: the number of margin lines on the base
    '''
    s=""
    for i in range(0,len(self.layer)):
      s+=str(self.layer[i][0])+'-'+str(self.layer[i][1])+' '
    return 'T ('+str(self.top[0])+','+str(self.top[1])+') '+s+str(self.margin)
#endof Tower.toString(self)
#endof class Tower

'''
print "**************In Tower**************"    

#T=Tower([0,0],[[0,3]],1)
#print T.getPolynomial().toString()
#print
#T=Tower(top=[1,2],margin=1)
#print T.getPolynomial().toString()
#print

T=Tower([0,0],[[0,5],[0,5],[0,5],[0,5],[0,5]],0)
print T.getPolynomial().toString()
#T=Tower([1,1],[[0,3]],0)
#print T.getPolynomial().toString()
#T=Tower([0,0],[[0,2],[0,2],[0,2]],0)
#print T.getPolynomial().toString()

print
#for name,p in Func.T_dic.items():
#  print "%s: %s" % (name,p.toString())
#for i in range(0,len(T.layer)):
#  print T.getLyrTr(i)
print "**************In Tower**************"
print
'''
