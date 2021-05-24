import random

route=[]

# n=4
# K=2

n=100
K=10
# q=[2,1]

# c = [[0, 4, 2, 5, 6, 4, 3, 2, 5],[4, 0, 3, 2, 4, 6, 5, 7, 8],[1, 2, 0, 1, 1, 4, 3, 9, 5],[3, 2, 6, 0, 6, 5, 6, 1, 2],
#     [3, 4, 2, 5, 0, 9, 9, 7, 5],[2, 1, 3, 4, 2, 0, 4, 2, 2 ],[3, 2, 6, 5, 7, 8, 0, 4, 3],[2, 3, 2, 4, 5, 8, 7, 0, 4],[1, 1, 2, 3, 1, 6, 4, 6, 0]]

f=open('data_'+str(n)+'_'+str(K)+'.txt', 'r')

[n, K] = [int(x) for x in f.readline().split()]
q = [int(x) for x in f.readline().split()]
c=[[] for i in range(2*n+1)]
for i in range(2*n+1):
    c[i]=[int(x) for x in f.readline().split()]

#init
for i in range(K):
    route.append([])

top_K = []
start = [int(c[0][i]) for i in range(n+1)] # danh sách điểm đón
for k in range(K):
    minDis=10000
    for i in range(1, n+1):
        if(minDis>start[i]):
            minDis=start[i]
            choose=i

    route[k].append(choose)
    route[k].append(choose+n)

    top_K.append(choose)
    start[choose]=10000 # cho điểm đã đón có chi phí lớn để xe sau k chọn là điểm gần nhất

for i in range(1, n+1):
    if(i not in top_K):
        tmp1=random.randint(0,K-1)
        tmp2=random.randint(0, len(route[tmp1])-1)
        route[tmp1].insert(tmp2,i)
        route[tmp1].insert(random.randint(tmp2+1, len(route[tmp1])-1), i+n )
# print(route,"inti")
# exit()

def violation_k(k):# qua tai cua xe k // xe co bao nhieu nguoi
    tmp=0
    maxVal = 0
    person_lose = 0
    if len(route[k]) == 2:
        return 0, -1
    for i in range(len(route[k])):
        if(route[k][i]<n+1):
            tmp+=1
            if tmp > maxVal:
                maxVal = tmp
                person_lose = route[k][i]
        else:
            tmp-=1
    if(maxVal<q[k]):
        return 0, 0
    else:
        return maxVal-q[k], person_lose
        
def max_violation_k():# xe qua tai nhieu nhat
    #Nếu có nhiều xe cùng lỗi nhiều nhát, thì add vào 1 list và random ra 1 xe
    listBus = []
    tmp=0
    maxBus = 0
    # violation_lose = 0
    # person = 0
    k = 0
    per = 0
    for i in range(K):
        if(len(route[i])>0):
            k, per = violation_k(i)
            if k > tmp:
                maxBus = i
                listBus.clear()
                listBus.append(i)
                tmp = k
            if (k == tmp):
                listBus.append(i)
    
    return listBus[random.randint(0, len(listBus)-1)]


# ham try thoa man khong tao ra loi va giam chi phi
def cost():#hàm lỗi để tính toán, trả về 1000 là có xu thế k xóa đi điểm của xa đang không có khách
    cost=0
    for i in range(K):
        if len(route[i])==0:
            return 1000000
        cost=cost+c[0][route[i][0]]
        for j in range(len(route[i])-1):
            cost+=c[route[i][j]][route[i][j+1]]
        cost+=c[route[i][len(route[i])-1]][0]
    return cost

def cost2(): #hàm lỗi thực tế
    cost=0
    for i in range(K):
        if len(route[i])==0:
            continue
        cost=cost+c[0][route[i][0]]
        for j in range(len(route[i])-1):
            cost+=c[route[i][j]][route[i][j+1]]
        cost+=c[route[i][len(route[i])-1]][0]
    return cost

def add_i(k, i):    #them diem i vao xe k
    global preCost
    global costNow
    global preVio
    global vioNow

    #so lan lap lai thu ngau nhien trong vong while
    # turn=n*K*10
    minVal = 100000
    NotbusLocate = 0
    destination = 0
    busDes=0


    for j in range(len(route[k])):
        for l in range(j+1, len(route[k])):

            route[k].insert(j, i)
            route[k].insert(l, i+n)

            costNow=cost()
            vioNow, tmp3=violation_k(k)
            if vioNow<preVio:
                return
            if (minVal >= costNow):
                minVal=costNow
                NotbusLocate = int(j)
                busDes = int(l)
            route[k].remove(i)
            route[k].remove(i+n)

    if NotbusLocate==0 and busDes==0:
        route[k].insert(1, i+n)
        route[k].insert(0, i)

        return
    route[k].insert(NotbusLocate, i)
    route[k].insert(busDes, i+n)

        
        
def changeInside(k, per): #thay doi thu tu diem trong xe k
    # print('Goi ham IN')
    global preCost
    global costNow
    preCost=cost()


    route[k].remove(per)
    route[k].remove(per+n)
    add_i(k, per)
    
  
def changeOutside(k, per): #dao diem sang xe khac
    # print('Goi ham OUT')
    global preCost
    global costNow

    preCost=cost()
    r=[]
    for i in range(k):
        r.append(i)
    for i in range(k+1, K):
        r.append(i)

    bus=random.choice(r)
    # tmp=random.randint(0,len(route[bus]))

    route[k].remove(per)
    route[k].remove(per+n)
    add_i(bus, per)

def Try():
    
# tim route[] co chi phi lon nhat
    global preVio
    global vioNow
    k = max_violation_k()
    preVio, i = violation_k(k)
    # print(route[k], 'loi',i)
    if i == -1 :
        return
    if preVio==0:
        i = random.randint(0, len(route[k])-1)
        if route[k][i]>n:
            i=route[k][i]-n
        else:
            i=route[k][i]
# ramdom la dao 1 cap van trong xe do hay la chuyen sang xe khac
    tmp=random.randint(0, 10)
    if(tmp<4):
        changeInside(k, i)
    else:
        changeOutside(k, i)
print(cost2())
for i in range(1000):
    Try()
        
print(route)
print(cost2())
    
print(violation_k(max_violation_k()))
    
    


















        
    
