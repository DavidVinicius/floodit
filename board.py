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
    LAST_MOVE_X = 0
    LAST_MOVE_Y = 0
    LAST_MOVE_I = 0
    LAST_MOVE_H = None
    X_DONE = 0
    XY_DONE = 0
    Y_DONE = 0
    XX_DONE = 1
    K_STEP = 2
    START_X = 0
    STOP_X = 0
    START_Y = 0
    STOP_Y = 0

    def __init__(self, orig=None, size=10, color=4, line=10, board=[], GROUPS = None, groupItems = True):


        self.COLOR_K = color
        self.groupItems = groupItems

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
            self.H = []
            self.COLORX = []
            self.COLORY = []
            self.COLORM = []
            self.resetQTD = 0
            self.GROUPS0 = copy.deepcopy(orig.GROUPS)
            self.STOP_X = orig.column//2
            self.STOP_Y = orig.line//3
        else:
            self.COLORS = self.COLORS[0:color]#random.sample(self.COLORS, k=color)
            self.size = size
            self.line = line
            self.column = size
            self.board = board if len(board) != 0 else [[' ' for i in range(self.column)] for i in range(self.line)]
            self.FC = 0
            self.FLOODED = []
            self.GROUPS = [] if GROUPS is None else GROUPS
            self.COLORNEIGHBOR = []
            self.H = []
            self.COLORX = []
            self.COLORY = []
            self.COLORM = []
            self.resetQTD = 0
            self.GROUPS0 = []
            self.STOP_X = size//2
            self.STOP_Y = line//3
            #self.reset()

    # passo 1 - ler o arquivo do mapa e mapear quais os grupos iniciais 
    def reset(self):
        #for i in range(self.line): # linha
        #    for j in range(self.column): # coluna
        #        temp_color = self.board[i][j]
        #        self.GROUPS.append([temp_color, [(i, j)]])
          
        # grouping
        MAX_INTERATIONS = 2
        i = 0
        while True or i <= MAX_INTERATIONS:
            done = True
            for n, g in enumerate(self.GROUPS): # para cada grupo
                #print(n,g)
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
            i += 1
            if done:
                break
            else:
                self.GROUPS[keep] = tempg
                self.GROUPS.remove(dele)        
        self.FC = self.GROUPS[0][0]
        self.FLOODED = self.GROUPS[0][1]
        del self.GROUPS[0]

    def reset2(self):
        #for i in range(self.line):
        #    for j in range(self.column):
        #        temp_color = self.board[i][j]
        #        self.GROUPS.append([temp_color, [(i, j)]])

        if len(self.GROUPS) > 100:
            self.GROUPS0 = copy.deepcopy(self.GROUPS)
            self.GROUPS= self.groupFilterM(2) #self.groupFilterK(100)

        done = False

        while not done:
            done = True
            for n, g in enumerate(self.GROUPS):
                for coor in g[1]:
                    x, y = coor
                    if y > 0 or x > 0:
                        for m, gg in enumerate(self.GROUPS):
                            if n != m and g[0] == gg[0]:
                                if (y > 0 and (x, y - 1) in gg[1]) or (x > 0 and (x - 1, y) in gg[1]):
                                    if n < m:
                                        tempg = g
                                        tempg[1] += gg[1]
                                        keep = n
                                        dele = gg
                                    if n > m:
                                        tempg = gg
                                        tempg[1] += g[1]
                                        keep = m
                                        dele = g
                                    done = False
                                    break
                        if not done:
                            break
                if not done:
                    break

            if not done:
                self.GROUPS[keep] = tempg
                self.GROUPS = [group for idx, group in enumerate(self.GROUPS) if idx != self.GROUPS.index(dele)]
                if len(self.GROUPS0) > 0:
                    self.GROUPS0[keep] = tempg
                    self.GROUPS0 = [group for idx, group in enumerate(self.GROUPS0) if idx != self.GROUPS0.index(dele)]

        self.FC = self.GROUPS[0][0]
        self.FLOODED = self.GROUPS[0][1]
        del self.GROUPS[0]
        if len(self.GROUPS0) > 0:
            del self.GROUPS0[0]

    def reset3(self):
        #for i in range(self.line): # linha
        #    for j in range(self.column): # coluna
        #        temp_color = self.board[i][j]
        #        self.GROUPS.append([temp_color, [(i, j)]])
          
        # grouping

        done = False

        while not done:
            done = True
            new_groups = []

            for n, g in enumerate(self.GROUPS):
                if not any((x > 0 and (x-1, y) in g[1]) or (y > 0 and (x, y-1) in g[1]) for x, y in g[1]): # verifica se o g não está conectado a outro grupo, ou seja sem vizinho a esquerda ou direita
                    new_groups.append(g)
                    continue
                    #(x > 0 and (x-1, y) in g[1]): Verifica se existe uma coordenada à esquerda da coordenada atual (x, y) do g[1]
                    #(y > 0 and (x, y-1) in g[1]): Verifica se existe uma coordenada acima da coordenada atual (x, y) do g[1]
                for x, y in g[1]:
                    for m, gg in enumerate(self.GROUPS):
                        if n != m and g[0] == gg[0] and ((x > 0 and (x-1, y) in gg[1]) or (y > 0 and (x, y-1) in gg[1])):
                            if n < m:
                                g[1].extend(gg[1])
                            else:
                                g = gg
                                g[1].extend(new_groups[n][1])
                            done = False
                            break
                    if not done:
                        break

                new_groups.append(g)

            self.GROUPS = new_groups

        self.FC = self.GROUPS[0][0]
        self.FLOODED = self.GROUPS[0][1]
        del self.GROUPS[0]


    def reset4(self):
        # grouping        
        adds = []
        for n, g in enumerate(self.GROUPS):
            for coor in g[1]:
                x, y = coor
                for m, gg in enumerate(self.GROUPS):
                    if n != m and g[0] == gg[0]:
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
                            
                            self.GROUPS[keep] = tempg
                            if dele in self.GROUPS:
                                self.GROUPS.remove(dele)
                            # adds.append({
                            #     'keep': keep,
                            #     'tempg': tempg,
                            #     'dele': dele
                            # })
        #print(adds)
        # for item in adds:        
        #     print(item)
        #     self.GROUPS[item.get('keep')] = item.get('tempg')
        #     if item.get('dele') in self.GROUPS:
        #         self.GROUPS.remove(item.get('dele'))

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
        self.flood2()

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
            
#---------------------------------------------
    def colorNeighborGROUPS(self, k):

        self.COLORNEIGHBORGROUPS = []
        # busca vizinhos
        for i in range(k):
            for coor in self.FLOODED: 
                x, y = coor
                #direita
                if y + i < self.column: 
                    if (self.FC != self.board[x][y + i]) and ( (self.board[x][y + i], (x,y+i)) not in self.COLORNEIGHBORGROUPS):
                        self.COLORNEIGHBORGROUPS.append([self.board[x][y + i], (x,y+i)])
                #abaixo
                if x + i < self.line: 
                    if (self.FC != self.board[x + i][y]) and ( (self.board[x + i][y], (x+i,y)) not in self.COLORNEIGHBORGROUPS):
                        self.COLORNEIGHBORGROUPS.append([self.board[x + i][y], (x+i,y)])
                #esquerda
                if (self.FC != self.board[x][y - i]) and ( (self.board[x][y - i], (x,y-i)) not in self.COLORNEIGHBORGROUPS) and (y - i > 0) :
                    self.COLORNEIGHBORGROUPS.append([self.board[x][y - i], (x,y-i)])
                #cima
                if (self.FC != self.board[x - i][y]) and ( (self.board[x - i][y], (x-i,y)) not in self.COLORNEIGHBORGROUPS) and (x - i > 0) :
                    self.COLORNEIGHBORGROUPS.append([self.board[x - i][y], (x-i,y)])
        #remove duplicados
        self.COLORNEIGHBORGROUPS = [list(t) for t in set(tuple(row) for row in self.COLORNEIGHBORGROUPS)]
            


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
    
    # retorna apenas os grupos da cor atual
    def groupFilterFC2(self):
        #coresCoord = list(map(lambda x: x if (x[0] == self.FC) else None, self.GROUPS))
        #list(filter(lambda x: x is not None, coresCoord ))
        groupFilter = [(i, x) for i, x in enumerate(self.GROUPS) if x[0] == self.FC]
        return groupFilter
    
    # retorna apenas os grupos k primeiros grupos
    def groupFilterK(self, k):
        return [self.GROUPS0[i] for i in range(len(self.GROUPS0)) if (self.GROUPS0[i][1][0][0] > 0) and (self.GROUPS0[i][1][0][1] > 0) and (i < k) ]
    
    #retorna apenas os grupos com coordenadas menores ou igual ao delimitador em tabuleiro divido por k 
    def groupFilterM(self, k):
        return [self.GROUPS0[i] for i in range(len(self.GROUPS0)) if (self.GROUPS0[i][1][0][0] <= self.GROUPS0[-1][1][0][0]//k) and (self.GROUPS0[i][1][0][1] <= self.GROUPS0[-1][1][0][1]//k) ]
  
#---------------------------------------------
    def colorNearcenter(self):
        xc = self.line //2
        yc = self.column //2
        minD = (0,0,self.line-1)
        for c, coor in self.COLORNEIGHBOR:
            x, y = coor
            d = math.sqrt((xc - x) ** 2 + (yc - y) ** 2)
            if d < minD[2]:
                minD = (c, coor, d)
        return minD[0]

#---------------------------------------------
    def colorNearHalf(self):
        xc = self.line //2
        yc = self.column -1
        minD = (0,0,self.line-1)
        for c, coor in self.COLORNEIGHBOR:
            x, y = coor
            d = math.sqrt((xc - x) ** 2 + (yc - y) ** 2)
            if d < minD[2]:
                minD = (c, coor, d)
        return minD[0]
#---------------------------------------------
    def colorNearY(self):
        xc = self.line -1
        yc = self.column -1
        minD = (0,0,xc*yc)
        for c, coor in self.COLORNEIGHBOR:
            x, y = coor
            d = math.sqrt((xc - x) ** 2 + (yc - y) ** 2)
            if d < minD[2]:
                minD = (c, coor, d)
        return minD[0]
#---------------------------------------------
    def colorNearDiagn(self):
        xc = self.line -1
        yc = self.column -1
        d = xc * math.sqrt(2)
        minD = (0,0,d)
        for c, coor in self.COLORNEIGHBOR:
            x, y = coor
            d = math.sqrt((xc - x) ** 2 + (yc - y) ** 2)
            if d < minD[2]:
                minD = (c, coor, d)
        return minD[0]

#---------------------------------------------
    def colorNearTop(self):
        xc = 0
        yc = self.column-1
        minD = (0,0,yc)
        for c, coor in self.COLORNEIGHBOR:
            x, y = coor
            d = math.sqrt((xc - x) ** 2 + (yc - y) ** 2)
            if d < minD[2]:
                minD = (c, coor, d)
        return minD[0]

    # cores de canto superior esquerdo (a) até canto superior direito (b)
    def quantityColorsAB(self):
        return len([list(t) for t in set(tuple(row) for row in self.board[0])])

    #diagnonal
    def quantityColorsAC(self):
        diag = [self.board[i][i] for i in range(len(self.board)) if self.board[i][i] != self.FC]
        diag.append(self.FC)
        return len([list(t) for t in set(tuple(row) for row in diag)])
    
    def quantityColorsHalf(self):
        board_transp = list(zip(*self.board))
        half = board_transp[self.column//2]
        lenHalf = len([list(t) for t in set(tuple(row) for row in half)])  # coluna do meio
        return lenHalf
    
    # cores de canto superior esquerdo (a) até canto inferior esquerdo (d)
    def quantityColorsAD(self):
        #board_transp = list(zip(*self.board))
        #return len([list(t) for t in set(tuple(row) for row in board_transp[0])]) 
        colYAD = [line[0] for line in self.board]
        return len([list(t) for t in set(tuple(row) for row in colYAD)])

    def quantityColorsY(self):
        board_transp = list(zip(*self.board))
        lenY = len([list(t) for t in set(tuple(row) for row in (board_transp[self.column-1]))]) # ultima coluna a esquerda
        
        return lenY
    
    # AB AD DC
    # cores de "d" canto inferior esquerdo até "c" canto inferior direito
    def quantityColorsDC(self):
       return len([list(t) for t in set(tuple(row) for row in self.board[self.line-1])])
    
    def quantityColorsBC(self):
        #board_transp = list(zip(*self.board))
        #return len([list(t) for t in set(tuple(row) for row in board_transp[self.column-1])]) 
        colYBC = [linha[-1] for linha in self.board]
        return len([list(t) for t in set(tuple(row) for row in colYBC)])

    def quantityColorsCD(self):
        return len([list(t) for t in set(tuple(row) for row in self.board[self.line-1])]) 

    def quantityColorsDA(self):
        #board_transp = list(zip(*self.board))
        #return len([list(t) for t in set(tuple(row) for row in board_transp[0])])
        colYDA = [linha[0] for linha in self.board]
        return len([list(t) for t in set(tuple(row) for row in colYDA)])
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
                #elif len(child.FLOODED)+len(child.GROUPS) == len(self.GROUPS) + len(self.FLOODED):
                #    children.append((child, c)) 
        return children
        
    # vizinho com a cor mais frequente
    def childrenNei(self):
        children = []
        self.colorNeighbor(1)
        c = self.colorNeighborFreqMax()
        if (c != self.FC) : 
            return c
        return self.childrenCenter()

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
        self.colorNeighbor(1)
        c = self.colorNearcenter()
        if (c == self.FC): 
            c = self.childrenC()                
        return c
    
    # filho mais próximo do topo considerando os vizinhos
    def childrenTopNei(self):
        children = []
        self.colorNeighbor(1)
        c = self.colorNearTop()
        if (c != self.FC): 
            child = Board(orig=self) # gera um tabuleiro com o cenário atual
            child.move(c) # troca a cor atual pela nova cor
            children.append((child, c)) 
        return children
    
    # filho mais próximo do topo sem considerar os vizinhos
    def childrenTop(self):
        c = self.colorInLineX(0) 
        return c[0]
    
    def colorNear(self, xc, yc, maxD):
        minD = (0,0,maxD)
        for c, coor in self.COLORNEIGHBOR:
            x, y = coor
            d = math.sqrt((xc - x) ** 2 + (yc - y) ** 2)
            if d < minD[2]:
                minD = (c, coor, d)
        return minD[0]
    
    
    # filho mais próximo canto inferior esquerdo (d)
    def childrenD(self):
        #children = []
        #self.colorNeighbor(1)
        c = self.colorInLineX(self.line -1)  # cor mais da linha self.line -1 mais perto do D
        #self.colorNear(self.line-1, 0, self.line-1) # cor do vizinho mais perto do D
        return c[0]
    
    # filho mais próximo a
    def childrenA(self):
        #children = []
        #self.colorNeighbor(1)
        #c = self.colorNear(0, 0, self.line-1)
        c = self.colorInLineY(0)
        return c
    # filho mais próximo canto inferior direito (c)
    def childrenC(self):
        c = self.colorInLineY(self.column - 1)
        return c
    
     # filho mais próximo da diagnonal
    def childrenDiagn(self):
        c = self.colorInLineDiag() 
        return c
    
     # filho mais próximo da linha inferior
    def childrenHalf(self):
        children = []
        self.colorNeighbor(1)
        c = self.colorNearHalf()
        #if (c != self.FC): 
        #    child = Board(orig=self) # gera um tabuleiro com o cenário atual
        #    child.move(c) # troca a cor atual pela nova cor
        #    children.append((child, c)) 
        #return children
        return c
    

    # filho mais próximo do Y extremo
    def childrenY(self):
        children = []
        self.colorNeighbor(1)
        c = self.colorNearY()
        #if (c != self.FC): 
        #    child = Board(orig=self) # gera um tabuleiro com o cenário atual
        #    child.move(c) # troca a cor atual pela nova cor
        #    children.append((child, c)) 
        #return children
        return c
#---------------------------------------------

    # estado objetivo - ou seja, sem grupo de cores
    def isOver(self):
        return len(self.GROUPS) == 0
        # if len(self.GROUPS) == 1:
        #     return (self.GROUPS[0][1] == [(0,0)]) and (self.GROUPS[0][0] == self.FC)
        # elif 
        #     return True
        # else:
        #     return False
    
    def isBoardOver(self):
        print(self.line, self.column)
        for i in range(0, self.line):
            for j in range(0, self.column):
                if (self.board[i][j] != self.board[0][0]):
                    return False                
        return True


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
                for n, g in enumerate(self.groupFilterFC()): #  percorre o mapeamento inicial de groups
                    #if self.FC == g[0]: # a cor inicial é a cor do grupo 
                    if (y < self.column and ((x, y+1) in g[1] or (x, y-1) in g[1]) ) or (x < self.line and ( (x+1, y) in g[1] or (x-1, y) in g[1] ) ):
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
                if len(self.GROUPS) > 0:
                    del self.GROUPS[g[0]]
    
    def flood2(self):
                        
        for coor in self.FLOODED:
            x, y = coor
            for n, g in enumerate(self.GROUPS): #  percorre o mapeamento inicial de groups
                if self.FC == g[0]: # a cor inicial é a cor do grupo 
                    if (y < self.column and (x, y+1) in g[1]) or (x <= self.line and (x+1, y) in g[1]):
                        tempg = g[1]#self.GROUPS[0]
                        #tempg[1] = tempg[1] + g[1]
                    
                        self.FLOODED += tempg
                        del self.GROUPS[n]
                        #print(g)
                        #print(self.GROUPS)


#---------------------------------------------
    def floodFC(self):
        
        while True:
            done = True
            for n, g in enumerate(self.groupFilterFC()): # self.FLOODED
                for coor in self.COLORNEIGHBOR: # self.groupFilterFC() percorre o mapeamento inicial de groups
                    x, y = coor[1]
                    if (y < self.column or x < self.line ) and ((x, y) in g[1]):
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
                if len(self.GROUPS0) > 0:
                    del self.GROUPS0[g[0]]


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


    def colorInLineX(self, l):
        colorsUnique = []
        for i in range(1, len(self.board[l])):
            if self.board[l][i] != self.board[l][i-1]:
                colorsUnique.append(self.board[l][i])  # adiciona a cor, se a cor anterior já existe não adiciona
                break
        return colorsUnique
    
    def nextColorInLineX(self, l):
        self.LAST_MOVE_I = 1 if self.LAST_MOVE_I == 0 else self.LAST_MOVE_I
        for i in range(self.LAST_MOVE_I, self.line):
            if self.board[l][i] != self.board[l][i-1]:
                self.LAST_MOVE_X = l
                self.LAST_MOVE_I = i                
                return self.board[l][i]
        return False
    
    def nextColorInLineX_K(self, l, k):
        self.LAST_MOVE_I = 1 if self.LAST_MOVE_I == 0 else self.LAST_MOVE_I
        for i in range(self.LAST_MOVE_I, k):
            if self.board[l][i] != self.board[l][i-1]:
                self.LAST_MOVE_X = l
                self.LAST_MOVE_I = i                
                return self.board[l][i]
        return False
    
    def colorInLineY(self, l):
        #colorsUnique = []
        #board_transp = [linha[l] for linha in self.board if linha[l] != self.FC]  #list(zip(*self.board))
        #for i in range(1, len(board_transp)):
        #    if board_transp[i] != board_transp[i-1]:
        #        colorsUnique.append(board_transp[i])  # adiciona a cor, se a cor anterior já existe não adiciona
        #        break    
        #return colorsUnique
        return next(linha[l] for linha in self.board if linha[l] != self.FC)
    
    def nextColorInLineY(self, l):
        self.LAST_MOVE_I = 1 if self.LAST_MOVE_I == 0 else self.LAST_MOVE_I

        for i in range(self.LAST_MOVE_I, self.line):
            if self.board[i][l] != self.board[i-1][l]:
                self.LAST_MOVE_Y = l
                self.LAST_MOVE_I = i
                return self.board[i][l]
        return False        
    
    def nextColorInLineY_K(self, l, K):
        self.LAST_MOVE_I = 1 if self.LAST_MOVE_I == 0 else self.LAST_MOVE_I

        for i in range(self.LAST_MOVE_I, K):
            if self.board[i][l] != self.board[i-1][l]:
                self.LAST_MOVE_Y = l
                self.LAST_MOVE_I = i
                return self.board[i][l]
        return False  
    
    def colorInLineDiag(self):
        #diag = [self.board[i][i] for i in range(len(self.board)) if self.board[i][i] != self.FC]
        #colorsUnique = []
        #for i in range(1, len(diag)):
        #    if diag[i] != diag[i-1]:
        #        colorsUnique.append(diag[i])
        #        break  
        #return colorsUnique
        return next(self.board[i][i] for i in range(len(self.board)) if self.board[i][i] != self.FC)
    
    def colorHalf(self):
        board_transp = list(zip(*self.board))
        half = board_transp[self.column//2]
        colorsUnique = []
        colorsUnique.append(half[self.column//2][0]) # adiciona a primeira cor
        for i in range(1, len(half[self.column//2])):
            if half[self.column//2][i] != half[self.column//2][i-1]:
                colorsUnique.append(half[self.column//2][i])  # adiciona a cor, se a cor anterior já existe não adiciona
                break
        return colorsUnique
    
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
