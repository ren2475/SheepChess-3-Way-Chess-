'''
promo.py 
Description :
    this module displays what piece that pawn want to promotion.
    Pawn promotion occurs when a pawn reaches the farthest rank from its original square.
    When this happens, the player can replace the pawn for a queen, a rook, a bishop, or a knight.
'''

import pygame
from pygame.locals import *

pygame.init()

promoFrame = pygame.image.load('images/pawnFrame.png')      #image for pawn promotion


'''
image_button
Description :
    this class creates a button from the image.
Initial parameter :
    x       - position in x axis
    y       - position in y axis
    image   - image of the button
'''
class image_button():

    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.pressed = False
    '''
    draw
    Description :
        this method draws the button on the screen.
    '''
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    '''
    check click
    Description :
        this method checks the case user click the button.
    Return value :
        true    - if the button was clicked.
        false   - if the button was not clicked.
    '''
    def is_Click(self):
        mouse_pos = pygame.mouse.get_pos()
        action = False
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and self.pressed == False:
                self.pressed = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.pressed = False
        
        return action


'''
promo_chess
Description :
    this method will display option to choose piece for player when in case pawn promotion.
Parameter :
    screen      - screen to display
    state       - use to open and close popup of promotion.
    player      - what player want to promo the pawn
Return value :  String and Boolean
'''
def promo_chess(screen, state, player):

    string_click = ""   # keep color of player

    screen.blit(promoFrame, (765,355))
    # white player
    if player == 0:
        promoQ = pygame.image.load("images/promowQ.png")
        promoR = pygame.image.load("images/promowR.png")
        promoN = pygame.image.load("images/promowN.png")
        promoB = pygame.image.load("images/promowB.png")
        string_click = 'w'

    # red player
    elif player == 1:
        promoQ = pygame.image.load("images/promorQ.png")
        promoR = pygame.image.load("images/promorR.png")
        promoN = pygame.image.load("images/promorN.png")
        promoB = pygame.image.load("images/promorB.png")
        string_click = 'r'

    # black player
    elif player == 2:
        promoQ = pygame.image.load("images/promobQ.png")
        promoR = pygame.image.load("images/promobR.png")
        promoN = pygame.image.load("images/promobN.png")
        promoB = pygame.image.load("images/promobB.png")
        string_click = 'b'

    #load images pop button
    b_promoQ = image_button(790, 380, promoQ)
    b_promoR = image_button(890, 380, promoR)
    b_promoN = image_button(790, 450, promoN)
    b_promoB = image_button(890, 450, promoB) 
    
    promo = [b_promoQ, b_promoR, b_promoN, b_promoB]
    for promo_seg in promo:
        promo_seg.draw(screen)
        # in case choose queen for promotion
        if b_promoQ.is_Click():
            string_click = string_click + "Q"
            state = False               # close popup
        # in case choose rook for promotion
        elif b_promoR.is_Click():
            string_click = string_click + "R"
            state = False               # close popup
        # in case choose knight for promotion
        elif b_promoN.is_Click():
            string_click = string_click + "N"
            state = False               # close popup
        # in case choose bishop for promotion
        elif b_promoB.is_Click():
            string_click = string_click + "B"
            state = False               # close popup        
    
    return state, string_click
    



