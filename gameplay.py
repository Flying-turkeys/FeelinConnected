"""CSC111 Winter 2023 Final Project: Feelin Connected
File Information
===============================
This file contains any and all code required to run a pygame version of our
Connect 4 implementation.


This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""
import pygame
from board import Board, Piece
from typing import Optional
from players import GreedyPlayer, generate_game_tree


# Colours used within the implementation:
# SALMON KHAKI PIECES WITH AQUAMARINE BOARD, LIGHT GREY BACKGROUND
BO_AQUAMARINE = (102, 205, 170)
P1_SALMON = (250, 128, 114)
P2_KHAKI = (255, 165, 0)
BA_LAVANDAR = (230, 230, 250)


class GameBoard(Board):
    """A subclass which helps visualize the graph implementmentation of the Board class.
    The visualization is fostered through pygame methods, and allows you to play the Connect 4
    game.

    Instance Atrributes:
        - slots: a list of pygame rectangles that represent each slot (either filled
        or unfilled with a token) on the board
        - column_space: a mapping of the pygame x-coordidnates of each column to a set of all remaining
        row y-coordinates
        - game_state: a str, either PVP or PVC, which determines whether the game should be played
        utilizing two player inputs (PVP), versus a player input and a Computer/AI input (PVC)

    Representation Invarients:
        - len(slots) == self.width ** 2
        - self.game_state in {'PVP', 'PVC', 'unspecified'}
    """
    # Private Instance Attributes:
    #   - _proportionality: an integer which dicates the size of each item on the board, since it
    #      is proproptional to every surface.

    slots: list[pygame.Rect]
    column_spaces: dict[float: list[float]]
    game_state = str
    _proportionality = int

    def __init__(self, width: int = 7) -> None:
        """Intialize the game board with the dimentions of width by width (default 7),
        and the respective attirbutes.
        """
        super().__init__(width)
        self._proportionality = 75
        self.slots = []
        self.column_spaces = {}
        self.game_state = 'unspecified'

    def draw_slots(self, surface: pygame.Surface):
        """Draw each slot of the gameboard on the pygame surface with respects to its width."""

        ################################################################
        # Background:

        pygame.draw.rect(surface=surface,
                         color=BO_AQUAMARINE,
                         rect=pygame.Rect(0, self._proportionality, self.width * self._proportionality, self.width * self._proportionality))

        ################################################################

        all_x = set()
        all_y = set()
        for row in range(self.width):
            for column in range(self.width):
                x = column * self._proportionality + self._proportionality / 2
                y = (1 + row) * self._proportionality + self._proportionality / 2
                circle = pygame.draw.circle(surface=surface,
                                            color=BA_LAVANDAR,
                                            center=(x, y),
                                            radius=self._proportionality // 2 - 3)
                all_x.add(x)
                all_y.add(y)

                self.slots.append(circle)

        self.column_spaces = {x_cord: list(all_y) for x_cord in all_x}

        pygame.display.update()

    def convert_coordinates(self, coordinate: tuple) -> tuple:
        """For the given coordinate of either floats (if pygame coordinates),
        or ints (if cartesian coordinates) convert and return the opposite coordinate
        system. Therefore, cartesian coordinates will be converted to pygame coordinates
        and vise versa."""

        x, y = coordinate

        int_conversion = {a: self.width - a for a in range(self.width)}
        float_conversion = {self.width - a: a for a in range(self.width)}

        if isinstance(x, int) and isinstance(y, int):
            new_x = x * self._proportionality + self._proportionality / 2
            new_y = self._proportionality * int_conversion[y] + self._proportionality / 2

        elif isinstance(x, float) and isinstance(y, float):
            new_x = int((x - self._proportionality / 2) / self._proportionality)
            new_y = float_conversion[int((y - self._proportionality / 2) / self._proportionality)]

        else:
            raise ValueError

        new_coordinate = (new_x, new_y)

        return new_coordinate

    def remaining_column_space(self, x_coordinate: float) -> float:
        """Return the remaining pygame y-coordinate in the column pertaining to x-coordintate
        on the game surface."""

        remaining_cords = self.column_spaces[x_coordinate]
        min_y = self._proportionality + self._proportionality / 2

        if len(remaining_cords):
            coordinate = max(remaining_cords)
            self.column_spaces[x_coordinate].remove(coordinate)
            return coordinate
        else:
            print('You cannot place there anymore!')
            return min_y

    def determine_colour(self, opposite: bool = False) -> tuple[int, int, int]:
        """Return the colour that should be displayed on the game board. If opposite
         is True, return the opposing player colour."""

        if not opposite:
            if self.first_player_turn():
                return P1_SALMON
            else:
                return P2_KHAKI
        else:
            if self.first_player_turn():
                return P2_KHAKI
            else:
                return P1_SALMON

    def player_click_to_coordinates(self, clicks: list[bool]) -> tuple[float, float]:
        """Depending on where the player clicks on the game surface (given through the
        index of the list, clicks), return the pygame coordinates for where the token should be placed."""

        index_of_click = clicks.index(True)
        clicked_circle = self.slots[index_of_click]

        x_cord = clicked_circle.centerx + 0.5  # In order to ensure a float is returned.
        y_cord = self.remaining_column_space(x_cord)

        return (x_cord, y_cord)

    def visualize_and_record_move(self, move: Piece, surface: pygame.Surface) -> None:
        """Record the move within the board graph and equally display the move on the
        game surface."""

        coordinates = move.location

        # Visualize move:
        if not isinstance(coordinates[0], float):
            coordinates = self.convert_coordinates(coordinates)

        pygame.draw.circle(surface=surface,
                           color=self.determine_colour(),
                           center=coordinates,
                           radius=self._proportionality // 2 - 3)

        pygame.display.update()

        # Record move:
        if self.first_player_turn():
            self.make_move(move, 'P1')
        else:
            self.make_move(move, 'P2')

    def check_winner(self, surface: pygame.Surface) -> None:
        """Check to see if there is a winner within the game before proceeding into the
        game loop"""

        if self.get_winner() is not None:
            if self.get_winner()[0] != "Tie":
                surface.fill(self.determine_colour(True))
                pygame.display.update()
                print(self.get_winner()[0], "is the winner!")
                pygame.quit()

            else:
                surface.fill(BA_LAVANDAR)
                pygame.display.update()
                print('Hey its a tie! Try again next time.')
                pygame.quit()

    def run_pvp_state(self) -> None:
        """Run a Player-versus-player game."""

        ################################################################
        # Initialize all necessary components of pygame:

        pygame.init()
        pygame.display.set_caption('FeelinConnected')

        size = (self.width * self._proportionality, (self.width + 1) * self._proportionality)
        game_surface = pygame.display.set_mode(size)
        game_surface.fill(BA_LAVANDAR)
        pygame.display.flip()
        clock = pygame.time.Clock()

        ################################################################

        self.draw_slots(game_surface)

        running = True
        while running:

            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:

                    clicks = [slot.collidepoint(event.pos) for slot in self.slots]
                    if any(clicks):
                        new_move = self.player_click_to_coordinates(clicks)
                        convert_cord = self.convert_coordinates(new_move)
                        game_piece = self.pieces[convert_cord]
                        self.visualize_and_record_move(game_piece, game_surface)
                        self.check_winner(game_surface)

            pygame.display.update()

        quit()

    def run_pvc_state(self) -> None:
        """Run a Player-versus-Computer/AI game."""

        ################################################################
        # Initialize all necessary components of pygame:

        pygame.init()
        pygame.display.set_caption('FeelinConnected')

        size = (self.width * self._proportionality, (self.width + 1) * self._proportionality)
        game_surface = pygame.display.set_mode(size)
        game_surface.fill(BA_LAVANDAR)
        pygame.display.flip()
        clock = pygame.time.Clock()

        ################################################################
        tree = None
        ai_player = GreedyPlayer(tree, 'P2')

        self.draw_slots(game_surface)

        iteration = 0

        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

            if not self.first_player_turn():
                new_move = ai_player.make_move(self)
                self.visualize_and_record_move(new_move, game_surface)
                convert_move = self.convert_coordinates(new_move.location)
                self.column_spaces[convert_move[0]].remove(convert_move[1])
                self.check_winner(game_surface)
                iteration += 1
            else:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:

                        # if self.first_player_turn():
                        clicks = [slot.collidepoint(event.pos) for slot in self.slots]
                        if any(clicks):
                            new_move = self.player_click_to_coordinates(clicks)
                            convert_cord = self.convert_coordinates(new_move)
                            game_piece = self.pieces[convert_cord]
                            self.visualize_and_record_move(game_piece, game_surface)
                            self.check_winner(game_surface)
                            iteration += 1

                            if iteration >= 3:
                                tree = generate_game_tree(self.player_moves['P1'][-1], self, 4)
                                ai_player = GreedyPlayer(tree, 'P2')

            pygame.display.update()

        quit()

    def run_game(self) -> None:
        """Run the game implementation."""

        if self.game_state == 'PVP':
            self.run_pvp_state()

        elif self.game_state == 'PVC':
            self.run_pvc_state()

        else:
            print('Error: Game state is not specified')
