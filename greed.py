class Greed():
    def findMove(self, board): 

        if len(board.FLOODED) < (board.line * board.column )//6 : # cores do vizinho mais próximo do meio 
            board.H.append("h4")
            return board.childrenCenter()
        else: # busca gulosa
            board.H.append("h5")
            children = list(sorted(board.children(), key=lambda x: x[0].score()))
        h=2
        if h == 1:
            #AB
            if board.quantityColorsAB() > 1:  # cores de canto superior esquerdo (a) até canto superior direito (b)
                board.H.append("hAB")
                #children = board.childrenTopNei()
                return board.childrenTop()
            #BC
            elif board.quantityColorsBC() > 1: # and (board.H.count('hBC') <= board.H.count('hAB')):
                board.H.append("hBC")
                return board.childrenC()
            #DA
            elif board.quantityColorsDA() > 1:
                board.H.append("hDA")
                return board.childrenA()
            #CD
            elif board.quantityColorsCD() > 1:
                board.H.append("hCD")
                return board.childrenD()  
            #AC diagonal
            elif board.quantityColorsAC() > board.COLOR_K//2:
                board.H.append("hAC")
                return board.childrenDiagn()
            else:                
                board.H.append("h3")
                children = list(sorted(board.children(), key=lambda x: x[0].score()))


        return children[0][1] # retorna o FC topo da lista ou seja a nova cor 

    def greed(self, board):
        children = list(sorted(board.children(), key=lambda x: x[0].score()))
        return children[0][1] # retorna o FC topo da lista ou seja a nova cor 
    
    def goToCenter(self, board):
        return board.childrenCenter()
    
    def borders(self, board):
        color = False
        if board.LAST_MOVE_H == None or board.LAST_MOVE_H == 'X':            
            color = board.nextColorInLineX(0)
            board.LAST_MOVE_H = 'X' 


        if board.LAST_MOVE_H != 'C' and (board.LAST_MOVE_H == 'YY' or color == False):
            if color == False:
                board.LAST_MOVE_I = 1
            #print('XX', end=' ')
            color = board.nextColorInLineY(board.line-1)
            board.LAST_MOVE_H = 'YY'


        if board.LAST_MOVE_H != 'XX' and board.LAST_MOVE_H != 'C' and (board.LAST_MOVE_H == 'Y' or color == False):
            if color == False:
                board.LAST_MOVE_I = 1            
            #print('Y', end=' ')
            color = board.nextColorInLineY(0)
            board.LAST_MOVE_H = 'Y'

        
        if board.LAST_MOVE_H != 'C' and (board.LAST_MOVE_H == 'XX' or color == False):
            if color == False:
                board.LAST_MOVE_I = 1            
            #print('XX', end=' ')
            color = board.nextColorInLineX(board.size-1)
            board.LAST_MOVE_H = 'XX'

        
        
            
        
        if color == False or board.LAST_MOVE_H == 'C':
            #print('C', end=' ')
            color = board.childrenNei()
            board.LAST_MOVE_H = 'C'        
            
        
        return color

    def borders2(self, board):
        color = False

        if board.X_DONE == 0: # and (board.LAST_MOVE_H == None or board.LAST_MOVE_H == 'X'):
            color = board.nextColorInLineX_K(board.START_X, board.STOP_X)
            board.LAST_MOVE_H = 'X' 
            if color != False:
                return color
            else:
                board.X_DONE = 1
                board.START_Y = board.LAST_MOVE_I if board.START_X > 0 else 0
                board.Y_DONE = 0
                board.LAST_MOVE_I = 1
            
        if board.Y_DONE == 0: #and (board.LAST_MOVE_H != 'XX' and board.LAST_MOVE_H != 'C' and (board.LAST_MOVE_H == 'Y' or color == False)):
            #board.LAST_MOVE_I = 1            
            color = board.nextColorInLineY_K(board.START_Y, board.STOP_Y)
            board.LAST_MOVE_H = 'Y'
            if color != False:
                return color
            else:
                board.Y_DONE = 1
                board.START_X = board.LAST_MOVE_I
                board.STOP_X = board.STOP_X//3
                board.X_DONE = 1 if board.STOP_X == 0 else 0
                board.LAST_MOVE_I = 1       

        if board.DY_DONE==0 and color == False:            
            color = board.childrenY()
            board.DY_DONE=1
            if color != False:
                return color                
        
        if color == False or board.LAST_MOVE_H == 'C':            
            color = board.childrenNei()
            board.LAST_MOVE_H = 'C' 
            board.DY_DONE = 0  
            board.MAXCHILDREN_DONE=0     
            if color != False:
                return color
            
        
        return color     