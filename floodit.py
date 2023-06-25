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
    m = p.borders2(b)
    #print(m)
    b.LAST_MOVE_PEN = moves[-1][2] if len(moves) > 0 else b.FC
    b.move(m)
    #if len(b.GROUPS) > 0:
    #    if (b.GROUPS[0][1] == [(0,0)]) and (b.GROUPS[0][0] != b.FC):
    #        del b.GROUPS[0] # remove a primeira posição para atualizar o group
    #if len(moves) > 100 and ( moves[len(moves)-3 : len(moves)-1] == [moves[len(moves)-1], 'a '+str(m)] ):
    #    print('........................Verificar')
        #print(*moves)
    if len(moves) == 350:
        print('check')
    moves.append('a '+str(m))
    #b.print()
    #if i % 10 == 0:
        #b.print()        
    #    print(*moves)
    #    print('heuristica usada até o passo 100 '+' h4:'+str(b.H.count('h4'))+' h5:'+str(b.H.count('h5'))+' hAB:'+str(b.H.count('hAB'))+' hBC:'+str(b.H.count('hBC'))+' hDA:'+str(b.H.count('hDA'))+' hCD:'+str(b.H.count('hCD'))+' hAC:'+str(b.H.count('hCD')))
        #break

print(i)
#print(datetime.datetime.now())
print(*moves)

#print('heuristica '+' hAB:'+str(b.H.count('hAB'))+' hBC:'+str(b.H.count('hBC'))+' hDA:'+str(b.H.count('hDA'))+' hCD:'+str(b.H.count('hCD'))+' hAC:'+str(b.H.count('hCD')))
#print(str(b.H))