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
        if board.quantityColors() < board.COLOR_K // 2:
            print('Q')
            children = list(sorted(board.children(), key=lambda x: x[0].scoree())) # classifica a lista conforme o score len(self.GROUPS)        
        else:
            print('S')
            children = list(sorted(board.children(), key=lambda x: x[0].score())) # classifica a lista conforme o score len(self.GROUPS)        

        return children[0][1] # retorna o FC topo da lista ou seja a nova cor 