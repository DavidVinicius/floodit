import random
import math
import sys
import string
import copy


class Board(object):

    #COLORS = string.ascii_uppercase
    # 20 digitos
    COLORS = list(map(str, range(1,21))) # "0123456789" # to-do pensar no cenário de 20 cores 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19

    COLORNEIGHBOR = ""
    COLOR_K = 0

    def __init__(self, orig=None, size=10, color=4, line=10, board=[]):


        self.COLOR_K = color
        
        if orig:
            self.COLORS = copy.deepcopy(orig.COLORS)
            self.size = orig.size
            self.line = orig.line
            self.column = orig.column
            self.board = copy.deepcopy([list(col) for col in orig.board])
            self.FC = copy.deepcopy(orig.FC)
            self.FLOODED = copy.deepcopy(orig.FLOODED)
            self.GROUPS = copy.deepcopy(orig.GROUPS)
        else:
            self.COLORS = self.COLORS[0:color]#random.sample(self.COLORS, k=color)
            self.size = size
            self.line = line
            self.column = size
            self.board = board if len(board) != 0 else [[' ' for i in range(self.column)] for i in range(self.line)]
            self.FC = 0
            self.FLOODED = []
            self.GROUPS = []
            self.reset()

    # passo 1 - ler o arquivo do mapa e mapear quais os grupos iniciais 
    def reset(self):
        for i in range(self.line): # linha
            for j in range(self.column): # coluna
                # get a random color
                #tempc = self.COLORS[random.randrange(len(self.COLORS))]

                # set the color for this block
                #self.board[i][j] = tempc
                temp_color = self.board[i][j]
                self.GROUPS.append([temp_color, [(i, j)]])


        # grouping
        while True:
            done = True
            for n, g in enumerate(self.GROUPS): # para cada grupo
                for coor in g[1]: # extrai a coordenada 0,0 tendo 'B', [(0,0)]
                    x, y = coor # não daria para colocar um  if (y > 0 or (x > 0), assim evita percorrer o for da linha 52, para ficar verificando parando no if da linha 54
                    for m, gg in enumerate(self.GROUPS): # percorre todos os grupos
                        if n != m and g[0] == gg[0]: # se indices diferentes( n != m) mas com cor igual (g[0] ==gg[00])
                            if (y > 0 and (x, y-1) in gg[1]) or (x > 0 and (x-1, y) in gg[1]):
                                if n < m:
                                    tempg = g
                                    tempg[1] = tempg[1] + gg[1]
                                    keep = n
                                    dele = gg
                                if n > m:
                                    tempg = gg
                                    tempg[1] = tempg[1] + g[1]
                                    keep = m
                                    dele = g
                                done = False
                                break
                    if not done:
                        break
                if not done:
                    break
            if done:
                break
            else:
                self.GROUPS[keep] = tempg
                self.GROUPS.remove(dele)

        self.FC = self.GROUPS[0][0]
        self.FLOODED = self.GROUPS[0][1]
        del self.GROUPS[0]



#---------------------------------------------


    def hash(self):
        output = ""
        #for i in range(len(self.GROUPS)+1):
        for g in self.GROUPS:
            output += g[0] + str(g[1][0])
                #output = output << 2
        return output


#---------------------------------------------


    def move(self, c):
        self.FC = c
        self.COLORNEIGHBOR = ""
        for coor in self.FLOODED:
            x, y = coor
            self.board[x][y] = c
            #busca vizinhos
            #direita
            if y + 1 < self.column: 
                if (self.FC != self.board[x][y + 1]) and (self.board[x][y + 1] not in self.COLORNEIGHBOR):
                    self.COLORNEIGHBOR += self.board[x][y + 1]
            #abaixo
            if x + 1 < self.line: 
                if (self.FC != self.board[x + 1][y]) and (self.board[x + 1][y] not in self.COLORNEIGHBOR):
                    self.COLORNEIGHBOR += self.board[x + 1][y]
            #esquerda
            if (self.FC != self.board[x][y - 1]) and (self.board[x][y - 1] not in self.COLORNEIGHBOR) and (y - 1 > 0) :
                self.COLORNEIGHBOR += self.board[x][y - 1] 
            #cima
            if (self.FC != self.board[x - 1][y]) and (self.board[x - 1][y] not in self.COLORNEIGHBOR) and (x - 1 > 0) :
                self.COLORNEIGHBOR += self.board[x - 1][y] 
        self.flood()

#---------------------------------------------
    def colorNeighbor(self):

        self.COLORNEIGHBOR = ""
        # busca vizinhos
        for coor in self.FLOODED: 
            x, y = coor
            #direita
            if y + 1 < self.column: 
                if (self.FC != self.board[x][y + 1]) and (self.board[x][y + 1] not in self.COLORNEIGHBOR):
                    self.COLORNEIGHBOR += self.board[x][y + 1]
            #abaixo
            if x + 1 < self.line: 
                if (self.FC != self.board[x + 1][y]) and (self.board[x + 1][y] not in self.COLORNEIGHBOR):
                    self.COLORNEIGHBOR += self.board[x + 1][y]
            #esquerda
            if (self.FC != self.board[x][y - 1]) and (self.board[x][y - 1] not in self.COLORNEIGHBOR) and (y - 1 > 0) :
                self.COLORNEIGHBOR += self.board[x][y - 1] 
            #cima
            if (self.FC != self.board[x - 1][y]) and (self.board[x - 1][y] not in self.COLORNEIGHBOR) and (x - 1 > 0) :
                self.COLORNEIGHBOR += self.board[x - 1][y] 

    #A cor mais frequente na borda    
    def colorNeighborFreq(self):
        cores = list(map(lambda x: (x[0], len(x[1])), self.GROUPS))        
        coresDict = {}
        maxValue = (0,0)
        for cor, qtd in cores:
            coresDict[cor] = coresDict.get(cor, 0) + qtd
            if coresDict[cor] > maxValue[1]:
                maxValue = (cor, coresDict[cor])
        return maxValue[0]
    
    def quantityColors(self):
        cores = list(map(lambda x: x[0], self.GROUPS))
        return len(set(cores))
      
#---------------------------------------------
    def nearcenter(self):
          xc = (self.line//2) - 1 if self.line//2 >=1 else self.line//2
          yc = (self.column//2) - 1 if self.column//2 >=1 else self.column//2
          xm = ""
          ym = ""
          for coor in self.FLOODED: 
            x, y = coor
            if(xm == "" and ym == ""):
                xm = x
                ym = y
            else:
                dx = xc - x 
                dy = yc - y
                if(dx < (xc - xm)) and (dy < (yc - ym)):
                    xm = x
                    ym = y
            
            if (xm < xc) and (ym < yc):
                return xc - xm
            else:
                return xm - xc

#---------------------------------------------

    # heuristica nó de estado possíveis
    def children(self):
        children = []
        #self.COLORNEIGHBOR
        for c in self.COLORS: # : para cada cor 
            if c != self.FC: # se a cor for dirente da atual 
                child = Board(orig=self) # gera um tabuleiro com o cenário atual
                child.move(c) # troca a cor atual pela nova cor
                if (len(child.GROUPS) < len(self.GROUPS)): # ) and (len(child.FLOODED) > len(self.FLOODED)) verifica se o grupo de cores direntes do nó aberto é menor que o nó
                    children.append((child, c)) # então adiciona o nó aberto  
        return children
        

#---------------------------------------------

    # estado objetivo - ou seja, sem grupo de cores
    def isOver(self):
        if len(self.GROUPS) == 0:
            return True
        else:
            return False


#---------------------------------------------


    def score(self):
        return len(self.GROUPS)

    def scoree(self):
        return len(self.FLOODED)


#---------------------------------------------


    # merge adjacent same color groups in larger group and update self.GROUPS
    # continues to check until no update is made, then break the loop. 
    # mescla grupos adjacentes da mesma cor em um grupo maior e atualiza self.GROUPS
    # continua verificando até que nenhuma atualização seja feita, então quebre o loop.
    def flood(self):

        while True:
            done = True
            for coor in self.FLOODED: # todo mudar para comparar somente a borda
                x, y = coor
                for n, g in enumerate(self.GROUPS): # percorre o mapeamento inicial de groups
                    if self.FC == g[0]: # a cor inicial é a cor do grupo 
                        if (y < self.column and (x, y+1) in g[1]) or (x <= self.line and (x+1, y) in g[1]):
                            tempg = g[1]#self.GROUPS[0]
                            #tempg[1] = tempg[1] + g[1]
                            done = False
                            break
                if not done:
                    break
            if done:
                break
            else:
                self.FLOODED += tempg#self.GROUPS[0][1] += tempg
                del self.GROUPS[n]


#---------------------------------------------


    def print(self):
        print()
        print('+' + '---+' * self.column)
        for i in range(self.line):
            row = '|'
            for j in range(self.column):
                row += ' ' + str(self.board[i][j]) + ' |'
            print(row)
            print('+' + '---+' * self.column)
        print()

    def show(self):
        print(self.FC)
        print(self.FLOODED)
        print(len(self.GROUPS))
        print(self.GROUPS)

      

if __name__ == "__main__":
    
    b = Board(size=10, color=4, line=10)
    #b.reset()
    b.show()
    b.print()
    i = 0
    while not b.isOver():
        inp = input("Input the color: ")
        if inp.upper() in b.COLORS:
            b.move(inp.upper())
            i += 1
            print("Moves: " + str(i))
            b.print()
        else:
            print("Invalid input. ")
