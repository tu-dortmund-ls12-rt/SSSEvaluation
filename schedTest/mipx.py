#!/usr/bin/python

# Copyright 2016, Gurobi Optimization, Inc.

# This example formulates and solves the following simple MIP model:
#  maximize
#        x +   y + 2 z
#  subject to
#        x + 2 y + 3 z <= 4
#        x +   y       >= 1
#  x, y, z binary

from mip import *
from gurobipy import *

import gurobipy
def sumDBF(t,tasks,d):
    sumd=0
    for j in range(len(tasks)):
        task=tasks[j]
        d2=task['period']-task['sslength']-d[j].x
        if t<d[j].x:
            dbf=0
        elif t<d2: 
            dbf=task['Cseg'][0]+(t-d[j].x)*task['Cseg'][0]/task['period']
        else:        
            dbf=task['Cseg'][0]+task['Cseg'][1]+((t-d[j].x)*task['Cseg'][0]/task['period'])+(t-d2)*task['Cseg'][1]/task['period']
        sumd+=dbf
    return sumd
def mip(tasks):
    
    for itask in tasks:

        if itask['Cseg'][0]>itask['Cseg'][1]:
            k=itask['Cseg'][0]
            itask['Cseg'][0]=itask['Cseg'][1]
            itask['Cseg'][1]=k
        
    # Create a new model
    m = Model("mip1")
    d=[]
    n=len(tasks)
    a2=[[0 for x in range(n)] for j in range(n)]
    a1=[[0 for x in range(n)] for j in range(n)]
    b2=[[0 for x in range(n)] for j in range(n)]
    b1=[[0 for x in range(n)] for j in range(n)]
    g12=[[0 for x in range(n)] for j in range(n)]
    g11=[[0 for x in range(n)] for j in range(n)]
    
    g22=[[0 for x in range(n)] for j in range(n)]
    g21=[[0 for x in range(n)] for j in range(n)]
    
    y1=[[0 for x in range(n)] for j in range(n)]
    y2=[[0 for x in range(n)] for j in range(n)]
    
    M=0
    for itask in tasks: 
        if itask['period']>M:
            M=itask['period']
    M=10000*M
    #M=99999999
    
    for i in range(len(tasks)):        
        d.append( m.addVar(vtype=GRB.INTEGER, name="d"+str(i),lb=tasks[i]['Cseg'][0],ub=(tasks[i]['period']-tasks[i]['sslength'])/2))
        
        for j in range(len(tasks)):
            a2[i][j]= m.addVar(vtype=GRB.CONTINUOUS, name="a2"+str(i)+str(j),lb=0)
            b2[i][j]= m.addVar(vtype=GRB.CONTINUOUS, name="b2"+str(i)+str(j),lb=0)
            y2[i][j]= m.addVar(vtype=GRB.CONTINUOUS, name="y2"+str(i)+str(j),lb=0)
            g12[i][j]= m.addVar(vtype=GRB.BINARY, name="g12"+str(i)+str(j))
            g22[i][j]= m.addVar(vtype=GRB.BINARY, name="g22"+str(i)+str(j)) 

            a1[i][j]= m.addVar(vtype=GRB.CONTINUOUS, name="a1"+str(i)+str(j),lb=0)
            b1[i][j]= m.addVar(vtype=GRB.CONTINUOUS, name="b1"+str(i)+str(j),lb=0)
            y1[i][j]= m.addVar(vtype=GRB.CONTINUOUS, name="y1"+str(i)+str(j),lb=0)
            g11[i][j]= m.addVar(vtype=GRB.BINARY, name="g11"+str(i)+str(j))
            g21[i][j]= m.addVar(vtype=GRB.BINARY, name="g21"+str(i)+str(j)) 
       
    
    m.params.OutputFlag=0
    # Integrate new variables
    #m.params.Presolve = 0
    m.update()
    
    # Add constraint: x + 2 y + 3 z <= 4
    # testing two points for each task 
    for i in range(len(tasks)):
        t=d[i]
        y=y2[i]
        a=a2[i]
        b=b2[i]
        g1=g12[i]
        g2=g22[i]
        ##compute dbf with mixed integer linear programming 
        for j in range(len(tasks)):
            task=tasks[j]
            d2=task['period']-task['sslength']-d[j]
            expr1=task['Cseg'][0]+(t-d[j])*task['Cseg'][0]/task['period']
            expr2=task['Cseg'][0]+task['Cseg'][1]+((t-d[j])*task['Cseg'][0]/task['period'])+(t-d2)*task['Cseg'][1]/task['period']
            
            ## max(a,b)
            m.addConstr(y[j]>=a[j]  , "c4"+str(i)+str(j))
            m.addConstr(y[j]>=b[j]  , "c5"+str(i)+str(j))

            ## if t>=d1 then a>=expr1; otherwise, a>=0
            m.addConstr(t-d[j]>=-M*(1-g1[j])  , "c6"+str(i)+str(j))
            m.addConstr(t-d[j]<=M*g1[j]-1  , "c7"+str(i)+str(j))
            
            m.addConstr(a[j]-expr1>=-M*(1-g1[j])  , "c8"+str(i)+str(j))
            m.addConstr(a[j]>=-M*g1[j] , "c9"+str(i)+str(j))
    
            m.addConstr(t-d2>=-M*(1-g2[j])  , "c10"+str(i)+str(j))
            m.addConstr(t-d2<=M*g2[j]-1   , "c11"+str(i)+str(j))
            
            m.addConstr(b[j]-expr2>=-M*(1-g2[j])  , "c12"+str(i)+str(j))
            m.addConstr(b[j]>=-M*g2[j]  , "c13"+str(i)+str(j))


            
            
        t=tasks[i]['period']-tasks[i]['sslength']-d[i]
        y=y1[i]
        a=a1[i]
        b=b1[i]
        g1=g11[i]
        g2=g21[i]
        for j in range(len(tasks)):
            task=tasks[j]
            expr1=task['Cseg'][0]+(t-d[j])*task['Cseg'][0]/task['period']

            d2=task['period']-task['sslength']-d[j]
            expr2=task['Cseg'][0]+task['Cseg'][1]+((t-d[j])*task['Cseg'][0]/task['period'])+(t-d2)*task['Cseg'][1]/task['period']
            

            m.addConstr(y[j]>=a[j]  , "c14"+str(i)+str(j))
            m.addConstr(y[j]>=b[j]  , "c15"+str(i)+str(j))

            
            m.addConstr(t-d[j]>=-M*(1-g1[j])  , "c16"+str(i)+str(j))
            m.addConstr(t-d[j]<=M*g1[j]-1  , "c17"+str(i)+str(j))
            
            m.addConstr(a[j]-expr1>=-M*(1-g1[j])  , "c18"+str(i)+str(j))
            m.addConstr(a[j]>=-M*g1[j]  , "c19"+str(i)+str(j))
    
            m.addConstr(t-d2>=-M*(1-g2[j])  , "c20"+str(i)+str(j))
            m.addConstr(t-d2<=M*g2[j]-1  , "c21"+str(i)+str(j))
            
            m.addConstr(b[j]-expr2>=-M*(1-g2[j])  , "c22"+str(i)+str(j))
            m.addConstr(b[j]>=-M*g2[j]  , "c23"+str(i)+str(j))


            

    
    for i in range(len(tasks)):
        t=d[i]
        y=y2[i]
        expr= LinExpr()
        for j in range(len(tasks)):
            expr=expr+y[j]

        m.addConstr(expr<=t , "c24"+str(i))
   
    for i in range(len(tasks)):
        task=tasks[i]
        y=y1[i]
        expr= LinExpr()
        t=task['period']-task['sslength']-d[i]
        for j in range(len(tasks)):
            expr=expr+y[j]
        
        m.addConstr(expr<=t  , "c25"+str(i))
    
    #expr = LinExpr()
    # Set objective
    m.setObjective(0, GRB.MINIMIZE )
    m.update()
    #m.params.method = 4;
    #m.params.NumericFocus = 3
    m.optimize()
    
    m.write("model.lp") 
    #print(m.ObjCon)
    #print(n,m.NumConstrs)


    #for v in m.getVars():
    #    print('%s %g' % (v.varName, v.x))
    #
    #if m.Status!=2:
         #m.computeIIS();
         #print(m.Status)
         #print(tasks)
         #m.write("model.ilp");
         #print(m.getConstrs)
            

    #     ##for i in d:
    #      #   print(i.x)
    #     # for i in y1:
    #     #     for j in i:
    #     #         print(j.x)
    #     # for i in y2:
    #     #     for j in i:
    #     #         print(j.x)
    #     # for i in a2:
    #     #     for j in i:
    #     #         print(j.x)
    #     # for i in b2:
    #     #     for j in i:
    #     #         print(j.x)
    #     sys.exit()
    if m.Status==2:
        for i in range(len(tasks)):        
            
            t=d[i].X
            
            
            if sumDBF(t,tasks,d)>t+0.1:
                print(tasks)
                for k in range(len(tasks)):        
                    print("tasks",k,d[k].X)
                print(sumDBF(t,tasks,d),t)
                print("infeasible1")

                
                for h in range(len(tasks)):
                    print(y2[1][h].varName,y2[1][h].X)
                    print(a2[1][h].varName, a2[1][h].X)
                    print(b2[1][h].varName, b2[1][h].X)
                sys.exit()
            t=tasks[i]['period']-tasks[i]['sslength']-d[i].x
            if sumDBF(t,tasks,d)>t+0.1:
                print(tasks)
                for k in range(len(tasks)):        
                    print("tasks",k,d[k].x)
                print(sumDBF(t,tasks,d),t)
                print("infeasible1")
                sys.exit()

            
        return True
    #print(m.Status)
    return False

    

