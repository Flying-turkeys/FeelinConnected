"""CSC111 Winter 2023 Final Project: Feelin Connected
File Information
===============================
This file contains any and all code required to run a pygame version of our
Connect 4 implementation.


This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""

from board import Piece, Board, Connection
import pygame
from typing import Optional
from players import GreedyPlayer

# COLOURS
# SALMON KHAKI PIECES WITH AQUAMARINE BOARD, LIGHT GREY BACKGROUND
BO_AQUAMARINE = (102, 205, 170)
P1_SALMON = (250, 128, 114)
P2_KHAKI = (255, 165, 0)
BA_LAVANDAR = (230, 230, 250)

CIRCLES = []


class GameBoard(Board):
    """A subclass of Board, except with an additional instance attribute and methods in order
    to be implemented with pygame.

    Instance Attributes:
        - game_pieces: a mapping containing the piece locations used throughout the
        course of this project mapped to the equivalent locations within pygame.

    Representation Invariants:
        - len(self.game_peices) == self.width ** 2
        - self._tile_size // 2 - 3 != 0
    """

    # Game Pieces must be mapped from pygame locations to our locations
    # A Column Attribute is required and should behave as a stack.
    # Game Mode True/False Attribute Will be implemented in a bit

    pieces_to_location: {tuple[float, float]: tuple[int, int]}
    column_stack: {float: list[float]}
    _window: pygame.Surface
    _tile_size: int

    def __init__(self, width: int = 7) -> None:
        """Initialize this board with the dimensions of width by width.
                Preconditions:
                    - width == 7
                """
        super().__init__(width)
        self._tile_size = 75

        rows, columns = width, width
        self._window = pygame.display.set_mode((columns * self._tile_size, (rows + 1) * self._tile_size))
        background = BA_LAVANDAR
        self._window.fill(background)

        self.pieces_to_location = {}
        for row in range(rows):
            for column in range(columns):
                x = column * self._tile_size + 1 / 2 * self._tile_size
                y = (1 + row) * self._tile_size + self._tile_size / 2
                i = (width - 1) - row
                j = column
                self.pieces_to_location[(x, y)] = (i, j)

        self.column_stack = {}
        for column in range(columns):
            x = column * self._tile_size + 1 / 2 * self._tile_size
            y = [(1 + row) * self._tile_size + self._tile_size / 2 for row in range(rows)]
            self.column_stack[x] = y

    def run_game(self) -> Optional[tuple[str, set[Piece]]]:
        """Run the game. If any player wins, returns player and path of win."""

        # pygame.init()
        #
        # pygame.display.set_caption('FeelinConnected')
        #
        # pygame.display.flip()
        # clock = pygame.time.Clock()
        #
        # # Slider Colour and Token Colour must behave according to player turns.
        # slider_colours = [P1_SALMON, P2_KHAKI]
        # color_index = 0
        # color = slider_colours[color_index]
        # slider_x = self._tile_size
        # slider_y = self._tile_size - (self._tile_size // 2)
        #
        # self.draw_game_slots()
        #
        # finished = False
        # while not finished:
        #
        #     if self.get_winner() is not None:
        #         # Note: This is temporary, does not account for ties.
        #         self._window.fill(slider_colours[(color_index + 1) % len(slider_colours)])
        #         pygame.display.update()
        #         return self.get_winner()
        #
        #     clock.tick(60)
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             finished = True
        #         if event.type == pygame.MOUSEMOTION:
        #
        #             mouse_x = event.pos[0]
        #             if mouse_x < slider_x and slider_x > (self.width * self._tile_size) - (self.width * self._tile_size - 40):
        #                 slider_x -= 10
        #             if mouse_x > slider_x and slider_x < (self.width * self._tile_size - 40):
        #                 slider_x += 10
        #
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #
        #             collisions = [circle.collidepoint(event.pos) for circle in CIRCLES]
        #             if any(collisions):
        #
        #                 color_index = (color_index + 1) % len(slider_colours)
        #                 color = slider_colours[color_index]
        #
        #                 colour = slider_colours[(color_index + 1) % len(slider_colours)]
        #                 self.place_game_piece(colour, collisions)
        #
        #     pygame.draw.rect(self._window, BA_LAVANDAR, (0, 0, self.width * self._tile_size, self._tile_size))
        #     pygame.draw.circle(self._window, color, (slider_x, slider_y), self._tile_size // 2 - 3)
        #
        #     pygame.display.update()
        # quit()

        tree = None
        p2 = GreedyPlayer(tree, "P2")

        pygame.init()

        pygame.display.set_caption('FeelinConnected')

        pygame.display.flip()
        clock = pygame.time.Clock()

        # Slider Colour and Token Colour must behave according to player turns.
        slider_colours = [P1_SALMON, P2_KHAKI]
        color_index = 0
        color = slider_colours[color_index]
        slider_x = self._tile_size
        slider_y = self._tile_size - (self._tile_size // 2)

        self.draw_game_slots()

        finished = False
        while not finished:

            clock.tick(60)
            if not self.first_player_turn() and self.get_winner() is None:
                move = p2.make_move(self)
                self.make_move(move, "P2")

                move_loc = tuple()
                for key in self.pieces_to_location:
                    if self.pieces_to_location[key] == move.location:
                        move_loc = key

                x_cord = move_loc[0]
                y_cord = max(self.column_stack[x_cord])
                pygame.draw.circle(self._window, P2_KHAKI, (x_cord, y_cord), self._tile_size // 2 - 3)
                self.column_stack[x_cord].remove(y_cord)

            if self.first_player_turn() and self.get_winner() is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        finished = True
                    if event.type == pygame.MOUSEMOTION:

                        mouse_x = event.pos[0]
                        if mouse_x < slider_x and slider_x > (self.width * self._tile_size) - (
                                self.width * self._tile_size - 40):
                            slider_x -= 10
                        if mouse_x > slider_x and slider_x < (self.width * self._tile_size - 40):
                            slider_x += 10

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        collisions = [circle.collidepoint(event.pos) for circle in CIRCLES]
                        if any(collisions):
                            # color_index = (color_index + 1) % len(slider_colours)
                            # color = slider_colours[color_index]

                            # colour = slider_colours[(color_index + 1) % len(slider_colours)]
                            self.place_game_piece(P1_SALMON, collisions)

            else:
                # Note: This is temporary, does not account for ties.
                self._window.fill("Green")
                pygame.display.update()
                return self.get_winner()

            pygame.draw.rect(self._window, BA_LAVANDAR, (0, 0, self.width * self._tile_size, self._tile_size))
            pygame.draw.circle(self._window, "red", (slider_x, slider_y), self._tile_size // 2 - 3)

            pygame.display.update()
        quit()

    def draw_game_slots(self) -> None:
        """Initialize a pygame window which contains the specified width.
        """
        global CIRCLES
        rows, columns = self.width, self.width

        pygame.draw.rect(surface=self._window,
                         color=BO_AQUAMARINE,
                         rect=pygame.Rect(0, self._tile_size, columns * self._tile_size, rows * self._tile_size))
        for row in range(rows):
            for column in range(columns):
                x = column * self._tile_size + 1 / 2 * self._tile_size
                y = (1 + row) * self._tile_size + self._tile_size / 2
                circle = pygame.draw.circle(self._window, BA_LAVANDAR, (x, y), self._tile_size // 2 - 3)
                CIRCLES.append(circle)

        pygame.display.update()

    def place_game_piece(self, colour: tuple, collisions: list) -> None:
        """place a game piece within the specified player position."""

        new_color = colour
        collision_i = collisions.index(True)

        x_pos = CIRCLES[collision_i].centerx + 0.5
        y_pos = max(self.column_stack[x_pos])
        new_game_piece = x_pos, y_pos

        location = self.pieces_to_location[new_game_piece]
        new_piece = self.pieces[location]

        # self.player_moves["P1"].append(new_piece)
        self.make_move(new_piece, "P1")

        pygame.draw.circle(self._window, new_color, new_game_piece, self._tile_size // 2 - 3)
        self.column_stack[x_pos].remove(y_pos)

        pygame.display.update()

# class GamePiece(Piece):
#     """A subclass of Piece, except with additional methods in order
#     to be implemented with pygame."""
#
#     def __int__(self, location: tuple[int, int]):
#         """Initialize this piece with the given location and no connections to other pieces."""
#
#         super().__init__(location)
