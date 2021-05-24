import numpy as np
from ortools.sat.python import cp_model
import time


# n=4
# K=2

# q=[2,1]

# c = [[0, 4, 2, 5, 6, 4, 3, 2, 5],[4, 0, 3, 2, 4, 6, 5, 7, 8],[1, 2, 0, 1, 1, 4, 3, 9, 5],[3, 2, 6, 0, 6, 5, 6, 1, 2],
#     [3, 4, 2, 5, 0, 9, 9, 7, 5],[2, 1, 3, 4, 2, 0, 4, 2, 2 ],[3, 2, 6, 5, 7, 8, 0, 4, 3],[2, 3, 2, 4, 5, 8, 7, 0, 4],[1, 1, 2, 3, 1, 6, 4, 6, 0]]


n=7
K=2
# q=[2,1]

# c = [[0, 4, 2, 5, 6, 4, 3, 2, 5],[4, 0, 3, 2, 4, 6, 5, 7, 8],[1, 2, 0, 1, 1, 4, 3, 9, 5],[3, 2, 6, 0, 6, 5, 6, 1, 2],
#     [3, 4, 2, 5, 0, 9, 9, 7, 5],[2, 1, 3, 4, 2, 0, 4, 2, 2 ],[3, 2, 6, 5, 7, 8, 0, 4, 3],[2, 3, 2, 4, 5, 8, 7, 0, 4],[1, 1, 2, 3, 1, 6, 4, 6, 0]]
# đọc dữ liệu 
f=open('data_'+str(n)+'_'+str(K)+'.txt', 'r')

[n, K] = [int(x) for x in f.readline().split()]
q = [int(x) for x in f.readline().split()]
c=[[] for i in range(2*n+1)]
for i in range(2*n+1):
    c[i]=[int(x) for x in f.readline().split()]


solver = cp_model.CpSolver()

d=[[0 for i in range(2*n+2*K+1)] for j in range(2*n+2*K+1)]

for i in range(2*n+1):
    for j in range(2*n+1):
        d[i][j]=c[i][j]

for i in range(2*n+1,2*n+K+1):
    for j in range(2*n+1):
        d[i][j]= c[0][j]

for i in range(2*n+K+1,2*n+2*K+1):
    for j in range(2*n+1):
        d[j][i]= c[j][0]
print(d)
model = cp_model.CpModel()

x=[model.NewIntVar(0, 2*n+2*K, 'x'+str(i)) for i in range(2*n+K+1)]
model.Add(x[0]==0)
y=[model.NewIntVar(1, K, 'y'+str(i)) for i in range(2*n+2*K+1)]#xe
cost=[model.NewIntVar(0, 100000, 'cost'+str(i)) for i in range(2*n+2*K+1)]
numCustommer=[model.NewIntVar(0, n, 'customer'+str(i)) for i in range(2*n+2*K+1)]

for i in range(2*n+1, 2*n+K+1):
    model.Add(cost[i]==0)
    model.Add(numCustommer[i]==0)

#diem dau va diem cuoi
for i in range(K):
    model.Add(y[2*n+i+1]==y[2*n+i+K+1])
for i in range(K):
    model.Add(y[2*n+i+1]==i+1)

model.AddAllDifferent(x)

for i in range(1, 2*n+K+1):
    model.Add(x[i]!=i)

#diem o giua khong di den diem dau
for i in range(1, 2*n+1):
    for j in range(2*n+1, 2*n+K+1):
        model.Add(x[i] != j)

for i in range(K):
    model.Add(x[2*n+i+1]<=2*n)
b={}
for i in range(1, 2*n+1+K):
    for j in range(1, n+1):
        b[i, j] = model.NewBoolVar('b['+str(i)+', '+str(j)+']')
        model.Add(x[i]==j).OnlyEnforceIf(b[i, j])
        model.Add(x[i]!=j).OnlyEnforceIf(b[i, j].Not())
        
        model.Add(y[i]==y[j]).OnlyEnforceIf(b[i, j])
        model.Add(cost[j]==cost[i]+d[i][j]).OnlyEnforceIf(b[i, j])
        model.Add(numCustommer[j]==numCustommer[i]+1).OnlyEnforceIf(b[i, j])

for i in range(1, 2*n+K+1):
    for j in range(n+1, 2*n+1):
        b[i, j] = model.NewBoolVar('b['+str(i)+', '+str(j)+']')
        model.Add(x[i]==j).OnlyEnforceIf(b[i, j])
        model.Add(x[i]!=j).OnlyEnforceIf(b[i, j].Not())
        
        model.Add(y[i]==y[j]).OnlyEnforceIf(b[i, j])
        model.Add(cost[j]==cost[i]+d[i][j]).OnlyEnforceIf(b[i, j])
        model.Add(numCustommer[j]==numCustommer[i]-1).OnlyEnforceIf(b[i, j])

for i in range(1, 2*n+1):
    for j in range(2*n+K+1, 2*n+2*K+1):
        b[i, j] = model.NewBoolVar('b['+str(i)+', '+str(j)+']')
        model.Add(x[i]==j).OnlyEnforceIf(b[i, j])
        model.Add(x[i]!=j).OnlyEnforceIf(b[i, j].Not())
        
        model.Add(y[i]==y[j]).OnlyEnforceIf(b[i, j])
        model.Add(cost[j]==cost[i]+d[i][j]).OnlyEnforceIf(b[i, j])


for i in range(1, n+1):
    model.Add(cost[i]<cost[i+n])
    model.Add(y[i]==y[i+n])
# diem cuoi cost cua nhung diem cuoi la lon nhat?


b1={}
for i in range(1, 2*n+1):
    for k in range(K):
        b1[i] = model.NewBoolVar('b1['+str(i)+']')
        model.Add(y[i]==k+1).OnlyEnforceIf(b1[i])
        model.Add(y[i]!=k+1).OnlyEnforceIf(b1[i].Not())

        model.Add(numCustommer[i]<=q[k]).OnlyEnforceIf(b1[i])



# y[i]=k thi numCustommer[i]<q[k]

t = model.NewIntVar(0, 100000,'AllCost')

model.Add(t==(sum(cost[i] for i in range(2*n+K+1, 2*n+2*K+1))))

model.Minimize(t)

solver = cp_model.CpSolver()


status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    print(solver.Value(t))

    for i in range(1, 2*n+K+1):
        print(i, solver.Value(x[i]),solver.Value(y[i]))

    for i in range(1, 2*n+K+1):
    	print(i, solver.Value(numCustommer[i]))





















 















