import datetime
from board import Board
from greed import Greed


i = 0
#print(datetime.datetime.now())
n,m,k = map(int, input().split())

estadoInicial = []
fcInicial = ''
floodInicial = []
groupInicial = []
for i in range(n):
    linhaMatriz = list(map(str, input().split()))
    if fcInicial == '':
        fcInicial = linhaMatriz[0]
    for j in range(m): # coluna
        if linhaMatriz[j] == fcInicial :
            if floodInicial == [] :
                floodInicial.append((i, j))
            elif ((i, j-1) in floodInicial) or ((i-i, j) in floodInicial) : # coluna/linha anterior está na lista
                floodInicial.append((i, j))
        groupInicial.append([linhaMatriz[j], [(i, j)]])
    estadoInicial.append(linhaMatriz)

b = Board(line=n, size=m, color=k, board=estadoInicial, GROUPS=groupInicial, groupItems=True)
b.reset4()
p = Greed()
moves = []
i=0
while not b.isBoardOver():
    i+=1
    print(i)
    m = p.goToCenter(b)    
    b.move(m)    
    moves.append('a '+str(m))
    #b.print()
    if i % 10 == 0:
        print(*moves)    

print(i)
#print(datetime.datetime.now())
print(*moves)

#print('heuristica '+' hAB:'+str(b.H.count('hAB'))+' hBC:'+str(b.H.count('hBC'))+' hDA:'+str(b.H.count('hDA'))+' hCD:'+str(b.H.count('hCD'))+' hAC:'+str(b.H.count('hCD')))
#print(str(b.H))