from board import Board
from greed import Greed

i = 0

n,m,k = map(int, input().split())

estadoInicial = []
for i in range(n):
    linhaMatriz = list(map(str, input().split()))
    estadoInicial.append(linhaMatriz)

b = Board(line=n, size=m, color=k, board=estadoInicial)
b.print()
    
p = Greed()

while not b.isOver():
    i+=1
    print(i)
    m = p.findMove(b)
    print(m)
    b.move(m)
    b.print()