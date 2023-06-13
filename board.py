import random
import math
import sys
import string
import copy


class Board(object):

    #COLORS = string.ascii_uppercase
    # 20 digitos
    COLORS = list(map(str, range(1,21))) # "0123456789" # to-do pensar no cenário de 20 cores 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19

   
    COLOR_K = 0
    LAST_MOVE = None

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
            self.COLORNEIGHBOR = []
        else:
            self.COLORS = self.COLORS[0:color]#random.sample(self.COLORS, k=color)
            self.size = size
            self.line = line
            self.column = size
            self.board = board if len(board) != 0 else [[' ' for i in range(self.column)] for i in range(self.line)]
            self.FC = 0
            self.FLOODED = []
            self.GROUPS = []
            self.COLORNEIGHBOR = []
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
        self.LAST_MOVE = c
        for coor in self.FLOODED:
            x, y = coor
            self.board[x][y] = c
        #self.colorNeighbor(1)
        self.flood()

#---------------------------------------------
    def colorNeighbor(self, i):

        self.COLORNEIGHBOR = []
        # busca vizinhos
        for coor in self.FLOODED: 
            x, y = coor
            #direita
            if y + i < self.column: 
                if (self.FC != self.board[x][y + i]) and ( (self.board[x][y + i], (x,y+i)) not in self.COLORNEIGHBOR):
                    self.COLORNEIGHBOR.append([self.board[x][y + i], (x,y+i)])
            #abaixo
            if x + i < self.line: 
                if (self.FC != self.board[x + i][y]) and ( (self.board[x + i][y], (x+i,y)) not in self.COLORNEIGHBOR):
                    self.COLORNEIGHBOR.append([self.board[x + i][y], (x+i,y)])
            #esquerda
            if (self.FC != self.board[x][y - i]) and ( (self.board[x][y - i], (x,y-i)) not in self.COLORNEIGHBOR) and (y - i > 0) :
                self.COLORNEIGHBOR.append([self.board[x][y - i], (x,y-i)])
            #cima
            if (self.FC != self.board[x - i][y]) and ( (self.board[x - i][y], (x-i,y)) not in self.COLORNEIGHBOR) and (x - i > 0) :
                self.COLORNEIGHBOR.append([self.board[x - i][y], (x-i,y)])
        #remove duplicados
        self.COLORNEIGHBOR = [list(t) for t in set(tuple(row) for row in self.COLORNEIGHBOR)]
            


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
    
    #A cor vizinha mais frequente    
    def colorNeighborFreqMax(self):
        cores = list(map(lambda x: (x[0], len(x[1])), self.COLORNEIGHBOR))        
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
    def colorsInBoard(self):
        cores = list(set(map(lambda x: x[0], self.GROUPS)).difference(('' if not None else self.LAST_MOVE)))
        return cores
    
    def colorsInNEIGHBOR(self):
        cores = list(set(map(lambda x: x[0], self.COLORNEIGHBOR)).difference(('' if not None else self.LAST_MOVE)))
        return cores
    
    def coordInBoard(self):
        coresCoord = list(map(lambda x: x if (x[0] in self.COLORNEIGHBOR) and (x[0]  != self.LAST_MOVE)  else None, self.GROUPS))
        return list(filter(lambda x: x is not None, coresCoord ))
    
    # retorna apenas os grupos da cor atual
    def groupFilterFC(self):
        #coresCoord = list(map(lambda x: x if (x[0] == self.FC) else None, self.GROUPS))
        #list(filter(lambda x: x is not None, coresCoord ))
        groupFilter = [(i, x[1]) for i, x in enumerate(self.GROUPS) if x[0] == self.FC]
        return groupFilter
    
#---------------------------------------------
    def colorNearcenter(self):
        xc = self.line //2
        yc = self.column //2
        minD = (0,0,self.line)
        for c, coor in self.COLORNEIGHBOR:
            x, y = coor
            d = math.sqrt((xc - x) ** 2 + (yc - y) ** 2)
            if d < minD[2]:
                minD = (c, coor, d)
        return minD[0]


#---------------------------------------------

    # heuristica nó de estado possíveis
    def children(self):
        children = []
        for c in self.colorsInBoard(): # : para cada cor 
            if (c != self.FC)  : # se a cor for dirente da atual e diferente da ultima escolhida 
                child = Board(orig=self) # gera um tabuleiro com o cenário atual
                child.move(c) # troca a cor atual pela nova cor
                if (len(child.GROUPS) < len(self.GROUPS)): # ) and (len(child.FLOODED) > len(self.FLOODED)) verifica se o grupo de cores direntes do nó aberto é menor que o nó
                    children.append((child, c)) # então adiciona o nó aberto  
                elif len(child.FLOODED)+len(child.GROUPS) == len(self.GROUPS) + len(self.FLOODED):
                    children.append((child, c)) 
        return children
        
    # heuristica nó de estado possíveis
    def childrenNei(self):
        children = []
        self.colorNeighbor(1)
        c = self.colorNeighborFreqMax()
        if (c != self.FC) : 
            child = Board(orig=self) 
            child.move(c)
            children.append((child, c)) 
        return children

    # filho com a maior posição vizinha
    def childrenMax(self):
        children = []
        self.colorNeighbor(1)
        coorMax = max(enumerate(self.COLORNEIGHBOR), key=lambda x: x[1][1])
        c = coorMax[1][0]
        if (c != self.FC): 
            child = Board(orig=self) # gera um tabuleiro com o cenário atual
            child.move(c) # troca a cor atual pela nova cor
            children.append((child, c)) 
        return children
    
    # filho mais próximo do centro
    def childrenCenter(self):
        children = []
        self.colorNeighbor(1)
        c = self.colorNearcenter()
        if (c != self.FC): 
            child = Board(orig=self) # gera um tabuleiro com o cenário atual
            child.move(c) # troca a cor atual pela nova cor
            children.append((child, c)) 
        return children
#---------------------------------------------

    # estado objetivo - ou seja, sem grupo de cores
    def isOver(self):
        if len(self.GROUPS) == 0:
            return True
        else:
            return False


#---------------------------------------------
    def scoreNeigh(self):
        return len(self.COLORNEIGHBOR)

    def score(self):
        return len(self.GROUPS)

    def scoree(self):
        return len(self.FLOODED)
    #
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
            for coor in self.FLOODED:
                x, y = coor
                for n, g in enumerate(self.groupFilterFC()): # percorre o mapeamento inicial de groups
                    #if self.FC == g[0]: # a cor inicial é a cor do grupo 
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
                del self.GROUPS[g[0]]#self.GROUPS[n]


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
