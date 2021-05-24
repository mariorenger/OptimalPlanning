import random
import math

# def distance(i, j, l ,m):
# 	return 
# def genData(n, K):

# 	with open('data_'+str(n)+'_'+str(k)+'.txt', 'w') as f:
# 		data=[][]
# 		for i in range(2*n+1):
# 			data[0][i]=ra
# 	    for line in lines:
# 	        f.write(line)
# 	        f.write('\n')
n=150
K=30
# bị 3 điểm thẳng hàng
def distance(i1, j1, i2, j2):
	return int(math.sqrt((i1-i2)*(i1-i2)+(j1-j2)*(j1-j2)))+1

# sinh các điểm trên vòng tròn để không có 3 điểm nào thẳng hàng
point=[[100*math.cos(i*2*math.pi/(2*n+1)), 100*math.sin(i*2*math.pi/(2*n+1))] for i in range(2*n+1)] 
# print(point)
# đảo ngẫu nhiên vị trí các điểm trong dãy điểm
for i in range(n*2):
	tmp=random.randint(0, len(point)-1)
	remove=point[tmp]
	point.remove(point[tmp])
	point.append(remove)

# print(point)

c=[[0 for i in range(2*n+1)] for j in range(2*n+1)]
for i in range(2*n+1):
	for j in range(2*n+1):
		if j!=i:
			c[i][j]=distance(point[i][0], point[i][1], point[j][0], point[j][1])
# print(c)
q=[random.randint(1, int(n/K)) for i in range(K) ]
with open('data_'+str(n)+'_'+str(K)+'.txt', 'w') as f:
	f.writelines(str(n)+ ' '+str(K)+' '+'\n')
	for i in range(K):
		f.write(str(q[i])+' ')
	f.write('\n')
	for i in range(2*n+1):
		for j in range(2*n+1):
			f.write(str(c[i][j])+' ')
		f.write('\n')

# f=open('data_'+str(n)+'_'+str(K)+'.txt', 'r')

# [n, K] = [int(x) for x in f.readline().split()]
# q = [int(x) for x in f.readline().split()]
# c=[[] for i in range(2*n+1)]
# for i in range(2*n+1):
# 	c[i]=[int(x) for x in f.readline().split()]

# print(n, K)
# print(q)
# print(c)