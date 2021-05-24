import random

route=[]
listCustomers=[]

n=150
K=15
# q=[2,1]

# c = [[0, 4, 2, 5, 6, 4, 3, 2, 5],[4, 0, 3, 2, 4, 6, 5, 7, 8],[1, 2, 0, 1, 1, 4, 3, 9, 5],[3, 2, 6, 0, 6, 5, 6, 1, 2],
#     [3, 4, 2, 5, 0, 9, 9, 7, 5],[2, 1, 3, 4, 2, 0, 4, 2, 2 ],[3, 2, 6, 5, 7, 8, 0, 4, 3],[2, 3, 2, 4, 5, 8, 7, 0, 4],[1, 1, 2, 3, 1, 6, 4, 6, 0]]

f=open('data_'+str(n)+'_'+str(K)+'.txt', 'r')

[n, K] = [int(x) for x in f.readline().split()]
q = [int(x) for x in f.readline().split()]
c=[[] for i in range(2*n+1)]
for i in range(2*n+1):
    c[i]=[int(x) for x in f.readline().split()]

busPosition=[0 for i in range(K)]
Cost=0
#init
for i in range(K):
    route.append([])
    listCustomers.append([])

top_K = []
start = [int(c[0][i]) for i in range(n+1)] # danh sách điểm đón

# K xe đi đón K khách gần nhất
for k in range(K):
    minDis=10000
    for i in range(1, n+1):
        if(minDis>start[i]):
            minDis=start[i]
            choose=i

    route[k].append(choose)
    listCustomers[k].append(choose)
    busPosition[k]=choose

    Cost+=minDis

    top_K.append(choose)
    start[choose]=10000 # cho điểm đã đón có chi phí lớn để xe sau k chọn là điểm gần nhất

# print(top_K)
def chooseBus(i):
	global Cost
	minDistance=10000
	bus=-1
	gainCost=0
	for k in range(K):
		# minDistance=min(minDistance, c[busPosition[k]][i])
		if(minDistance>c[busPosition[k]][i]):
			minDistance=c[busPosition[k]][i]
			gainCost=c[busPosition[k]][i]
			bus=k

	busPosition[bus]=i
	Cost+=gainCost
	listCustomers[bus].append(i)
	route[bus].append(i)

	return bus

def checkBus(k):	
	global Cost
	minDistance=10000
	place=-1
	# print(listCustomers)
	# print(route, 'duong di')
	if (len(listCustomers[k])==q[k]):
		for i in range(len(listCustomers[k])):
			if minDistance>c[busPosition[k]][listCustomers[k][i]+n]:
				minDistance=c[busPosition[k]][listCustomers[k][i]+n]
				place=listCustomers[k][i]+n

		busPosition[k]=place
		Cost+=minDistance
		listCustomers[k].remove(place-n)
		route[k].append(place)

# chọn xe gần nhất , check xem xe đó đã đầy chưa
for i in range(1, n+1):
	if(i not in top_K):
		k=chooseBus(i)
		checkBus(k)

for k in range(K):
	while len(listCustomers[k])!=0:
		minDistance=10000
		for i in range(len(listCustomers[k])):
			if minDistance>c[busPosition[k]][listCustomers[k][i]+n]:
				minDistance=c[busPosition[k]][listCustomers[k][i]+n]
				place=listCustomers[k][i]+n

		busPosition[k]=place
		Cost+=minDistance
		listCustomers[k].remove(place-n)
		route[k].append(place)

for k in range(K):
	Cost+=c[busPosition[k]][0]

print(route)	
print(Cost)	




