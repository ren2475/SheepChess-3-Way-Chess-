'''
movelog.py 
Description :
    this module will track which position the player move
    the Chess, then display it while the player playing.
'''

import pygame
from pygame.locals import *

pygame.font.init()

'''
load_image
Description :
    this method will load images of chess pieces used to display in movelog.
Parameter :
    name_pic - name of piece use to display in movelog.
Return value : Image
'''
def load_image(name_pic):

    pieces = ['wP','wR','wN','wB','wK','wQ','bP','bR','bN','bB','bK','bQ','rP','rR','rN','rB','rK','rQ']
    for i in range(len(pieces)):
        if name_pic == pieces[i]:
            return pygame.transform.scale(pygame.image.load("images/" + pieces[i] + ".png") , (30,30))

'''
movelog_display
Description :
    this method will display position while the player playing.
Parameter : 
    scroll      - use to scroll movelog
    screen      - screen to display
    gamestate   - data in game
Return value : Number
'''
def movelog_display(scroll, screen, gamestate):

    k = 0               # loop in print movelog
    move_split = []     # keep text position (white, red, black)
    keep_pieces = []    # keep name of piece
    
    font = pygame.font.Font('font/Sanchez-Regular.ttf',15)
    
    #change format movelog [ f14f35 to f14 f35 ] 
    for i in range(len(gamestate.moveLog)):
        split_text1 = gamestate.moveLog[i].getChessNotation()[:3] + " " + gamestate.moveLog[i].getChessNotation()[3:]
        move_split.append(split_text1)

        #name piece move
        split_text2 = gamestate.moveLog[i].pieceMoved[0] + gamestate.moveLog[i].pieceMoved[1]
        keep_pieces.append(split_text2)

    # keep movelog in form
    # >> 1.     h21 h14         (White move)
    #           a72 a52         (Red   move)
    #           h71 h62         (Black move)
    for i in range(0, len(move_split), 3):

        # white move
        move_split[i] = ">> " + str(i//3 + 1) + ". " + "         " + str(move_split[i])
        
        # red move
        if (i+1 < len(move_split)):
            move_split[i+1] = "         " + "       " + move_split[i+1]

        # black move
        if (i+2 < len(move_split)):
            move_split[i+2] = "         " + "       " +  move_split[i+2]
    
    # loop to print movelog on screen
    for y in range(len(move_split)):

        lines = move_split[y].splitlines()

        for i, l in enumerate(lines):
            # display movelog on screen
            screen.blit(font.render(l, 10, (0,0,0)), (1075, 225 + (30 * y) - scroll))

            pic_dis = load_image(keep_pieces[k])
            screen.blit(pic_dis, (1110, 215 + (30 * y) - scroll))
            k+=1

    return 225 + (30 * y)
    

