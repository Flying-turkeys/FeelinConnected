"""CSC111 Winter 2023 Final Project: Feelin Connected

File Information
===============================
This file contains graphical user interface for the game board

This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""
import pygame, numpy

# GlOBAL VARIABLES
ROWS = 7
COLUMNS = 7
CONNECT_X = 4
TILE_SIZE = 80

# COLOURS
# SALMON KHAKI PIECES WITH AQUAMARINE BOARD, LIGHT GREY BACKGROUND
AQUAMARINE = (102, 205, 170)
SALMON = (250, 128, 114)
KHAKI = (240, 230, 140)
LAVANDAR = (230, 230, 250)


def draw_board():
    """Draws all parts of the board"""
    global ROWS, COLUMNS, TILE_SIZE, AQUAMARINE, SALMON, KHAKI, window
    pygame.draw.rect(window, AQUAMARINE, pygame.Rect(0, TILE_SIZE, COLUMNS * TILE_SIZE, ROWS * TILE_SIZE))
    for row in range(ROWS):
        for column in range(COLUMNS):
            x = column * TILE_SIZE + 1 / 2 * TILE_SIZE
            y = (1 + row) * TILE_SIZE + TILE_SIZE / 2
            pygame.draw.circle(window, LAVANDAR, (x, y), TILE_SIZE // 2 - 3)
    pygame.display.update()


window = pygame.display.set_mode((COLUMNS * TILE_SIZE, (ROWS + 1) * TILE_SIZE))
background = LAVANDAR
window.fill(background)
pygame.display.flip()

finished = False
while not finished:
    draw_board()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
quit()
