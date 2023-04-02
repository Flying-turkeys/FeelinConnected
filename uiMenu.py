"""CSC111 Winter 2023 Final Project: Feelin Connected
File Information
===============================
Menu file

This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""
import random

import pygame
pygame.init()
pygame.font.init()

# GlOBAL VARIABLES
ROWS = 7
COLUMNS = 7
# CONNECT_X = 4
TILE_SIZE = 75

# COLOURS
# SALMON KHAKI PIECES WITH AQUAMARINE BOARD, LIGHT GREY BACKGROUND
BO_AQUAMARINE = (102, 205, 170)
P1_SALMON = (250, 128, 114)
P2_KHAKI = (255, 165, 0)
BA_LAVANDAR = (230, 230, 250)
THISTLE = (216, 191, 216)
LIGHTSAL = (233, 150, 122)

# SLIDER_WIDTH = TILE_SIZE + 1 / 2 * TILE_SIZE
# SLIDER_HEIGHT = TILE_SIZE + TILE_SIZE / 2
SLIDER_COLORS = [P1_SALMON, P2_KHAKI]
color_index = 0
color = SLIDER_COLORS[color_index]
SLIDER_X = TILE_SIZE
SLIDER_Y = TILE_SIZE - 25

mouse_x = 0
mouse_y = 0

pygame.init()

# initialize screeem
window = pygame.display.set_mode((COLUMNS * TILE_SIZE, (ROWS + 1) * TILE_SIZE))
pygame.display.set_caption('Menu')
background = BA_LAVANDAR
window.fill(background)
pygame.display.flip()

class Button:
    """A subclass which aids in the creation of all buttons used in this game.
    Instance Attributes:
        - rect: a pygame object which stores and manipulates the rectangular area of the image
    """
    # Private Instance Attributes:
    #   - _pressed: a boolean value which represents whether the button object has been
    #       clicked using the pygame.mouse.get_pressed method
    #   - _image: external .png file converted into an image using pygame.image.load('') method
    #   - _elevation: int value which represents the y coordinate value of the buttomn while not being pressed
    #   - _dynamic_elevation: int value which represents the y coordinate value of the buttomn while being pressed
    #   - _xpos: int representing the x coordinate of the image
    #   - _ypos: int representing the y coordinate of the image
    #   - width: int representing the width of the image
    #   - height: int representing the height of the image

    _pressed: bool
    _image: any
    _elevation: int
    _dynamic_elevation = int
    _original_y: int
    _xpos: int
    _ypos: int
    _width: int
    _height: int
    rect: pygame.Rect

    def __init__(self, x, y, image, elevation):
        """Initialize the button with x and y positions, the image being used,
        as well as the difference in elevation wanted while being clicked"""
        self.pressed = False
        self.image = image
        # top and bottom positions for button elevation
        self.elevation = elevation
        self.dynamic_elevation = elevation

        self.xpos = x
        self.ypos = y
        self.width = image.get_width()
        self.height = image.get_height()
        self.rect = pygame.Rect(self.xpos, self.ypos, self.width, self.height)

    def draw(self):
        """Draws the images as buttons onto the surface and specifies actions for when mouse hovers over
        or clicks on the buttons. when mouse hovers over one of the buttons its color changes by switching the
        image for the button with another one only while mouse is whithin the parameters of the button.
        When button is clicked, it calls the game its specified game state and starts the game. The button visibly
        shifts down when clicked"""
        self.rect.y = self.ypos - self.dynamic_elevation
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.image == player_v_player:
                window.blit(player_v_player_hovered, (self.rect.x, self.rect.y))
            elif self.image == player_v_pc:
                window.blit(player_v_pc_hovered, (self.rect.x, self.rect.y))
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                if self.pressed:
                    print("Clicked")  # replace with action of choosing type of gameplay and switch to game screen by main_menu = False
                    self.pressed = False
        else:
            if self.image == player_v_player:
                window.blit(player_v_player, (self.rect.x, self.rect.y))
            elif self.image == player_v_pc:
                window.blit(player_v_pc, (self.rect.x, self.rect.y))
            self.dynamic_elevation = self.elevation


def draw_board():
    """Draws all parts of the board"""
    global ROWS, COLUMNS, TILE_SIZE, BO_AQUAMARINE, P1_SALMON, P2_KHAKI, window
    pygame.draw.rect(window, BO_AQUAMARINE, pygame.Rect(0, TILE_SIZE, COLUMNS * TILE_SIZE, ROWS * TILE_SIZE))
    for row in range(ROWS):
        for column in range(COLUMNS):
            x = column * TILE_SIZE + 1 / 2 * TILE_SIZE
            y = (1 + row) * TILE_SIZE + TILE_SIZE / 2
            pygame.draw.circle(window, BA_LAVANDAR, (x, y), TILE_SIZE // 2 - 12)
    pygame.display.update()


fps = 60
timer = pygame.time.Clock()

# possible circle colors
colors = [(102, 205, 170), (250, 128, 114), (255, 165, 0), (205, 92, 92), (152, 251, 152), (255, 127, 80), (255, 91, 71)]

main_menu = True

# loads different font sizes
font = pygame.font.Font('Pixeltype.ttf', 35)
font1 = pygame.font.Font('Pixeltype.ttf', 30)
font2 = pygame.font.Font('Pixeltype.ttf', 25)
# load pvp button images
player_v_player = pygame.image.load('button1_f.png').convert_alpha(window)
player_v_player = pygame.transform.scale(player_v_player, (140, 140))
player_v_player_hovered = pygame.image.load('button1-hovered_f.png').convert_alpha(window)
player_v_player_hovered = pygame.transform.scale(player_v_player_hovered, (140, 140))
# load pvc button images
player_v_pc = pygame.image.load('button2_f.png').convert_alpha(window)
player_v_pc = pygame.transform.scale(player_v_pc, (140, 140))
player_v_pc_hovered = pygame.image.load('button2-hovered_f.png').convert_alpha(window)
player_v_pc_hovered = pygame.transform.scale(player_v_pc_hovered, (140, 140))
# Convert images into button objects
button1 = Button(window.get_rect().width // 2 - 160, window.get_rect().height // 2 - 20, player_v_player, 6)
button2 = Button(window.get_rect().width // 2 + 20, window.get_rect().height // 2 - 20, player_v_pc, 6)

# this method is just a template for how to add this menu into main game loop
# importent is to set main_menu to true in beginning and then switch to false once button is clicked
# and then switch to game play
def draw_menu():
    pygame.draw.rect(window, THISTLE, pygame.Rect(TILE_SIZE - 10, TILE_SIZE * 1.5 - 50, COLUMNS * TILE_SIZE - TILE_SIZE * 2 + 18, ROWS * TILE_SIZE - TILE_SIZE + 15), border_radius=15)
    button1.draw()
    button2.draw()

finished = False
while not finished:
    # draws random circles around border
    color_circle = pygame.draw.circle(window, color=random.choice(colors), center=(random.randint(0, 600), random.randint(0, 700)), radius=random.randint(1, 150))
    pygame.time.wait(100)

    timer.tick(fps)
    if main_menu is True:
        draw_menu()
    else:
        draw_board()
    # places text in exact positions
    message1 = font.render("Welcome to FeelinConnected:", True, 'black')
    window.blit(message1, (120, 150))
    message2 = font1.render("A Connect4 Special Edition", True, 'black')
    window.blit(message2, (140, 185))
    message3 = font2.render("By Flying Turkeys", True, 'black')
    window.blit(message3, (300, 500))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    pygame.display.flip()
quit()
