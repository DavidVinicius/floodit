import random
import math
##from priorityq import PQ
import datetime

class Player():

    def __init__(self):
        pass


# random move
class PlayerRandom(Player):

    def __init__(self):
        super().__init__()

    def findMove(self, board):
        children = board.children()

        return random.choice(children)[1]



# greedy algorithm
class PlayerNaive(Player):
    def __init__(self):
        super().__init__()

    def findMove(self, board):
        print("len(self.FLOODED)"+str(board.scoree())+"-len(self.GROUPS)"+str(board.score()))
        if(board.score() < board.scoree()):
            # to-do mudar para a cor mais frequente na borda ?
            board.colorNeighbor()
            children = list(sorted(board.children(), key=lambda x: x[0].score())) # classifica a lista conforme o score len(self.FLOOD)
            return children[0][1] # retorna o FC topo da lista ou seja a nova cor 
        else:
            board.colorNeighbor()
            children = list(sorted(board.children(), key=lambda x: x[0].scoree())) # classifica a lista conforme o score len(self.GROUPS)
            return children[0][1] # retorna o FC topo da lista ou seja a nova cor 



# n-step ahead
class PlayerStep(Player):
    def __init__(self, depth):
        self.depth = depth

    def findMove(self, board):
        return self.findMoveHelper(board, self.depth)[1]

    def findMoveHelper(self, board, depth):

        if board.isOver():
            return (board.scoree(), -1)
        elif depth == 0:
            return (board.scoree(), -1)

        best = -math.inf
        move = ""
        for child in board.children():
            temp = self.findMoveHelper(child[0], depth-1)[0]
            if temp > best:
                best = temp
                move = child[1]

        return (best, move)


# BFS
class PlayerBFS(Player):
    def __init__(self, board):
        super().__init__()
        self.open = [(board, "")]
        self.board = board

    def findMove(self):

        x = 0
        while len(self.open) > 0:
            print("Cenário nó "+str(x)+" - self.open["+str(x)+"]:"+str(x))
            x+=1

            b, move = self.open[0] # self.open[0] estado inicial 
            
            if b.isOver():
                print("..................................Finish: "+str( datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
                print("Ordem de troca das cores na posição 0,0: ") # print solução
                print(len(move))
                step = ""
                for color in move:
                    step += "a "+color+" "
                print(step)
                return move

            children = b.children()
            for child, m in children:
                self.open.append((child, move+m)) # adiciona o nó com o melhor caminho (move+m) ex. A B ...

            del self.open[0] # remove o nó anterior


# Dynamic Programming that saves states and cuts branches that have seen before
class PlayerDP(Player):
    def __init__(self, board):
        super().__init__()
        self.closedSet = []
        self.open = [(board, "")]
        self.board = board

    def findMove(self):

        x = 0
        while len(self.open) > 0:
            print(x)
            x+=1

            b, move = self.open[0]

            if b.isOver():
                print(move)
                return move
                
            if b.GROUPS in self.closedSet:
                del self.open[0]
                print("Cut")
                continue

            children = b.children()
            for child, m in children:
                self.open.append((child, move+m))

            self.closedSet.append(b.GROUPS)
            del self.open[0]




if __name__ == '__main__':
    from board import Board
    import copy
    while True:
        try:
            L = int(input("Line of the Board: "))
            N = int(input("Column of the Board: (8 is recommended for testing)"))
            M = int(input("Number of colors: (4 is recomended for testing)"))
            a = input("Select search algorithm type: (RAND, GREED, DEPTH, BFS, DP)")
            if a.upper() in "RANDGREEDDEPTHBFSDP":
                if a.upper() == "DEPTH":
                    d = int(input("Search Depth: (3 is recommended)"))
                break
            else:
                print("Invalid Input")
        except:
            print("Invalid Input")
    
    print("..................................Start: "+str( datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
             
    i = 0
    b = Board(size=N, color=M, line=L)
    b.print()
    if a.upper() == "RAND":
        p = PlayerRandom()
        while not b.isOver():
            i+=1
            print(i)
            m = p.findMove(b)
            print(m)
            b.move(m)
            b.print()
    elif a.upper() == "GREED":
        p = PlayerNaive()
        while not b.isOver():
            i+=1
            print(i)
            m = p.findMove(b)
            print(m)
            b.move(m)
            b.print()
    elif a.upper() == "DEPTH":
        p = PlayerStep(d)
        while not b.isOver():
            i+=1
            print(i)
            m = p.findMove(b)
            print(m)
            b.move(m)
            b.print()
    elif a.upper() == "BFS":
        p = PlayerBFS(b)
        for c in p.findMove():
            i+=1
            print("....... passo "+str(i))
            b.move(c)
            b.print()
    elif a.upper() == "DP":
        p = PlayerDP(b)
        for c in p.findMove():
            i+=1
            print(i)
            b.move(c)
            b.print()
    else:
        print("ERROR")
