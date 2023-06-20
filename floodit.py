from board import Board
from greed import Greed

i = 0

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
p = Greed()
moves = []
i=0
while not b.isOver():
    i+=1
    #print(i)
    m = p.goToCenter(b)
    #print(m)
    b.move(m)    
    moves.append('a '+str(m))    
    #if i== 100:
        #b.print()
        #print('heuristica usada até o passo 100 '+' hAB:'+str(b.H.count('hAB'))+' hBC:'+str(b.H.count('hBC'))+' hDA:'+str(b.H.count('hDA'))+' hCD:'+str(b.H.count('hCD'))+' hAC:'+str(b.H.count('hCD')))
        #break

print(i)
#print(len(moves))
print(*moves)
#print('heuristica '+' hAB:'+str(b.H.count('hAB'))+' hBC:'+str(b.H.count('hBC'))+' hDA:'+str(b.H.count('hDA'))+' hCD:'+str(b.H.count('hCD'))+' hAC:'+str(b.H.count('hCD')))
#print(str(b.H))