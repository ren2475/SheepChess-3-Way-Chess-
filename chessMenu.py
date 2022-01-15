'''
Sheep chess menu
Description :
    This module responsible for display the main menu to the user 
'''
import pygame
from pygame.locals import *
from ChessMain import playChess
import gameButton
import re
import sys

'''
Set key repeat
'''
pygame.key.set_repeat(500, 80)


pygame.font.init()
pygame.init()
playing = True


'''
Screen size variables
'''
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720

screen = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))

'''
Font in game
'''
Topicfont = pygame.font.Font('font/Sanchez-Regular.ttf',40)
Messagefont = pygame.font.Font('font/Sanchez-Regular.ttf',20)
inputfont = pygame.font.Font('font/Sanchez-Regular.ttf',25)

'''
Color variables
'''
BLUE = (65,105,225)
WHITE = (255,255,255)
BLACK = (0,0,0)
DARKBROWN = (75, 55, 28)
LIGHTBROWN = (204, 153, 102)
BROWN = (152, 118, 84)
LIGHTGRAY = (196, 196, 196)

'''
Images in the game
'''
bg_img = pygame.image.load('images/background_chess.png')
bg = pygame.transform.scale(bg_img,(1280,720))


logo_img = pygame.image.load('images/chessGameLogo.png')
logo = pygame.transform.scale(logo_img,(500,500))

menuBg_img = pygame.image.load('images/menuBg.png')
menuBg = pygame.transform.scale(menuBg_img,(600,700))

htplogo_img = pygame.image.load('images/h2plogo.png')
htplogo = pygame.transform.scale(htplogo_img,(800,500))

htpInfo_img = pygame.image.load('images/h2pInfo.png')
htpInfo = pygame.transform.scale(htpInfo_img,(1100,500))

creditLogo_img = pygame.image.load('images/creditLogo.png')
creditLogo = pygame.transform.scale(creditLogo_img,(800,500))

creditInfo_img = pygame.image.load('images/creditInfo.png')
creditInfo = pygame.transform.scale(creditInfo_img,(1100,500))

usernameLogo_img = pygame.image.load('images/usernameLogo.png')
usernameLogo = pygame.transform.scale(usernameLogo_img,(500,500))

ipLogo_img = pygame.image.load('images/ipLogo.png')
ipLogo = pygame.transform.scale(ipLogo_img,(500,500))

textFrame_img = pygame.image.load('images/textFrame.png')
textFrame = pygame.transform.scale(textFrame_img,(500,500))

joinLogo_img = pygame.image.load('images/joinLogo.png')
joinLogo = pygame.transform.scale(joinLogo_img,(800,500))

lobbyInfo_img = pygame.image.load('images/lobbyInfo.png')
lobbyInfo = pygame.transform.scale(lobbyInfo_img,(500,500))

lobbyBg = pygame.image.load('images/lobbyBg.png')

invalidIp = pygame.image.load('images/invalidIP.png')

clock = pygame.time.Clock()



'''
ChessMenu
Description :
    This method will display the main menu page which is the first page when the user accesses the game. 
    This page is responsible for navigating users through the game

Does not Return value
''' 
def chessMenu():
    
    #Variebles for button
    buttonS = gameButton.Button("START", 320, 60, (DISPLAY_WIDTH/2-160,DISPLAY_HEIGHT/2-50), 8, DARKBROWN, BROWN, 15, WHITE, LIGHTBROWN)
    buttonI = gameButton.Button("INSTRUCTION", 320, 60, (DISPLAY_WIDTH/2-160,DISPLAY_HEIGHT/2+40), 8, DARKBROWN, BROWN, 15, WHITE, LIGHTBROWN)
    buttonC = gameButton.Button("CREDITS", 320, 60, (DISPLAY_WIDTH/2-160,DISPLAY_HEIGHT/2+130), 8, DARKBROWN, BROWN, 15, WHITE, LIGHTBROWN)
    buttonQ = gameButton.Button("QUIT", 320, 60, (DISPLAY_WIDTH/2-160,DISPLAY_HEIGHT/2+220), 8, DARKBROWN, BROWN, 15, WHITE, LIGHTBROWN)

    playing = True #Check playing state

    while playing:
        
        screen.blit(bg, (0, 0))
        screen.blit(menuBg, (DISPLAY_WIDTH/2-300,DISPLAY_HEIGHT/2-350))
        screen.blit(logo, (DISPLAY_WIDTH/2-250,DISPLAY_HEIGHT/2-450))

        buttonS.draw() #Start button
        buttonI.draw() #Instruction button
        buttonC.draw() #Credits button
        buttonQ.draw() #Quit button

        if buttonS.check_click():
            lobby()

        if buttonI.check_click():
            howtoplay()

        if buttonC.check_click():
            credits()
        
        if buttonQ.check_click():
            playing = False
        
        for event in pygame.event.get():
            if playing == False:
                pygame.quit()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        clock.tick(120)
        pygame.display.update()
        

'''
Lobby
Description :
    This method will display the lobby page. The user must input both username and IP address on this page before proceeding to the game.

Does not Return Value
'''
def lobby():
    running = True
    screen = pygame.display.set_mode((1280, 720))
    buttonJ = gameButton.Button("JOIN", 150, 70, (DISPLAY_WIDTH/2 + 25,DISPLAY_HEIGHT/2 +120), 8, DARKBROWN, BROWN, 15, WHITE, LIGHTBROWN)
    name = ""
    ip = ""
    
    # user name box variables
    inputname_rect = pygame.Rect(460, 235, 220, 55)
    inputip_rect = pygame.Rect(455, 360, 370, 55)
    color_active = WHITE
    color_passive = LIGHTGRAY
    activeName = False  
    activeIp = False  
    
    while running:

        screen.blit(lobbyBg, (0, 0))
        screen.blit(lobbyInfo, (DISPLAY_WIDTH - 470,DISPLAY_HEIGHT/2-250))

        #If the user clicks in the text box the color will change to make the user understand, now they can type. 
        if activeName:
            colorUser = color_active
        else:
            colorUser = color_passive

        if activeIp:
            colorIp = color_active
        else:
            colorIp = color_passive


        screen.blit(joinLogo, (DISPLAY_WIDTH/2-500,DISPLAY_HEIGHT/2-375))
        screen.blit(textFrame, (DISPLAY_WIDTH/2-400,DISPLAY_HEIGHT/2 - 269))
        screen.blit(textFrame, (DISPLAY_WIDTH/2-260,DISPLAY_HEIGHT/2 - 144))


        #Display input from the user include username and IP address
        pygame.draw.rect(screen, colorUser, inputname_rect, 0)
        pygame.draw.rect(screen, colorIp, inputip_rect, 0)
        text_surfaceName = inputfont.render(name, 5, BLACK)
        text_surfaceIp = inputfont.render(ip, 5, BLACK)
        screen.blit(text_surfaceName, (inputname_rect.x + 5, inputname_rect.y + 10))
        screen.blit(text_surfaceIp, (inputip_rect.x + 20, inputip_rect.y + 8))


        screen.blit(usernameLogo, (DISPLAY_WIDTH/2-600,DISPLAY_HEIGHT/2 - 250))
        screen.blit(ipLogo, (DISPLAY_WIDTH/2-600,DISPLAY_HEIGHT/2 - 125))
        
        buttonJ.draw() #Join button
        gameButton.buttonB.draw() #Back button
        
        #Check if user input username or not and validate IP address
        if len(ip) > 0:
            if not checkIP(ip):
                screen.blit(invalidIp, (670,386))
            else:
                if len(name) > 0 and buttonJ.check_click():
                    game(name, ip)  #Enter the game with name and ip that user input

        if gameButton.buttonB.check_click():
            running = False #Back to main menu

        for event in pygame.event.get():
            #Check if the user clicked the text box    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if inputname_rect.collidepoint(event.pos):
                    activeName = True
                    activeIp = False
                elif inputip_rect.collidepoint(event.pos):
                    activeName = False
                    activeIp = True
                else:
                    activeName = False
                    activeIp = False
            #The user can press backspace to delete the latest letter.
            if event.type == pygame.KEYDOWN:
                if activeName:
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif len(name) < 8:
                            name += event.unicode
                    elif event.key == K_RETURN:
                        name = ""
                elif activeIp:
                    if event.key == pygame.K_BACKSPACE:
                        ip = ip[:-1]
                    elif len(ip) < 20:
                            ip += event.unicode
                    elif event.key == K_RETURN:
                        ip = ""  
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


'''
game
Description :
    This method will call playChess in chessMain after the user input username, IP address and press join button
Parameter :
    name    - username that will display during the game
    ip      - ip address of the room

Does not Return value
'''
def game(name, ip):
    playChess(name, ip)   



'''
howtoplay
Description :
    This method will display instruction for user

Does not Return Value
'''    
def howtoplay():
    running = True
    while running:
        screen.blit(bg, (0, 0))
        gameButton.buttonB.draw() #Back button
        screen.blit(htplogo, (DISPLAY_WIDTH/2-400,DISPLAY_HEIGHT/2-375))
        screen.blit(htpInfo, (DISPLAY_WIDTH/2-525,DISPLAY_HEIGHT/2-200))
        if gameButton.buttonB.check_click(): #Back to main menu
                    running = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


'''
credits
Description :
    This method will display the game developers name

Does not Return Value
'''
def credits():
    running = True
    while running:
        screen.blit(bg, (0, 0))
        gameButton.buttonB.draw() #Back button
        screen.blit(creditLogo, (DISPLAY_WIDTH/2-400,DISPLAY_HEIGHT/2-375))
        screen.blit(creditInfo, (DISPLAY_WIDTH/2-525,DISPLAY_HEIGHT/2-200))
        if gameButton.buttonB.check_click(): #Back to main menu
                    running = False   
        for event in pygame.event.get(): 
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()



'''
checkIP
Description :
    This method will validate the IP address from the user
Parameter :
    ip - IP address that user input in the lobby page
Return value : 
    True    - Valid IP format
    False   - Invalid IP format
'''
def checkIP(ip):
    
    #Valid IP address format
    validIPformat = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    if(re.search(validIPformat, ip)): #Check by comparing valid ip address format and ip from user
        return True
    else:
        return False


if __name__ == "__main__":
    chessMenu()