'''
Game button.py
Description :
    This module is used to create buttons for the game 
'''

import pygame

Topicfont = pygame.font.Font('font/Sanchez-Regular.ttf',30)
screen = pygame.display.set_mode((1280,720))
'''
    color variables
'''
WHITE = (255,255,255)
DARKBROWN = (75, 55, 28)
LIGHTBROWN = (204, 153, 102)
BROWN = (152, 118, 84)

'''
    Button - create button object
'''
class Button():
    '''
        __init__ - Constructor for creating an object which will use to setup an object.
         text - text display on the button
         width, height - size of the button
         pos - position of the button (x, y)
         elevation - elevation of the button
         color_top_rect - color of top of the button's rectangle
         color_bottom_rect - color of bottom of the button's rectangle
         borderRadius - Border radius of the button
         color_text - color of text
         color_hovered - color when the button is hovered
    '''
    def __init__(self, text, width, height, pos, elevation, color_top_rect, color_bottom_rect, borderRadius, color_text, color_hovered):
        self.color_text = color_text
        self.borderRadius = borderRadius
        self.color_top_rect = color_top_rect
        self.color_bottom_rect = color_bottom_rect
        self.color_hovered = color_hovered
        self.text = text

		#Core attributes 
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

		# top rectangle 
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = self.color_top_rect

		# bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = self.color_bottom_rect
		
		#text
        self.text_surf = Topicfont.render(self.text, True, self.color_text)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
    
    '''
        draw - draw button on the screen
    '''
    def draw(self):
		# elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center 

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen,self.bottom_color, self.bottom_rect, border_radius = self.borderRadius)
        pygame.draw.rect(screen,self.top_color, self.top_rect, border_radius = self.borderRadius)
        screen.blit(self.text_surf, self.text_rect)
        '''
			change color when hovering on the button
		'''
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.color_hovered
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0 #When user click elecation of the button become 0
            else:
                self.dynamic_elecation = self.elevation
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = self.color_top_rect

    '''
        check_click - used to check if the button was clicked
    '''
    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        action = False
        if self.top_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and self.pressed == False:
                self.pressed = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.pressed = False

        return action

'''
    General buttons for any functions
'''
buttonB = Button("BACK", 120, 60, (1280/2-550,720/2+250), 8, DARKBROWN, BROWN, 15, WHITE, LIGHTBROWN)
buttonMidB = Button("BACK", 120, 60, (1280/2-150,720/2), 8, DARKBROWN, BROWN, 15, WHITE, LIGHTBROWN)
buttonV = Button("VIEW", 120, 60, (1280/2+25,720/2), 8, DARKBROWN, BROWN, 15, WHITE, LIGHTBROWN)