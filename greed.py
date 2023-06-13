class Greed():
    def findMove(self, board):        
        #print("len(self.FLOODED)"+str(board.scoree())+"-len(self.GROUPS)"+str(board.score()))
        # if(board.score() < board.scoree()):
        #     # to-do mudar para a cor mais frequente na borda ?
        #     board.colorNeighbor()
        #     children = list(sorted(board.children(), key=lambda x: x[0].score())) # classifica a lista conforme o score len(self.FLOOD)
        #     return children[0][1] # retorna o FC topo da lista ou seja a nova cor 
        # else:
        #board.colorNeighbor()
        board.colorNeighbor(1)

        if board.scoree() < (board.column * board.line)//2: # flood menor que a metade, então escolhe o children mais ao meio
            #print("h1")
            children = list(sorted(board.childrenCenter(), key=lambda x: x[0].score()))
        elif board.scoree() < (board.column * board.line)//5 : #len(board.colorsInBoard()) >= board.COLOR_K:
            #print("h2")
            children = list(sorted(board.childrenMax(), key=lambda x: x[0].score()))
        elif len(board.colorsInNEIGHBOR()) >= 10 :  #len(board.COLORNEIGHBOR) >= board.scoree()//2: #board.score():
            #print("h3")
            children = list(sorted(board.childrenNei(), key=lambda x: x[0].score()))
        else:
            #print("h4")
            children = list(sorted(board.children(), key=lambda x: x[0].score()))

        #if children == [] :
        #    children = list(sorted(board.children(), key=lambda x: x[0].scoree()))

        #if (len(board.COLORNEIGHBOR) > 2):
            #print("COLORNEIGHBOR")
        #    children = list(sorted(board.children(), key=lambda x: x[0].scoreNeigh()))
        #else:
        #    children = list(sorted(board.children(), key=lambda x: x[0].score()))

        #children = list(sorted(board.children(), key=lambda x: x[0].score()))

        return children[0][1] # retorna o FC topo da lista ou seja a nova cor 