'''
ChessMain.py
Description :
    this module is for controlling main game including UI , Game flow and connecting to server
'''

import pygame as pg
import sys
from pygame.locals import *
import ChessEngine
import promo
from network import Network
from movelog import movelog_display
import gameButton


WIDTH   =   1280
HEIGHT  =   720
DIMENSION = 8
SQ_SIZE = 400 // DIMENSION
INBETWEENDISTANCE = 200
SECONDBOARDLEFTMOST = 600
MAX_FPS = 10
IMAGES = {}

'''
    Images in menu
'''
bg = pg.image.load('images/ingame_bg.png')

bFrame_img = pg.image.load('images/boardFrame.png')
bFrame = pg.transform.scale(bFrame_img,(430,230))

victoryLogo_img = pg.image.load('images/victoryLogo.png')
victoryLogo = pg.transform.scale(victoryLogo_img,(500,500))

defeatedLogo_img = pg.image.load('images/defeatLogo.png')
defeatedLogo = pg.transform.scale(defeatedLogo_img,(500,500))

drawLogo_img = pg.image.load('images/drawLogo.png')
drawLogo = pg.transform.scale(drawLogo_img,(500,500))

waitPlayer1_img = pg.image.load('images/waitingPlayer1.png')
waitPlayer1 = pg.transform.scale(waitPlayer1_img,(250,250))

waitPlayer2_img = pg.image.load('images/waitingPlayer2.png')
waitPlayer2 = pg.transform.scale(waitPlayer2_img,(250,250))


moveLog_image = pg.image.load('images/movelogLogo.png')
moveLog_frame = pg.image.load('images/movelogFrame.png')

usernameFrame = pg.image.load('images/userFrame.png')

turnnameFrame_img = pg.image.load('images/turnFrame.png')
turnFrame = pg.transform.scale(turnnameFrame_img,(250,80))


'''
loadImages
Description :
    this method loads chess piece images
'''

def loadImages():
    pieces = ['wP','wR','wN','wB','wK','wQ','bP','bR','bN','bB','bK','bQ','rP','rR','rN','rB','rK','rQ']
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load("images/" + piece + ".png") , (SQ_SIZE,SQ_SIZE))


'''
chessBoard
Description :
    this class creates a button tile in chessboard.
Initial parameter :
    row - row of the board
    col - column of the board
    board - board number
    player - player color (0,1,2)
    rectcolor - color of the tile
'''
class chessBoard:
    def __init__(self, row,col,board,player, rectcolor):

        self.col = col
        self.row = row
        self.board = board

        self.posx = col*50
        self.posy = (row%4) * 50

        self.mouse_hovering = False
        self.checkColor = pg.Color("Purple")
        self.dispcolor = rectcolor

        boardPos = 0

        if ChessEngine.isWhiteBoard(row , col ,board):
            boardPos += 1

        if ChessEngine.isRedBoard(row , col ,board):
            boardPos += 2

        boardPos -= int(player)

        boardPos = boardPos%3

        if boardPos == 0:
            if ChessEngine.isWhiteBoard(row,col,board):
                self.posx = 450 - self.posx
                self.posy = 250 - self.posy
            else:
                self.posx = self.posx + 100
                self.posy = self.posy + 100

        if boardPos == 1:
            if ChessEngine.isWhiteBoard(row,col,board):
                self.posx = self.posx + 350
                self.posy = self.posy + 350
            else:
                self.posx = 700 - self.posx
                self.posy = 500 - self.posy
        
        if boardPos == 2:
            if ChessEngine.isWhiteBoard(row,col,board):
                self.posx = 950 - self.posx
                self.posy = 250 - self.posy
            else:
                self.posx = self.posx + 600
                self.posy = self.posy + 100
        
        self.rect = pg.Rect((self.posx,self.posy,50,50))
        self.navigation = pg.Rect((self.posx,self.posy,15,15))
       

    '''
    draw
    Description :
        this method draws the chess tile on the screen.
    Parameter:
        surface - pygame surfact object
    '''    
    def draw(self, surface):
        pg.draw.rect(surface,self.dispcolor,self.rect)

    '''
    drawNavigation
    Description :
        this method draws the navigation on chess tile on the screen.
    Parameter:
        surface - pygame surfact object
    '''
    def drawNavigation(self,surface):
        pg.draw.rect(surface,pg.Color("blue"),self.navigation)

    '''
    drawCheck
    Description :
        this method draws the check notification on chess tile on the screen.
    Parameter:
        surface - pygame surfact object
    '''
    def drawCheck(self , surface):
        pg.draw.rect(surface,self.checkColor,self.rect)

    '''
    drawPiece
    Description :
        this method draws the piece on chess tile on the screen.
    Parameter:
        surface - pygame surfact object
        piece - piece to be drawn
    '''
    def drawPiece(self , surface ,piece):
        surface.blit(IMAGES[piece],self.rect )
    
    '''
    on_mousemotion
    Description :
        this method appends the clicking list on chess tile on the screen.
    Parameter:
        event - pygame event object
        blockSelected - clicking list
    '''
    def on_mousemotion(self, event,blockSelected):
        self.mouse_hovering = self.rect.collidepoint(event.pos)

        if self.mouse_hovering:
            blockSelected.append( (self.row , self.col , self.board) )



def readFromServer(gamestate:ChessEngine.GameState , log ):
    gamestate.gameID = log[0]

    if(gamestate.playerCount < 3):
        gamestate.playerCount = log[1]
        gamestate.playerList = log[2]
    else:        
        while( len(log)-3 == len(gamestate.moveLog) + 1):
            moveLogLen = len(gamestate.moveLog)

            data = log[moveLogLen + 3] 
            if(data[0:6] == "Change"):
                try:                       
                    move = ChessEngine.Move((int(data[8]), int(data[9]), int(data[10])), (int(data[11]), int(data[12]), int(data[13])), gamestate.board1, gamestate.board2)
                    gamestate.PromoteTo = [data[6:8]]
                    gamestate.makeMove(move)
                    gamestate.PromoteTo = ['-x']
                except:
                    print("PP error occured")            
            
            elif len(data) == 6:
                #Make move for the player
                try:
                            
                    move = ChessEngine.Move((int(data[0]), int(data[1]), int(data[2])), (int(data[3]), int(data[4]), int(data[5])), gamestate.board1, gamestate.board2)
                    gamestate.makeMove(move)                            

                except:
                    print("error occured")
        
        return True
    return False
    




'''
playChess
Description :
    this method appends the chessboard on chess tile on the screen.
Parameter:
    event - pygame event object
    blockSelected - clicking list
'''
def playChess(name, ip):

    '''
    Set Up Variable
    '''
    scroll = 0
    check_scroll = 0
    isPromote = False
    player = "0"
    lostConCount = 0

    '''
    Set Up Pygame Variable
    '''
    pg.init()
    screen = pg.display.set_mode((WIDTH,HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    color = [ pg.Color("light grey"),pg.Color("red") ]
    buttons = []

    '''
    Setup Valid moves List
    '''
    gamestate = ChessEngine.GameState(0)
    validMoves = gamestate.getValidMove()
    moveMade = False    #For Recalculate Valid Move after the move is made

    loadImages()

    '''
    Setup Clicking
    '''
    running = True
    blockSelected = []  # Track the Last Click (Row,Column,Board)
    lastSelected = []
    playerClicks = []   # Track player Click
    gameEnd = False

    viewCheck = False

    '''
    Try Connection
    '''
    try:
        network = Network(ip)
        data = network.send("Name" + str(name))

        #gamestate.playerList.append(name)
        player = data[1]-1
        #print("You are", player)
    except:
        state = True
        state = errorIP_display(screen)
        if not state: 
            running = False


    '''
    Setup chessboard
    '''
    board = 1
    for row in range(8):
        for col in range(8):
            buttons.append(chessBoard(row,col,board, player , color[( (row + col) % 2 )] ))

    board = 2
    for row in range(4):
        for col in range(8):
            buttons.append(chessBoard(row,col,board, player ,color[( (row + col) % 2 )] ))   



    '''
    Running The Game
    '''
    while running:

        '''
        Draw Game
        '''
        screen.blit(bg, (0,0))             # bg in game
        
        '''
        Getting Game data from server
        '''
        if not gameEnd:
            try:
                if lostConCount < 10:
                    data = network.send("getGame")
                    moveMade = readFromServer(gamestate,data)
                    lostConCount = 0

            except Exception as e:
                lostConCount += 1
                # print("get " + str(e))
                if lostConCount >= 10:
                    state = True
                    state = lostcon_display(screen)
                    if not state: 
                        running = False

        '''
        Waiting For Connection
        '''
        if not gamestate.connected():
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            # wait bg
            wait_screen = pg.image.load("images/waitingScreen.png")
            screen.blit(wait_screen, (0,0))
            gameButton.buttonB.draw()
            if gameButton.buttonB.check_click():
                running = False

            # show => wait for 2 player
            count_player = 3 - gamestate.playerCount                                # count player
            if(count_player == 2):
                screen.blit(waitPlayer1, (500,350))
            elif(count_player == 1):
                screen.blit(waitPlayer2, (500,350))


        '''
        Game is Connected
        '''
        if gamestate.connected():
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                '''
                Mouse Event
                '''                
                if e.type == pg.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        for button in buttons:
                            button.on_mousemotion(e,blockSelected)

                            

                        '''
                        Reading Player Clicking
                        '''

                        if(blockSelected == lastSelected):      #Double Click Same Square
                            blockSelected = []
                            lastSelected = []
                            playerClicks = []
                            isPromote = False
                        else:
                            if len(blockSelected) != 0:    
                                playerClicks.append(blockSelected[0])      #Append Double Click
                                lastSelected = []

                        if len(blockSelected) == 1:
                            lastSelected = blockSelected
                            blockSelected = []
                            isPromote = False

                        
                        
                        if len(playerClicks) == 1:
                            if(gamestate.isEmpty(lastSelected[0][0],lastSelected[0][1],lastSelected[0][2])):
                                blockSelected = []                      #Reset Block Clicked
                                playerClicks = []                       #Reset Clicks
                                isPromote = False
                                


                        if len(playerClicks) == 2:
                            move = ChessEngine.Move(playerClicks[0],playerClicks[1],gamestate.board1,gamestate.board2)
                            print("Turn        :" + str(gamestate.ToMove))
                            print("Try To Move :" + move.getChessNotation())
                            #Check Move Validity
                            
                            #If Valid
                            if move in validMoves and int(player) == gamestate.ToMove:
                                print("Move :" + move.getChessNotation())

                                if not gamestate.isPawnPromotion(move):
                                    #Format - RowBefore + ColumnBefore + BoardBefore + RowAfter + ColumnAfter + BoardAfter
                                    send = str(playerClicks[0][0]) + str(playerClicks[0][1]) + str(playerClicks[0][2]) + str(playerClicks[1][0]) + str(playerClicks[1][1]) + str(playerClicks[1][2])
                                    try:
                                        data = network.send(send)
                                        readFromServer(gamestate , data)
                                    except Exception as e:
                                        print("Sent " + str(e))
                                        # print("error sending move to server")

                                            #gamestate.makeMove(move)                   
                                    moveMade = True
                                    blockSelected = []                      #Reset Block Clicked
                                    lastSelected = []
                                    playerClicks = []                       #Reset Clicks

                                #PawnPromotion
                                elif gamestate.PromoteTo[0] == '-x':
                                    isPromote = True
                                    sendpromoMove =  str(playerClicks[0][0]) + str(playerClicks[0][1]) + str(playerClicks[0][2]) + str(playerClicks[1][0]) + str(playerClicks[1][1]) + str(playerClicks[1][2])
                                    

                            else :
                                del playerClicks[0]
                                if(gamestate.isEmpty(lastSelected[0][0],lastSelected[0][1],lastSelected[0][2])):
                                    blockSelected = []                  #Reset Block Clicked
                                    lastSelected = []
                                    playerClicks = []
                        
                        if len(playerClicks) == 3:
                            isPromote = False
                            del playerClicks[1]
                            del playerClicks[0]
                            
    
                    # scroll movelog
                    elif(e.button == 4):
                        if scroll > 0:
                            scroll -= 30
                    
                    elif (e.button == 5):
                        if (scroll + 700) < check_scroll:
                            scroll += 30           



            '''
            Exit game via Back
            '''
            gameButton.buttonB.draw()
            if gameButton.buttonB.check_click():
                        running = False

            '''
            Pawn Promotion
            '''
            if isPromote:
                isPromote , promoteBuffer = promo.promo_chess(screen,isPromote,int(player))
                if not isPromote:
                    gamestate.PromoteTo = [str(promoteBuffer)]
                    sendChangeTo = "Change" + promoteBuffer

                    try:
                        data = network.send(sendChangeTo + sendpromoMove)
                        readFromServer(gamestate,data)
                        
                    except:
                        print("error sending move to server")

                                            #gamestate.makeMove(move)                   
                    moveMade = True
                    blockSelected = []                      #Reset Block Clicked
                    lastSelected = []
                    playerClicks = []                       #Reset Clicks
                

            '''
            Get New Valid Move
            '''
            if(moveMade):
                validMoves = gamestate.getValidMove()
                moveMade = False                                

            '''
            Movelog
            '''
            moveLog_area = pg.Rect(1015, 0, 265, HEIGHT)
            pg.draw.rect(screen, (255,255,255), moveLog_area)
            screen.blit(moveLog_frame, (1015,180))
            screen.blit(moveLog_image, (1015,0))

            # moveLog display
            if len(gamestate.moveLog) > 0:
                check_scroll = movelog_display(scroll, screen, gamestate)
            
            # moveLog frame
            screen.blit(moveLog_frame, (1015,180))
            screen.blit(moveLog_image, (1015,0))
            

            '''
            Username area
            '''
            # top left box
            screen.blit(usernameFrame, (130,30))
            # top right box
            screen.blit(usernameFrame, (630,30))
            # middle box
            screen.blit(usernameFrame, (380,570))

            # turn area
            screen.blit(turnFrame,(70,340))

            # display username
            name_displayBoard(screen, gamestate, player)

            screen.blit(bFrame, (335,335)) ##white
            screen.blit(bFrame, (85,85)) ##black
            screen.blit(bFrame, (585,85)) ##red

            '''
            Draw Game
            '''
            drawGameState(screen,buttons,validMoves,playerClicks,player,gamestate)


            '''
            Display the game result
            ''' 
            if gamestate.findWinner() == -1: #Stalemate condition - Every player tie
                gameEnd = True
                if not viewCheck:
                    screen.blit(drawLogo, (WIDTH/2 - 250,HEIGHT/2-250))
                    gameButton.buttonMidB.draw() 
                    gameButton.buttonV.draw() #Button to view move log history
                    if gameButton.buttonV.check_click(): #Check if the player wants to view the latest state of the board and move logs.
                        viewCheck = True
                        screen.blit(bFrame, (335,335)) #white
                        screen.blit(bFrame, (85,85)) #black
                        screen.blit(bFrame, (585,85)) #red
                        drawGameState(screen,buttons,validMoves,playerClicks,player,gamestate)
                    if gameButton.buttonMidB.check_click():
                                running = False

            elif gamestate.findWinner() != -2: #Winner
                gameEnd = True
                if int(player) == gamestate.findWinner():
                    if not viewCheck:
                        screen.blit(victoryLogo, (WIDTH/2 - 250,HEIGHT/2-250))
                        gameButton.buttonMidB.draw() 
                        gameButton.buttonV.draw() #Button to view move log history
                        if gameButton.buttonV.check_click(): #Check if the player wants to view the latest state of the board and move logs.
                            viewCheck = True
                            screen.blit(bFrame, (335,335)) #white
                            screen.blit(bFrame, (85,85)) #black
                            screen.blit(bFrame, (585,85)) #red
                            drawGameState(screen,buttons,validMoves,playerClicks,player,gamestate)
                        if gameButton.buttonMidB.check_click():
                                    running = False

                else: 
                    if not viewCheck:  #Loser
                        screen.blit(defeatedLogo, (WIDTH/2 - 250,HEIGHT/2-250))
                        gameButton.buttonMidB.draw() 
                        gameButton.buttonV.draw() ##Button to view move log history
                        if gameButton.buttonV.check_click(): #Check if the player wants to view the latest state of the board and move logs.
                            viewCheck = True
                            screen.blit(bFrame, (335,335)) #white
                            screen.blit(bFrame, (85,85)) #black
                            screen.blit(bFrame, (585,85)) #red
                            drawGameState(screen,buttons,validMoves,playerClicks,player,gamestate)
                        if gameButton.buttonMidB.check_click():
                                    running = False


        clock.tick(MAX_FPS)
        pg.display.flip()


'''
drawGameState
Description :
    this method draw the game itself.
Parameter :
    screen - Pygame Screen Object
    buttons - list of chess tile
    validMoves - list of valid moves
    playerClicks - list of player clicking input
    player - player color (0,1,2)
    gamestate - gamestate object for the game
Does not Return value
'''
def drawGameState(screen,buttons,validMoves,playerClicks,player,gamestate):
    drawBoard(screen,buttons)
    drawCheck(screen,gamestate,buttons)
    drawNavigation(playerClicks,player,gamestate,validMoves,buttons,screen)    
    drawPieces(screen,gamestate.board1,gamestate.board2,buttons)

'''
drawBoard
Description :
    this method draw the game board.
Parameter :
    screen - Pygame Screen Object
    buttons - list of chess tile
Does not Return value
'''
def drawBoard(screen,buttons):
    for button in buttons:
        button.draw(screen)       
            
'''
drawNavigation
Description :
    this method draw the navigation on chess board.
Parameter :
    screen - Pygame Screen Object
    buttons - list of chess tile
    validMoves - list of valid moves
    playerClicks - list of player clicking input
    player - player color (0,1,2)
    gamestate - gamestate object for the game
Does not Return value
'''
def drawNavigation(playerClicks,player,gamestate,validMoves,buttons,screen):
    if(len(playerClicks) == 1 and int(player) == gamestate.ToMove):
        for validMove in validMoves:
            if playerClicks[0][0] == validMove.startRow and playerClicks[0][1] == validMove.startCol and playerClicks[0][2] == validMove.startBoard :
                position = validMove.endRow*8 + validMove.endCol + (validMove.endBoard-1)*64
                buttons[position].drawNavigation(screen)
    

'''
drawPieces
Description :
    this method draw the all the chess piece.
Parameter :
    screen - Pygame Screen Object
    buttons - list of chess tile
    board1 - first board
    board2 - second board
Does not Return value
'''
def drawPieces(screen,board1,board2,buttons):
    
    for row in range(8):
        for col in range (8):
            for board in [1,2]:
                if  board == 2 and row < 4:                    
                    piece = board2[row][col]
                    if piece != "--":
                        position = col + row*8 + 64
                        buttons[position].drawPiece(screen,piece)
                else:                    
                    piece = board1[row][col]
                    if piece != "--":
                        position = col + row*8
                        buttons[position].drawPiece(screen,piece)

   
'''
drawCheck
Description :
    this method draw the check notification.
Parameter :
    screen - Pygame Screen Object
    buttons - list of chess tile
    gamestate - gamestate object for the game
Does not Return value
'''
def drawCheck(screen,gamestate,buttons):
    opp1Move = gamestate.getPossibleMoves( gamestate.NextPlayer() )
    opp2Move = gamestate.getPossibleMoves( gamestate.PreviousPlayer() )
    row = gamestate.kingLocation[gamestate.ToMove][0]
    col = gamestate.kingLocation[gamestate.ToMove][1]
    board = gamestate.kingLocation[gamestate.ToMove][2]


    for move in opp1Move:
        if(move.endRow == row and move.endCol == col and move.endBoard == board):
            position = move.endRow*8 + move.endCol + (move.endBoard-1)*64
            buttons[position].drawCheck(screen)
            position = move.startRow*8 + move.startCol + (move.startBoard-1)*64
            buttons[position].drawCheck(screen)
            
            
    for move in opp2Move:
        if(move.endRow == row and move.endCol == col and move.endBoard == board):
            position = move.endRow*8 + move.endCol + (move.endBoard-1)*64
            buttons[position].drawCheck(screen)
            position = move.startRow*8 + move.startCol + (move.startBoard-1)*64
            buttons[position].drawCheck(screen)



'''
name_displayBoard
Description :
    this method will display username in game and display who turn.
Parameter :
    screen      - screen to display
    gamestate   - data in game
    player      - player in game
Does not return value
'''
def name_displayBoard(screen, gamestate, player):
    WHITE = (255,255,255)
    font1 = pg.font.Font('font/Sanchez-Regular.ttf',35)

    # white player display
    if int(player) == 0:
        # middle
        if len(gamestate.playerList) >= 1:
            text1 = font1.render(str(gamestate.playerList[0]), 5, WHITE)
            text_rect1 = text1.get_rect(center=(1100//2, 592))
            screen.blit(text1, text_rect1)
        # top right
        if len(gamestate.playerList) >= 2:
            text2 = font1.render(str(gamestate.playerList[1]), 5, WHITE)
            text_rect2 = text2.get_rect(center=(1600//2, 52))
            screen.blit(text2, text_rect2)
        # top left
        if len(gamestate.playerList) >= 3:
            text3 = font1.render(str(gamestate.playerList[2]), 5, WHITE)
            text_rect3 = text3.get_rect(center=(600//2, 52))
            screen.blit(text3, text_rect3)
    # red player display
    elif int(player) == 1:
        # middle
        if len(gamestate.playerList) >= 2:
            text1 = font1.render(str(gamestate.playerList[1]), 5, WHITE)
            text_rect1 = text1.get_rect(center=(1100//2, 592))
            screen.blit(text1, text_rect1)
        # top right
        if len(gamestate.playerList) >= 3:
            text2 = font1.render(str(gamestate.playerList[2]), 5, WHITE)
            text_rect2 = text2.get_rect(center=(1600//2, 52))
            screen.blit(text2, text_rect2)
        # top left
        if len(gamestate.playerList) >= 1:
            text3 = font1.render(str(gamestate.playerList[0]), 5, WHITE)
            text_rect3 = text3.get_rect(center=(600//2, 52))
            screen.blit(text3, text_rect3)
    # black player display
    elif int(player) == 2:
        # middle
        if len(gamestate.playerList) >= 3:
            text1 = font1.render(str(gamestate.playerList[2]), 5, WHITE)
            text_rect1 = text1.get_rect(center=(1100//2, 592))
            screen.blit(text1, text_rect1)
        # top right
        if len(gamestate.playerList) >= 1:
            text2 = font1.render(str(gamestate.playerList[0]), 5, WHITE)
            text_rect2 = text2.get_rect(center=(1600//2, 52))
            screen.blit(text2, text_rect2)
        # top left
        if len(gamestate.playerList) >= 2:
            text3 = font1.render(str(gamestate.playerList[1]), 5, WHITE)
            text_rect3 = text3.get_rect(center=(600//2, 52))
            screen.blit(text3, text_rect3)

    # display turn
    if int(player) == int(gamestate.ToMove):
        screen.blit(font1.render("Your Turn", 5, WHITE), (90, 355))
    elif int(gamestate.ToMove) == 0:
        screen.blit(font1.render("White Turn", 5, WHITE), (90, 355))
    elif int(gamestate.ToMove) == 1:
        screen.blit(font1.render("Red Turn", 5, WHITE), (90, 355))
    elif int(gamestate.ToMove) == 2:
        screen.blit(font1.render("Black Turn", 5, WHITE), (90, 355))


'''
lostcon_display
Description :
    this method will display error screen when one of the players lost connection.
Parameter :
    screen - screen to display
Return value : Boolean
'''
def lostcon_display(screen):

    running = True
    state = True

    # back button use to back to lobby
    buttonReturn = gameButton.Button("RETURN TO LOBBY", 320, 60, (490,550), 8, gameButton.DARKBROWN, gameButton.BROWN, 15, gameButton.WHITE, gameButton.LIGHTBROWN)

    # load lost connection screen
    lostcon_screen = pg.image.load("images/lostConnection.png")

    while running:

        # draw screen
        screen.blit(lostcon_screen,(0, 0))
        #back button
        buttonReturn.draw()

        #use to back to lobby
        if buttonReturn.check_click():
            state = False
            running = False

        pg.display.update()

        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()

    return state


'''
errorIP_display
Description :
    this method will display error screen when IP that user input is not use to open server.
Parameter :
    screen - screen to display
Return value : Boolean
'''
def errorIP_display(screen):

    running = True
    state = True

    # back button use to back to lobby
    buttonReturn = gameButton.Button("RETURN TO LOBBY", 320, 60, (490,550), 8, gameButton.DARKBROWN, gameButton.BROWN, 15, gameButton.WHITE, gameButton.LIGHTBROWN)

    # load notexistRoom screen
    errorIp_screen = pg.image.load("images/notexistRoom.png")

    while running:

        # draw screen
        screen.blit(errorIp_screen,(0, 0))
        #back button
        buttonReturn.draw()

        #use to back to lobby
        if buttonReturn.check_click():
            state = False
            running = False

        pg.display.update()

        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()

    return state