'''
ChessEngine.py
Description:
    This module is responsible for controlling chessboard and move
    It consists of 2 classes : gamestate and Move
'''


'''
mirror
Description :
    This Method responsible for mirroring the value Eg: 0 -> 7 1 -> 6
Parameter :
    value : value to be mirrored
Return mirrored value
'''
def mirror(value):
    return abs(value-7)


'''
isLowerBoard
Description :
    This Method responsible for checking the row of the board
Parameter :
    row : row of the board
Return Boolean
'''
def isLowerBoard(row):
    if(row < 4):
        return False
    else:
        return True


'''
isUpperBoard
Description :
    This Method responsible for checking the row of the board
Parameter :
    row : row of the board
Return Boolean
'''
def isUpperBoard(row):
    return not isLowerBoard(row)


'''
isWhiteBoard
Description :
    This Method responsible for checking board color (White) given the tile position
Parameter :
    row : row of the board
    col : column of the board
    board : board number
Return Boolean
'''
def isWhiteBoard(row,col,board):
    if(isLowerBoard(row)) and board == 1:
        return True
    else:
        return False


'''
isRedBoard
Description :
    This Method responsible for checking board color (Red) given the tile position
Parameter :
    row : row of the board
    col : column of the board
    board : board number
Return Boolean
'''
def isRedBoard(row,col,board):
    if(not isLowerBoard(row)) and board == 2:
        return True
    else:
        return False


'''
isBlackBoard
Description :
    This Method responsible for checking board color (Black) given the tile position
Parameter :
    row : row of the board
    col : column of the board
    board : board number
Return Boolean
'''
def isBlackBoard(row,col,board):
    if(not isLowerBoard(row)) and board == 1:
        return True
    else:
        return False

'''
isSameBoard
Description :
    This Method responsible for checking board of start and end tile of the move (In same board)
Parameter :
    Move : Move to be check
Return Boolean
'''
def isSameBoard(Move):
    if   (isWhiteBoard(Move.startRow,Move.startCol,Move.startBoard)) and (isWhiteBoard(Move.endRow,Move.endCol,Move.endBoard)):
        return True
    elif (isRedBoard(Move.startRow,Move.startCol,Move.startBoard)) and (isRedBoard(Move.endRow,Move.endCol,Move.endBoard)):
        return True
    elif (isBlackBoard(Move.startRow,Move.startCol,Move.startBoard)) and (isBlackBoard(Move.endRow,Move.endCol,Move.endBoard)):
        return True
    else:
        return False

'''
GameState
Description :
    This Class is responsible for controlling chessboard
Initial parameter :
    gameID - ID of the game given
'''
class GameState():
    
    '''
    Dictionary for Player Color
    0 -> white
    1 -> red
    2 -> black
    '''
    colorCode     = {0 : 'w' , 1 : 'r' , 2 : 'b'}
    colorToNumber = {'w' : 0 , 'r' : 1 , 'b' : 2}

    def __init__(self, gameID):
        self.board1 = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wK","wQ","wB","wN","wR"]]
        
        self.board2 = [
            ["rR","rN","rB","rQ","rK","rB","rN","rR"],
            ["rP","rP","rP","rP","rP","rP","rP","rP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["-x","-x","-x","-x","-x","-x","-x","-x"],
            ["-x","-x","-x","-x","-x","-x","-x","-x"],
            ["-x","-x","-x","-x","-x","-x","-x","-x"],
            ["-x","-x","-x","-x","-x","-x","-x","-x"]
        ]        
        self.ToMove = 0
        self.moveLog = []
        self.kingLocation =  [(7,3,1),(0,4,2),(0,4,1)]
        self.checkMove = []

        self.TwoStepPawnMove = []
        self.PossibleEnpassant = []
        self.EnpassantHistory = []

        self.CastlingHistory = []
        self.CastlingPossible = [True , True ,True]


        for col in range(8):
            for row in [1,6]:
                for board in [1,2]:
                    if row == 1:
                        self.TwoStepPawnMove.append( Move( (row,col,board) , (row+2,col,board) , self.board1 , self.board2  ) )
                    elif board == 1:
                        self.TwoStepPawnMove.append( Move( (row,col,board) , (row-2,col,board) , self.board1 , self.board2  ) )


        self.gameID = gameID
        self.playerList = []
        self.playerCount = 0
        self.ready = False

        self.stalemate = False
        self.checkmate = False

        self.PromoteTo = ['-x']
        self.PromotionHistory = []

    
    '''
    connected
    Description :
        This Method responsible for checking state of the game whether all players have connected
    Parameter :
        None
    Return Boolean
    '''
    def connected(self):
        if self.playerCount == 3:
            return True
        
        return False


    '''
    addPlayer
    Description :
        This Method responsible for adding player count to the parameter
    Parameter :
        None
    Does not Return Value
    '''
    def addPlayer(self):
        self.playerCount += 1


    '''
    NextTurn
    Description :
        This Method responsible for changing turn in gamestate
    Parameter :
        None
    Does not Return Value
    '''
    def NextTurn(self):
        self.ToMove = (self.ToMove + 1) % 3

    '''
    PreviousTurn
    Description :
        This Method responsible for changing turn in gamestate
    Parameter :
        None
    Does not Return Value
    '''
    def PreviousTurn(self):
        self.ToMove = self.ToMove - 1

        if(self.ToMove < 0):
            self.ToMove = 2

    
    '''
    NextPlayer
    Description :
        This Method responsible for returning count of next player
    Parameter :
        None
    Return Number
    '''
    def NextPlayer(self):
        return (self.ToMove + 1) % 3
    

    '''
    PreviousPlayer
    Description :
        This Method responsible for returning count of previous player
    Parameter :
        None
    Return Number
    '''
    def  PreviousPlayer(self):
        if(self.ToMove == 0):
            return 2
        else:
            return self.ToMove - 1
    
    '''
    isEmpty
    Description :
        This Method responsible for checking the tile whether is it empty
    Parameter :
        row : row of the board
        col : column of the board
        board : board number
    Return Boolean
    '''
    def isEmpty(self,row,col,board):
        if(board == 1):
            if(self.board1[row][col][0] == '-' ):
                return True
        elif(board == 2):
            if(self.board2[row][col][0] == '-' ):
                return True
        
        return False


    '''
    isPawnPromotion
    Description :
        This Method responsible for checking if the move is PawnPromotion
    Parameter :
        move : move to be checked
    Return Boolean
    '''
    def isPawnPromotion(self,move):
        if move.pieceMoved[1] == 'P':
            if move.endRow in [0,7]:
                return True
        
        return False

    
    '''
    findWinner
    Description :
        This Method responsible for finding the winner 
        Return
        -2 as No winner
        -1 as Stalemate
         0 as White
         1 as Red
         2 as Black
    Parameter :
        None
    Return Number
    '''
    def findWinner(self):
        if self.stalemate:
            return -1
        
        if self.checkmate:

            row = self.kingLocation[self.ToMove][0]
            col = self.kingLocation[self.ToMove][1]
            board = self.kingLocation[self.ToMove][2]

            opp1Move = self.getPossibleMoves( self.NextPlayer() )
            opp2Move = self.getPossibleMoves( self.PreviousPlayer() )
            
            for move in opp1Move:
                if(move.endRow == row and move.endCol == col and move.endBoard == board):
                    return self.NextPlayer()
                
            for move in opp2Move:
                if(move.endRow == row and move.endCol == col and move.endBoard == board):
                    return self.PreviousPlayer()

        return -2

    

    '''
    makeMove
    Description :
        This Method responsible for making a move in to the board and move to the next turn
    Parameter :
        None
    Does not Return
    '''
    def makeMove(self,move):
        
        if move.startBoard == 1:
            if self.board1[move.startRow][move.startCol] != "--" :
                self.board1[move.startRow][move.startCol] = "--"
                if move.endBoard == 1:
                    self.board1[move.endRow][move.endCol] = move.pieceMoved
                else:
                    self.board2[move.endRow][move.endCol] = move.pieceMoved

        else :
            if self.board2[move.startRow][move.startCol] != "--" :
                self.board2[move.startRow][move.startCol] = "--"
                if move.endBoard == 1:
                    self.board1[move.endRow][move.endCol] = move.pieceMoved
                else:
                    self.board2[move.endRow][move.endCol] = move.pieceMoved

        if(move.pieceMoved[1] == "K"):
            self.kingLocation[self.colorToNumber[ move.pieceMoved[0] ] ] = (move.endRow,move.endCol,move.endBoard)

        
        if move in self.PossibleEnpassant:

            if move.endRow == 2 :
                if move.endBoard == 1:
                    self.board1[move.endRow+1][move.endCol] = '--'
                else:
                    self.board2[move.endRow+1][move.endCol] = '--'
            
            if move.endRow == 5 :
                self.board1[move.endRow-1][move.endCol] = '--'

            self.EnpassantHistory.append(move)
        
        if move in self.CastlingPossible:
            if move.pieceMoved[0] == 'w':
                if move.endCol == 5 :
                    self.board1[7][7] = '--'
                    self.board1[7][4] = 'wR'
                else:
                    self.board1[7][0] = '--'
                    self.board1[7][2] = 'wR'

            elif move.pieceMoved[0] == 'b':
                if move.endCol == 6 :
                    self.board1[0][7] = '--'
                    self.board1[0][5] = 'bR'
                else:
                    self.board1[0][0] = '--'
                    self.board1[0][3] = 'bR'
            
            else:
                if move.endCol == 6 :
                    self.board2[0][7] = '--'
                    self.board2[0][5] = 'rR'
                else:
                    self.board2[0][0] = '--'
                    self.board2[0][3] = 'rR'
            
            self.CastlingHistory.append(move)

        if self.isPawnPromotion(move):
            if move.endBoard == 1:
                self.board1[move.endRow][move.endCol] = self.PromoteTo[0]
            else:
                self.board2[move.endRow][move.endCol] = self.PromoteTo[0]

            self.PromotionHistory.append(self.PromoteTo)
            self.PromoteTo = ['-x']    


        self.moveLog.append(move)               #Keep Log
        self.NextTurn()                         #Swap Player


    '''
    undoMove
    Description :
        This Method responsible for undoing a move in to the board and move to the next turn
    Parameter :
        None
    Does not Return
    '''
    def undoMove(self):
        if len(self.moveLog) != 0 :
            move = self.moveLog.pop()

            undoCode1 = "self.board" + str(move.startBoard) + "[move.startRow][move.startCol] = move.pieceMoved"
            exec(undoCode1)
            undoCode2 = "self.board" + str(move.endBoard) + "[move.endRow][move.endCol] = move.pieceCaptured"
            exec(undoCode2)

            if(move.pieceMoved[1] == "K"):
                self.kingLocation[self.colorToNumber[ move.pieceMoved[0] ] ] = (move.startRow,move.startCol,move.startBoard)

            

            if len(self.EnpassantHistory) != 0:
                if(move == self.EnpassantHistory[-1] and move.pieceMoved[1] == 'P' and move.startCol != move.endCol and move.pieceCaptured == '--'):
                    if move.endRow == 2 :
                        if move.endBoard == 1:
                            self.board1[move.endRow+1][move.endCol] = 'bP'
                        else:
                            self.board2[move.endRow+1][move.endCol] = 'rP'
                
                    if move.endRow == 5 :
                        self.board1[move.endRow-1][move.endCol] = 'wP'

                    self.EnpassantHistory.pop()
            
            if len(self.CastlingHistory) != 0:
                if move in self.CastlingHistory and move.pieceMoved[1] == 'K':
                    if move.pieceMoved[0] == 'w':
                        if move.endCol == 5 :
                            self.board1[7][7] = 'wR'
                            self.board1[7][4] = '--'
                        else:
                            self.board1[7][0] = 'wR'
                            self.board1[7][2] = '--'

                    elif move.pieceMoved[0] == 'b':
                        if move.endCol == 6 :
                            self.board1[0][7] = 'bR'
                            self.board1[0][5] = '--'
                        else:
                            self.board1[0][0] = 'bR'
                            self.board1[0][3] = '--'
                    
                    else:
                        if move.endCol == 6 :
                            self.board2[0][7] = 'rR'
                            self.board2[0][5] = '--'
                        else:
                            self.board2[0][0] = 'rR'
                            self.board2[0][3] = '--'
                
                self.CastlingHistory.pop()

            if len(self.PromotionHistory) != 0:
                if self.isPawnPromotion(move):
                    if move.endBoard == 1:
                        if move.pieceMoved == "wP":
                            self.board1[move.startRow][move.startCol] = "wP"
                        elif move.pieceMoved == "bP":
                            self.board1[move.startRow][move.startCol] = "bP"
                        elif move.pieceMoved == "rP":
                            self.board1[move.startRow][move.startCol] = "rP"
                    else:
                        if move.pieceMoved == "wP":
                            self.board2[move.startRow][move.startCol] = "wP"
                        elif move.pieceMoved == "bP":
                            self.board2[move.startRow][move.startCol] = "bP"
                        elif move.pieceMoved == "rP":
                            self.board2[move.startRow][move.startCol] = "rP"    

                    self.PromotionHistory.pop()

        self.PreviousTurn()

    
    '''
    getCastling
    Description :
        This Method responsible for adding "Castling" move to a move list
    Parameter :
        moves - move list to add move
        color - color of the player
    Does not Return
    '''
    def getCastling(self,moves,color):

        kColor = self.colorCode[color]

        
        if(self.CastlingPossible[color]):
            if self.hasMovedPieced(kColor + "K"):
                self.CastlingPossible[color] = False

            if(self.CastlingPossible[color]):
                if kColor == 'w':
                    if not self.hasMovedPosition(7,0,1) and self.board1[7][0] == 'wR' and self.isEmpty(7,1,1) and self.isEmpty(7,2,1) :
                        Moving = Move( (7,3,1) , (7,1,1) , self.board1 , self.board2 )
                        moves.append( Moving )
                        self.CastlingPossible.append( Moving )
                    
                    if not self.hasMovedPosition(7,7,1) and self.board1[7][0] == 'wR' and self.isEmpty(7,4,1) and self.isEmpty(7,5,1) and self.isEmpty(7,6,1):
                        Moving = Move( (7,3,1) , (7,5,1) , self.board1 , self.board2 )
                        moves.append( Moving )
                        self.CastlingPossible.append( Moving )
                
                if kColor == 'b':
                    if not self.hasMovedPosition(0,7,1) and self.board1[0][7] == 'bR' and self.isEmpty(0,5,1) and self.isEmpty(0,6,1) :
                        Moving = Move( (0,4,1) , (0,6,1) , self.board1 , self.board2 )
                        moves.append( Moving )
                        self.CastlingPossible.append( Moving )
                    
                    if not self.hasMovedPosition(0,0,1) and self.board1[0][0] == 'bR' and self.isEmpty(0,1,1) and self.isEmpty(0,2,1) and self.isEmpty(0,3,1):
                        Moving = Move( (0,4,1) , (0,2,1) , self.board1 , self.board2 )
                        moves.append( Moving )
                        self.CastlingPossible.append( Moving )

                if kColor == 'r':
                    if not self.hasMovedPosition(0,7,2) and self.board2[0][7] == 'rR' and self.isEmpty(0,5,2) and self.isEmpty(0,6,2) :
                        Moving = Move( (0,4,2) , (0,6,2) , self.board1 , self.board2 )
                        moves.append( Moving )
                        self.CastlingPossible.append( Moving )
                    
                    if not self.hasMovedPosition(0,0,2) and self.board2[0][0] == 'rR' and self.isEmpty(0,1,2) and self.isEmpty(0,2,2) and self.isEmpty(0,3,2):
                        Moving = Move( (0,4,2) , (0,2,2) , self.board1 , self.board2 )
                        moves.append( Moving )
                        self.CastlingPossible.append( Moving )


    '''
    hasMovedPieced
    Description :
        This Method responsible for checking if the piece has moved ( Only for King and Rook)
    Parameter :
        piece - the piece that want to be check
    Return Boolean
    '''
    def hasMovedPieced(self,piece):
        for move in self.moveLog:
            if move.pieceMoved == piece:
                return True
        return False

    '''
    hasMovedPosition
    Description :
        This Method responsible for checking if the piece has moved from that position
    Parameter :
        row - row of the position
        col - column of the position
        board - board of the position
    Return Boolean
    '''
    def hasMovedPosition(self , row , col , board):
        for move in self.moveLog:
            if move.startRow == row and move.startCol == col and move.startBoard == board:
                return True
        return False


    '''
    getEnpassasntMove
    Description :
        This Method responsible for adding "Enpassant" move to a move list
    Parameter :
        moves - move list to add move
        color - color of the player
    Does not Return
    '''
    def getEnpassasntMove(self,moves,color):
        
        self.PossibleEnpassant = []

        if len(self.moveLog) != 0 :
            LastMove = self.moveLog[-1]
            row   = LastMove.endRow
            col   = LastMove.endCol
            board = LastMove.endBoard
            pieceColor = LastMove.pieceMoved[0]

            if( LastMove in self.TwoStepPawnMove ):

                for n in [-1,1]:
                    if(0 <= col+n < 8):
                        if( isBlackBoard(row,col,board) ):
                            if( self.board1[row][col+n][0] != pieceColor and self.board1[row][col+n][1] == 'P' and self.board1[row-1][col] == '--' ):
                                print("B")
                                if( self.board1[row][col+n][0] == self.colorCode[color] and self.board1[row][col+n][1] == 'P' ):
                                    Moving = Move( (row,col+n,board) , (row-1,col,board) , self.board1 , self.board2 )
                                    moves.append(Moving)
                                    self.PossibleEnpassant.append(Moving)

                        if( isRedBoard(row,col,board) ):
                            if( self.board2[row][col+n][0] != pieceColor and self.board2[row][col+n][1] == 'P' and self.board2[row-1][col] == '--'):
                                print("R")
                                if( self.board2[row][col+n][0] == self.colorCode[color] and self.board2[row][col+n][1] == 'P' ):
                                    Moving = Move( (row,col+n,board) , (row-1,col,board) , self.board1 , self.board2 )
                                    moves.append(Moving)
                                    self.PossibleEnpassant.append(Moving)

                        if( isWhiteBoard(row,col,board) ):
                            if( self.board1[row][col+n][0] != pieceColor and self.board1[row][col+n][1] == 'P' and self.board1[row+1][col] == '--'):
                                print("W")
                                if( self.board1[row][col+n][0] == self.colorCode[color] and self.board1[row][col+n][1] == 'P' ):
                                    Moving = Move( (row,col+n,board) , (row+1,col,board) , self.board1 , self.board2 )
                                    moves.append(Moving)
                                    self.PossibleEnpassant.append(Moving) 




    '''
    getValidMove
    Description :
        This Method responsible for returning all valid move list
    Parameter :
        None
    Return Valid move list
    '''
    def getValidMove(self):

        possibleMove = []
        possibleMove = self.getPossibleMoves(self.ToMove) 
        self.getEnpassasntMove(possibleMove , self.ToMove)
        self.getCastling(possibleMove,self.ToMove)

        for i in range(len(possibleMove)-1 , -1 ,-1):   #Read List From Back To Front
            #Try Making a Move
            self.makeMove(possibleMove[i])
            self.PreviousTurn()

            if self.inCheck(self.ToMove):
                possibleMove.remove(possibleMove[i])
            
            self.NextTurn()
            self.undoMove()

            if len(possibleMove) == 0:

                if self.inCheck(self.ToMove):
                    self.checkmate = True
                else:
                    self.stalemate = True
            

        return possibleMove

            

    '''
    inCheck
    Description :
        This Method responsible for check whether that the king is being checked
    Parameter :
        color - color of the king
    Return Boolean
    '''
    def inCheck(self,color):
        return self.squareUnderAtk(self.kingLocation[color][0], self.kingLocation[color][1] , self.kingLocation[color][2])

    '''
    squareUnderAtk
    Description :
        This Method responsible for check whether that tile is being attacked
    Parameter :
        row - row of the square
        col - column of the square
        board - board of the square
    Return Boolean
    '''
    def squareUnderAtk(self,row,col,board):
        #Generate Enermy Move
        opp1Move = self.getPossibleMoves( self.NextPlayer() )
        opp2Move = self.getPossibleMoves( self.PreviousPlayer() )
            
        for move in opp1Move:
            if(move.endRow == row and move.endCol == col and move.endBoard == board):
                self.checkMove.append(move)
                return True
            
        for move in opp2Move:
            if(move.endRow == row and move.endCol == col and move.endBoard == board):
                self.checkMove.append(move)
                return True

        return False



 
    '''
    getPossibleMoves
    Description :
        This Method responsible for returning all "Possible" move list
    Parameter :
        colorToCheck - color of the player to be checked
    Return Valid move list
    '''
    def getPossibleMoves(self,colorToCheck):
        moves = []
        for r in range(len(self.board1)):
            for c in range(len(self.board1)):
                
                #For The First Board
                color = self.board1[r][c][0]
                if(color == self.colorCode[colorToCheck]):
                    piece = self.board1[r][c][1]
                    if(piece == 'P'):
                        self.getPawnMoves(r,c,1,moves,colorToCheck)
                    if(piece == 'R'):
                        self.getRookMoves(r,c,1,moves,colorToCheck)
                    if(piece == 'N'):
                        self.getKnightMoves(r,c,1,moves,colorToCheck)
                    if(piece == 'B'):
                        self.getBishopMoves(r,c,1,moves,colorToCheck)
                    if(piece == 'Q'):
                        self.getQueenMoves(r,c,1,moves,colorToCheck)
                    if(piece == 'K'):
                        self.getKingMoves(r,c,1,moves,colorToCheck)

                #For The Second Board  
                color = self.board2[r][c][0]
                if(color == self.colorCode[colorToCheck]):
                    piece = self.board2[r][c][1]
                    if(piece == 'P'):
                        self.getPawnMoves(r,c,2,moves,colorToCheck)
                    if(piece == 'R'):
                        self.getRookMoves(r,c,2,moves,colorToCheck)
                    if(piece == 'N'):
                        self.getKnightMoves(r,c,2,moves,colorToCheck)
                    if(piece == 'B'):
                        self.getBishopMoves(r,c,2,moves,colorToCheck)
                    if(piece == 'Q'):
                        self.getQueenMoves(r,c,2,moves,colorToCheck)
                    if(piece == 'K'):
                        self.getKingMoves(r,c,2,moves,colorToCheck)
        return moves




    '''
    getPawnMoves
    Description :
        This Method responsible for add pawn move to move list
    Parameter :
        row - row of the board
        column - column of the board
        board - board number
        moves - move list
        inColor - color of the player that want to check
    Does not Return
    '''
    def getPawnMoves(self,row,column,board,moves,inColor):
        
        color = self.colorCode[inColor]

        #White Pawn Always Move "Up"
        if color == 'w':

            # 1 Blocked Moved in Board1
            if(not isRedBoard(row,column,board)): #From White/Black Board
                #No Enermy Captured
                if self.board1[row-1][column] == "--":
                    Moving = Move( (row,column,1) , (row-1,column,1),self.board1,self.board2 )
                    moves.append(Moving)

                if self.board2[row-1][column] == "--":
                    Moving = Move( (row,column,1) , (row-1,column,1),self.board1,self.board2 )
                    if( not isSameBoard(Moving)):
                        moves.append(Moving.FromWhiteToRed(self.board1,self.board2))
                        
                #Captured
                if column-1 >= 0:    #To The Left
                    if self.board1[row-1][column-1][0] != 'w' and self.board1[row-1][column-1][0] != '-':
                        moves.append( Move( (row,column,board) , (row-1,column-1,1),self.board1,self.board2 ) )
                    if(row == 4):
                        if self.board2[row-1][column-1][0] != 'w' and self.board2[row-1][column-1][0] != '-':
                            moves.append( Move( (row,column,board) , (row-1,column-1,2),self.board1,self.board2 ) )

                if column+1 <= 7:    #To The Right
                    if self.board1[row-1][column+1][0] != 'w' and self.board1[row-1][column+1][0] != '-':
                        moves.append( Move( (row,column,board) , (row-1,column+1,1),self.board1,self.board2 ) )
                    if(row == 4):
                        if self.board2[row-1][column+1][0] != 'w' and self.board2[row-1][column+1][0] != '-':
                            moves.append( Move( (row,column,board) , (row-1,column+1,2),self.board1,self.board2 ) )

            # 1 Blocked Moved in Board2
            if(isRedBoard(row,column,board)):   #From Red Board
                #No Enermy Captured
                if(self.board2[row-1][column] == "--"):
                    moves.append(  Move( (row,column,2) , (row-1,column,2),self.board1,self.board2 )  )
                
                #Captured
                if column-1 >= 0:    #To The Left
                    if self.board2[row-1][column-1][0] != 'w' and self.board2[row-1][column-1][0] != '-':
                        moves.append( Move( (row,column,board) , (row-1,column-1,2),self.board1,self.board2 ) )

                if column+1 <= 7:    #To The Right
                    if self.board2[row-1][column+1][0] != 'w' and self.board2[row-1][column+1][0] != '-':
                        moves.append( Move( (row,column,board) , (row-1,column+1,2),self.board1,self.board2 ) )
            
            
            # 2 Blocked Moved
            if(row == 6 and board == 1 and self.board1[row-2][column] == '--' and self.board1[row-1][column] == '--'):
                moves.append( Move((row,column,1) , (row-2,column,1), self.board1 , self.board2 ) )

        #------------------------------------------------------------------------------------------------------------------------------

        #RedPawnMove Move "down" on Red and White       Move "up" on Black
        if color == 'r':
            #1 Block Moved

            if(isRedBoard(row,column,board)):   #In Red Board
                #No Enermy Capture
                if self.board2[row+1][column] == '--':
                    Moving = Move( (row,column,2) , (row+1,column,2),self.board1,self.board2 )
                    moves.append(Moving)
                if self.board1[row+1][column] == '--':
                    Moving = Move( (row,column,2) , (row+1,column,2),self.board1,self.board2 )
                    if(not isSameBoard(Moving)):
                        moves.append(Moving.FromRedToWhite(self.board1,self.board2))
                if self.board1[mirror(row+1)][mirror(column)] == '--':
                    Moving = Move( (row,column,2) , (row+1,column,2),self.board1,self.board2 )
                    if(not isSameBoard(Moving)):
                        moves.append(Moving.FromRedToBlack(self.board1,self.board2))

                #Captured
                if column-1 >=  0:      #To The Left
                    if self.board2[row+1][column-1][0] != 'r' and self.board2[row+1][column-1][0] != '-':                           #Red To Red
                        moves.append( Move( (row,column,board) , (row+1,column-1,2),self.board1,self.board2 ))
                    
                    if(row == 3):
                        if self.board1[row+1][column-1][0] != 'r' and self.board1[row+1][column-1][0] != '-':                           #Red To White
                            moves.append( Move( (row,column,board) , (row+1,column-1,1),self.board1,self.board2 ))
                        if self.board1[mirror(row+1)][mirror(column-1)][0] != 'r' and self.board1[mirror(row+1)][mirror(column-1)][0] != '-': #Red To Black
                            moves.append( Move( (row,column,board) , ( mirror(row+1),mirror(column-1) , 1)  , self.board1 , self.board2))

                if column+1 <=  7:      #To The Right
                    if self.board2[row+1][column+1][0] != 'r' and self.board2[row+1][column+1][0] != '-':                           #Red To Red
                        moves.append( Move( (row,column,board) , (row+1,column+1,2),self.board1,self.board2 ))
                    
                    if(row == 3):
                        if self.board1[row+1][column+1][0] != 'r' and self.board1[row+1][column+1][0] != '-':                           #Red To White
                            moves.append( Move( (row,column,board) , (row+1,column+1,1),self.board1,self.board2 ))
                        if self.board1[mirror(row+1)][mirror(column+1)][0] != 'r' and self.board1[mirror(row+1)][mirror(column+1)][0] != '-': #Red To Black
                            moves.append( Move( (row,column,board) , ( mirror(row+1),mirror(column+1) , 1)  , self.board1 , self.board2))

            if(isBlackBoard (row,column,board)): #In Black Board ( Move Up )
                #No Enermy Capture
                if self.board1[row-1][column] == '--':
                    moves.append( Move((row,column,1) , (row-1,column,1),self.board1,self.board2 ))

                #Captured
                if(column-1) >= 0:  #To The Left
                    if self.board1[row-1][column-1][0] != 'r' and self.board1[row-1][column-1][0] != '-':               
                        moves.append( Move( (row,column,board) , (row-1,column-1,1),self.board1,self.board2 ))
                if(column+1) <= 7:  #To The Right
                    if self.board1[row-1][column+1][0] != 'r' and self.board1[row-1][column+1][0] != '-':                      
                        moves.append( Move( (row,column,board) , (row-1,column+1,1),self.board1,self.board2 ))

            if(isWhiteBoard (row,column,board)): #In White Board ( Move Down )
                #No Enermy Capture
                if self.board1[row+1][column] == '--':
                    moves.append( Move((row,column,1) , (row+1,column,1),self.board1,self.board2 ))

                #Captured
                if(column-1) >= 0:  #To The Left
                    if self.board1[row+1][column-1][0] != 'r' and self.board1[row+1][column-1][0] != '-':               
                        moves.append( Move( (row,column,board) , (row+1,column-1,1),self.board1,self.board2 ))
                if(column+1) <= 7:  #To The Right
                    if self.board1[row+1][column+1][0] != 'r' and self.board1[row+1][column+1][0] != '-':                      
                        moves.append( Move( (row,column,board) , (row+1,column+1,1),self.board1,self.board2 ))
            
            # 2 Blocked Moved
            if(row == 1 and board == 2 and self.board2[row+2][column] == '--' and self.board2[row+1][column] == '--'):
                moves.append( Move((row,column,2) , (row+2,column,2), self.board1 , self.board2 ) )
    
        #------------------------------------------------------------------------------------------------------------------------------

        #BlackPawnMove Move "down" on Black and White       Move "up" on Red
        if color == 'b':
            #1 Block Moved

            if(isBlackBoard(row,column,board)):   #In Black Board
                #No Enermy Capture
                if self.board1[row+1][column] == '--':
                    Moving = Move( (row,column,1) , (row+1,column,1),self.board1,self.board2 )
                    moves.append(Moving)
                if self.board2[mirror(row+1)][mirror(column)] == "--":
                    Moving = Move( (row,column,1) , (row+1,column,1),self.board1,self.board2 )
                    if(not isSameBoard(Moving)):
                        moves.append(Moving.FromBlackToRed(self.board1,self.board2))

                #Captured
                if column-1 >=  0:      #To The Left
                    if self.board1[row+1][column-1][0] != 'b' and self.board1[row+1][column-1][0] != '-':                           #Black To Black and White
                        moves.append( Move( (row,column,board) , (row+1,column-1,1),self.board1,self.board2 ))
                    if row == 3:
                        if self.board2[mirror(row+1)][mirror(column-1)][0] != 'b' and self.board2[mirror(row+1)][mirror(column-1)][0] != '-': #Black To Red
                            moves.append( Move( (row,column,board) , ( mirror(row+1),mirror(column-1) , 2)  , self.board1 , self.board2))

                if column+1 <=  7:      #To The Right
                    if self.board1[row+1][column+1][0] != 'b' and self.board1[row+1][column+1][0] != '-':                           #Black To Black and White
                        moves.append( Move( (row,column,board) , (row+1,column+1,1),self.board1,self.board2 ))
                    if row == 3:
                        if self.board2[mirror(row+1)][mirror(column+1)][0] != 'b' and self.board2[mirror(row+1)][mirror(column+1)][0] != '-': #Black To Red
                            moves.append( Move( (row,column,board) , ( mirror(row+1),mirror(column+1) , 2)  , self.board1 , self.board2))

            if(isRedBoard (row,column,board)): #In Red Board ( Move Up )
                #No Enermy Capture
                if self.board2[row-1][column] == '--':
                    moves.append( Move((row,column,2) , (row-1,column,2),self.board1,self.board2 ))

                #Captured
                if(column-1) >= 0:  #To The Left
                    if self.board2[row-1][column-1][0] != 'b' and self.board2[row-1][column-1][0] != '-':               
                        moves.append( Move( (row,column,board) , (row-1,column-1,2),self.board1,self.board2 ))
                if(column+1) <= 7:  #To The Right
                    if self.board2[row-1][column+1][0] != 'b' and self.board2[row-1][column+1][0] != '-':                      
                        moves.append( Move( (row,column,board) , (row-1,column+1,2),self.board1,self.board2 ))

            if(isWhiteBoard (row,column,board)): #In White Board ( Move Down )
                #No Enermy Capture
                if self.board1[row+1][column] == '--':
                    moves.append( Move((row,column,1) , (row+1,column,1),self.board1,self.board2 ))

                #Captured
                if(column-1) >= 0:  #To The Left
                    if self.board1[row+1][column-1][0] != 'b' and self.board1[row+1][column-1][0] != '-':               
                        moves.append( Move( (row,column,board) , (row+1,column-1,1),self.board1,self.board2 ))
                if(column+1) <= 7:  #To The Right
                    if self.board1[row+1][column+1][0] != 'b' and self.board1[row+1][column+1][0] != '-':                      
                        moves.append( Move( (row,column,board) , (row+1,column+1,1),self.board1,self.board2 ))
            
            # 2 Blocked Moved
            if(row == 1 and board == 1 and self.board1[row+2][column] == '--' and self.board1[row+1][column] == '--'):
                moves.append( Move((row,column,1) , (row+2,column,1), self.board1 , self.board2 ) )
            

    '''
    getRookMoves
    Description :
        This Method responsible for add rook move to move list
    Parameter :
        row - row of the board
        column - column of the board
        board - board number
        moves - move list
        inColor - color of the player that want to check
    Does not Return
    '''
    def getRookMoves(self,row,column,board,moves,inColor):
        color = self.colorCode[inColor]
        direction = ((1,0),(-1,0),(0,1),(0,-1))
        for d in direction:
            endSameBoard = False
            endDiffBoard = False
            endDiffBoard2 = False
            for i in range(1,8):
                endRow = row + d[0] * i
                endCol = column + d[1] * i
                
                if( 0 <= endRow <= 7 and 0 <= endCol <= 7):
                    
                    #In Board1
                    if(board == 1):
                        Moving = Move((row,column,1),(endRow,endCol,1),self.board1,self.board2)
                        
                        if(not endSameBoard):                            
                            #Empty Space
                            if(self.board1[endRow][endCol] == '--'):
                                moves.append(Moving)
                                
                            #Captured
                            if(self.board1[endRow][endCol] != '--' ):
                                if self.board1[endRow][endCol][0] != color:
                                    moves.append(Moving)
                                endSameBoard = True
                                if(isSameBoard(Moving)):
                                    endDiffBoard = True
                                    endDiffBoard2 = True

                        if( not isSameBoard(Moving) and not endDiffBoard):
                            #White TO Red
                            if(isWhiteBoard(row,column,board)):
                                if(self.board2[endRow][endCol] == '--'):
                                    moves.append(Moving.FromWhiteToRed(self.board1,self.board2))
                                if(self.board2[endRow][endCol] != '--'):
                                    if(self.board2[endRow][endCol][0] != color):
                                        moves.append(Moving.FromWhiteToRed(self.board1,self.board2))
                                    endDiffBoard = True
                                    endDiffBoard2 = True

                            #Black TO Red
                            if(isBlackBoard(row,column,board)):
                                if(self.board2[mirror(endRow)][mirror(endCol)] == '--'):
                                    moves.append(Moving.FromBlackToRed(self.board1,self.board2))
                                if(self.board2[mirror(endRow)][mirror(endCol)] != '--'):
                                    if(self.board2[mirror(endRow)][mirror(endCol)][0] != color):
                                        moves.append(Moving.FromBlackToRed(self.board1,self.board2))
                                    endDiffBoard = True

                    #In Board2
                    if(board == 2):
                        Moving = Move((row,column,2),(endRow,endCol,2),self.board1,self.board2)

                        if(not endSameBoard):                            
                            #Empty Space
                            if(self.board2[endRow][endCol] == '--'):
                                moves.append(Moving)
                                
                            #Captured
                            if(self.board2[endRow][endCol] != '--' ):
                                if self.board2[endRow][endCol][0] != color and self.board2[endRow][endCol][1] != 'x':
                                    moves.append(Moving)
                                endSameBoard = True
                                if(isSameBoard(Moving)):
                                    endDiffBoard = True
                                    endDiffBoard2 = True
                        
                        if( not isSameBoard(Moving)):
                            #To White Board
                            if(not endDiffBoard):
                                if(self.board1[endRow][endCol] == '--'):
                                    moves.append(Moving.FromRedToWhite(self.board1,self.board2))
                                if(self.board1[endRow][endCol] != '--'):
                                    if(self.board1[endRow][endCol][0] != color):
                                        moves.append(Moving.FromRedToWhite(self.board1,self.board2))
                                    endDiffBoard = True

                            if(not endDiffBoard2):
                                if(self.board1[mirror(endRow)][mirror(endCol)] == '--'):
                                    moves.append(Moving.FromRedToBlack(self.board1,self.board2))
                                if(self.board1[mirror(endRow)][mirror(endCol)] != '--'):
                                    if(self.board1[mirror(endRow)][mirror(endCol)][0] != color):
                                        moves.append(Moving.FromRedToBlack(self.board1,self.board2))
                                    endDiffBoard2 = True

                    if(endSameBoard and endDiffBoard and endDiffBoard2):
                        break
                            


    '''
    getKnightMoves
    Description :
        This Method responsible for add knight move to move list
    Parameter :
        row - row of the board
        column - column of the board
        board - board number
        moves - move list
        inColor - color of the player that want to check
    Does not Return
    '''
    def getKnightMoves(self,row,column,board,moves,inColor):
        color = self.colorCode[inColor]
        direction = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        for d in direction:
            endRow = row + d[0]
            endColumn = column + d[1]
            if( 0 <= endRow <= 7 and 0 <= endColumn <= 7):
                #In Board1
                if(board == 1):
                    Moving = Move((row,column,1) , (endRow,endColumn,1) , self.board1 , self.board2)

                    #Move To Same Board
                    if( self.board1[endRow][endColumn][0] != color):                  
                        moves.append(Moving)

                    #Move To Different Board
                    if(not isSameBoard(Moving)):
                        if(isWhiteBoard(row,column,board)):
                            if(self.board2[endRow][endColumn][0] != color and self.board2[endRow][endColumn][1] != 'x'):
                                moves.append(Moving.FromWhiteToRed(self.board1,self.board2))
                        elif(isBlackBoard(row,column,board)):
                            if(self.board2[mirror(endRow)][mirror(endColumn)][0] != color and self.board2[mirror(endRow)][mirror(endColumn)][1] != 'x'):
                                moves.append(Moving.FromBlackToRed(self.board1,self.board2))
                    
                #In Board2
                if(board == 2):
                    Moving = Move((row,column,2) , (endRow,endColumn,2) , self.board1 , self.board2)

                    #Move in Same Board
                    if( self.board2[endRow][endColumn][0] != color):                    
                        if(self.board2[endRow][endColumn][1] != 'x' ):
                            moves.append(Moving)

                    #Move To Different Board
                    if(not isSameBoard(Moving)):
                        if(self.board1[endRow][endColumn][0] != color):
                            moves.append(Moving.FromRedToWhite(self.board1,self.board2))
                        if(self.board1[mirror(endRow)][mirror(endColumn)][0] != color):
                            moves.append(Moving.FromRedToBlack(self.board1,self.board2))



    '''
    getBishopMoves
    Description :
        This Method responsible for add bishop move to move list
    Parameter :
        row - row of the board
        column - column of the board
        board - board number
        moves - move list
        inColor - color of the player that want to check
    Does not Return
    '''
    def getBishopMoves(self,row,column,board,moves,inColor):
        color = self.colorCode[inColor]
        direction = ((1,1),(-1,-1),(-1,1),(1,-1))
        for d in direction:
            endSameBoard = False
            endDiffBoard = False
            endDiffBoard2 = False
            for i in range(1,8):
                endRow = row + d[0] * i
                endCol = column + d[1] * i
                
                if( 0 <= endRow <= 7 and 0 <= endCol <= 7):
                    
                    #In Board1
                    if(board == 1):
                        Moving = Move((row,column,1),(endRow,endCol,1),self.board1,self.board2)
                        
                        if(not endSameBoard):                            
                            #Empty Space
                            if(self.board1[endRow][endCol] == '--'):
                                moves.append(Moving)
                                
                            #Captured
                            if(self.board1[endRow][endCol] != '--' ):
                                if self.board1[endRow][endCol][0] != color:
                                    moves.append(Moving)
                                endSameBoard = True
                                if(isSameBoard(Moving)):
                                    endDiffBoard = True
                                    endDiffBoard2 = True

                        if( not isSameBoard(Moving) and not endDiffBoard):
                            #White TO Red
                            if(isWhiteBoard(row,column,board)):
                                if(self.board2[endRow][endCol] == '--'):
                                    moves.append(Moving.FromWhiteToRed(self.board1,self.board2))
                                if(self.board2[endRow][endCol] != '--'):
                                    if(self.board2[endRow][endCol][0] != color):
                                        moves.append(Moving.FromWhiteToRed(self.board1,self.board2))
                                    endDiffBoard = True
                                    endDiffBoard2 = True

                            #Black TO Red
                            if(isBlackBoard(row,column,board)):
                                if(self.board2[mirror(endRow)][mirror(endCol)] == '--'):
                                    moves.append(Moving.FromBlackToRed(self.board1,self.board2))
                                if(self.board2[mirror(endRow)][mirror(endCol)] != '--'):
                                    if(self.board2[mirror(endRow)][mirror(endCol)][0] != color):
                                        moves.append(Moving.FromBlackToRed(self.board1,self.board2))
                                    endDiffBoard = True

                    #In Board2
                    if(board == 2):
                        Moving = Move((row,column,2),(endRow,endCol,2),self.board1,self.board2)

                        if(not endSameBoard):                            
                            #Empty Space
                            if(self.board2[endRow][endCol] == '--'):
                                moves.append(Moving)
                                
                            #Captured
                            if(self.board2[endRow][endCol] != '--' ):
                                if self.board2[endRow][endCol][0] != color and self.board2[endRow][endCol][1] != 'x':
                                    moves.append(Moving)
                                endSameBoard = True
                                if(isSameBoard(Moving)):
                                    endDiffBoard = True
                                    endDiffBoard2 = True
                        
                        if( not isSameBoard(Moving)):
                            #To White Board
                            if(not endDiffBoard):
                                if(self.board1[endRow][endCol] == '--'):
                                    moves.append(Moving.FromRedToWhite(self.board1,self.board2))
                                if(self.board1[endRow][endCol] != '--'):
                                    if(self.board1[endRow][endCol][0] != color):
                                        moves.append(Moving.FromRedToWhite(self.board1,self.board2))
                                        endDiffBoard = True

                            if(not endDiffBoard2):
                                if(self.board1[mirror(endRow)][mirror(endCol)] == '--'):
                                    moves.append(Moving.FromRedToBlack(self.board1,self.board2))
                                if(self.board1[mirror(endRow)][mirror(endCol)] != '--'):
                                    if(self.board1[mirror(endRow)][mirror(endCol)][0] != color):
                                        moves.append(Moving.FromRedToBlack(self.board1,self.board2))
                                        endDiffBoard2 = True

                    if(endSameBoard and endDiffBoard and endDiffBoard2):
                        break
    
    
    '''
    getQueenMoves
    Description :
        This Method responsible for add queen move to move list
    Parameter :
        row - row of the board
        column - column of the board
        board - board number
        moves - move list
        inColor - color of the player that want to check
    Does not Return
    '''
    def getQueenMoves(self,row,column,board,moves,inColor):
        self.getRookMoves(row,column,board,moves,inColor)
        self.getBishopMoves(row,column,board,moves,inColor)


    '''
    getKingMoves
    Description :
        This Method responsible for add king move to move list
    Parameter :
        row - row of the board
        column - column of the board
        board - board number
        moves - move list
        inColor - color of the player that want to check
    Does not Return
    '''
    def getKingMoves(self,row,column,board,moves,inColor):
        color = self.colorCode[inColor]
        direction = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        for d in direction:
            endRow = row + d[0]
            endCol = column + d[1]

            if( 0 <= endRow <= 7 and 0 <= endCol <= 7):
                if(board == 1):
                        Moving = Move((row,column,1),(endRow,endCol,1),self.board1,self.board2)
                                                
                        #Empty Space
                        if(self.board1[endRow][endCol] == '--'):
                            moves.append(Moving)
                                
                        #Captured
                        if(self.board1[endRow][endCol] != '--' ):
                            if self.board1[endRow][endCol][0] != color:
                                moves.append(Moving)

                        
                        if(not isSameBoard(Moving)):
                            #White TO Red
                            if(isWhiteBoard(row,column,board)):
                                if(self.board2[endRow][endCol] == '--'):
                                    moves.append(Moving.FromWhiteToRed(self.board1,self.board2))
                                if(self.board2[endRow][endCol] != '--'):
                                    if(self.board2[endRow][endCol][0] != color):
                                        moves.append(Moving.FromWhiteToRed(self.board1,self.board2))

                            #Black TO Red
                            if(isBlackBoard(row,column,board)):
                                if(self.board2[mirror(endRow)][mirror(endCol)] == '--'):
                                    moves.append(Moving.FromBlackToRed(self.board1,self.board2))
                                if(self.board2[mirror(endRow)][mirror(endCol)] != '--'):
                                    if(self.board2[mirror(endRow)][mirror(endCol)][0] != color):
                                        moves.append(Moving.FromBlackToRed(self.board1,self.board2))

                    #In Board2
                if(board == 2):
                    Moving = Move((row,column,2),(endRow,endCol,2),self.board1,self.board2)
                       
                    #Empty Space
                    if(self.board2[endRow][endCol] == '--'):
                        moves.append(Moving)
                                
                    #Captured
                    if(self.board2[endRow][endCol] != '--' ):
                        if self.board2[endRow][endCol][0] != color and self.board2[endRow][endCol][1] != 'x':
                            moves.append(Moving)

                    if(not isSameBoard(Moving)):   
                        #To White Board
                        if(self.board1[endRow][endCol] == '--'):
                            moves.append(Moving.FromRedToWhite(self.board1,self.board2))
                        if(self.board1[endRow][endCol] != '--'):
                            if(self.board1[endRow][endCol][0] != color):
                                moves.append(Moving.FromRedToWhite(self.board1,self.board2))


                        #To Black Board
                        if(self.board1[mirror(endRow)][mirror(endCol)] == '--'):
                            moves.append(Moving.FromRedToBlack(self.board1,self.board2))
                        if(self.board1[mirror(endRow)][mirror(endCol)] != '--'):
                            if(self.board1[mirror(endRow)][mirror(endCol)][0] != color):
                                moves.append(Moving.FromRedToBlack(self.board1,self.board2))

            


'''
Move
Description :
    This Class responsible for controlling each move
Initial parameter :
    startBlock - Start Tile (row ,column , board)
    endBlock - End Tile (row , column , board)
    board1 - Board one list
    board2 - Board two list
'''
class Move():

    '''
    Move Dictionary
    Mathemathics Notation To Chess Notation and vice versa
    '''
    rankToRows = {"1" : 7 , "2" : 6 , "3":5 , "4" : 4,
                  "5" : 3 , "6" : 2 , "7":1 , "8" : 0}
    rowsToRank = {v:k for k , v in rankToRows.items()}

    filesToCols = {"a" : 0 , "b" : 1 , "c":2 , "d" : 3,
                  "e" : 4 , "f" : 5 , "g":6 , "h" : 7}
    colsToFiles = {v:k for k , v in filesToCols.items()}

    def __init__(self,startBlock,endBlock,board1,board2):
        self.startRow = startBlock[0]
        self.startCol = startBlock[1]
        self.startBoard = startBlock[2]
        
        self.endRow = endBlock[0]
        self.endCol = endBlock[1]
        self.endBoard = endBlock[2]

        self.moveID = self.startRow * 100000 + self.startCol * 10000 + self.startBoard * 1000 + self.endRow * 100 + self.endCol * 10 + self.endBoard


        if(startBlock[2] == 1):
            self.pieceMoved = board1[self.startRow][self.startCol]
        else:
            self.pieceMoved = board2[self.startRow][self.startCol]

        if(endBlock[2] == 1):
            self.pieceCaptured = board1[self.endRow][self.endCol]
        else:
            self.pieceCaptured = board2[self.endRow][self.endCol]


    '''
    Overide equal method for class Move
    Parameter
        other - move to be compared to
    '''
    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False

    '''
    getChessNotation
    Description :
        This Method responsible for translating chess notation (Move)
    Parameter :
        None
    Return string
    '''
    #Ex : a31a42 (Move From a31 to a42)
    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol,self.startBoard) + self.getRankFile(self.endRow,self.endCol,self.endBoard)

    '''
    getRankFile
    Description :
        This Method responsible for translating chess notation (Tile)
    Parameter :
        None
    Return string
    '''
    #Ex : a31 
    def getRankFile(self,row,col,board1):
        return self.colsToFiles[col] + self.rowsToRank[row] + str(board1)

    
    '''
    FromWhiteToRed
    Description :
        This Method responsible for changing move board (From white to Red)
    Parameter :
        board1 - Board one
        board2 - Board Two
    Return Move Class
    '''
    def FromWhiteToRed(self,board1,board2):
        ToRed = Move((self.startRow,self.startCol,self.startBoard) , (self.endRow,self.endCol,2) , board1,board2)
        return ToRed

    '''
    FromRedToWhite
    Description :
        This Method responsible for changing move board (From White to Red)
    Parameter :
        board1 - Board one
        board2 - Board Two
    Return Move Class
    '''    
    def FromRedToWhite(self,board1,board2):
        ToWhite = Move((self.startRow,self.startCol,self.startBoard) , (self.endRow,self.endCol,1) , board1,board2)
        return ToWhite

    '''
    FromBlackToRed
    Description :
        This Method responsible for changing move board (From Black to Red)
    Parameter :
        board1 - Board one
        board2 - Board Two
    Return Move Class
    '''    
    def FromBlackToRed(self,board1,board2):
        ToRed = Move((self.startRow,self.startCol,self.startBoard) , (mirror(self.endRow),mirror(self.endCol),2) , board1,board2)
        return ToRed

    '''
    FromRedToBlack
    Description :
        This Method responsible for changing move board (From Red to Black)
    Parameter :
        board1 - Board one
        board2 - Board Two
    Return Move Class
    '''
    def FromRedToBlack(self,board1,board2):
        ToBlack = Move((self.startRow,self.startCol,self.startBoard) , (mirror(self.endRow),mirror(self.endCol),1) , board1,board2)
        return ToBlack