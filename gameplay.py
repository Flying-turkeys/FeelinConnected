"""CSC111 Winter 2023 Final Project: Feelin Connected

File Information
===============================
This file contains any and all code required to run a pygame version of our Connect 4 implementation.

This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""
import random
from typing import Optional
import pygame
from board import Board, Piece
from players import GreedyPlayer, generate_game_tree
from gameplay_additions import Button


# Colours used within the implementation:
# SALMON KHAKI PIECES WITH AQUAMARINE BOARD, LIGHT GREY BACKGROUND
BO_AQUAMARINE = (102, 205, 170)
P1_SALMON = (250, 128, 114)
P2_KHAKI = (255, 165, 0)
BA_LAVANDAR = (230, 230, 250)
THISTLE = (216, 191, 216)
RANDOM_COLOURS = [
    (102, 205, 170),
    (250, 128, 114),
    (255, 165, 0),
    (205, 92, 92),
    (152, 251, 152),
    (255, 127, 80),
    (255, 91, 71)
]


class GameBoard(Board):
    """A subclass which helps visualize the graph implementmentation of the Board class.
    The visualization is fostered through pygame methods, and allows you to play the Connect 4
    game.

    Instance Atrributes:
        - slots:
            a list of pygame rectangles that represent each slot (either filled or unfilled with a token) on the board
        - column_space:
            a mapping of the pygame x-coordidnates of each column to a set of all remaining row y-coordinates
        - game_state:
            a str, either PVP or PVC, which determines whether the game should be played
            utilizing two player inputs (PVP), versus a player input and a Computer/AI input (PVC)
    Representation Invarients:
        - len(slots) == self.width ** 2
        - self.game_state in {'PVP', 'PVC', 'unspecified'}
    """
    # Private Instance Attributes:
    #   - _proportionality: an integer which dicates the size of each item on the board, since it
    #      is proproptional to everything on the pygame surface.

    slots: list[pygame.Rect]
    column_spaces: dict[float: list[float]]
    game_state: str
    _proportionality: int

    def __init__(self, width: int = 7) -> None:
        """Intialize the game board with the dimentions of width by width (default 7),
        and the respective attirbutes.
        """
        super().__init__(width)
        self._proportionality = 75
        self.slots = []
        self.column_spaces = {}
        self.game_state = 'unspecified'

    def draw_slots(self, surface: pygame.Surface) -> None:
        """Draw each slot of the gameboard on the pygame surface with respects to its width."""

        ################################################################
        # Background:

        pygame.draw.rect(surface=surface,
                         color=BO_AQUAMARINE,
                         rect=pygame.Rect(0, self._proportionality, self.width * self._proportionality,
                                          self.width * self._proportionality))

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
            x = x * self._proportionality + self._proportionality / 2
            y = self._proportionality * int_conversion[y] + self._proportionality / 2

        elif isinstance(x, float) and isinstance(y, float):
            x = int((x - self._proportionality / 2) / self._proportionality)
            y = float_conversion[int((y - self._proportionality / 2) / self._proportionality)]

        else:
            raise ValueError

        new_coordinate = (x, y)

        return new_coordinate

    def remaining_column_space(self, x_coordinate: float) -> Optional[float]:
        """Return the remaining pygame y-coordinate in the column pertaining to x-coordintate
        on the game surface."""

        remaining_cords = self.column_spaces[x_coordinate]
        # min_y = self._proportionality + self._proportionality / 2

        if len(remaining_cords):
            coordinate = max(remaining_cords)
            self.column_spaces[x_coordinate].remove(coordinate)
            return coordinate
        return None
        # else:
        #     print('You cannot place there anymore!')
        #     return min_y

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

    def player_click_to_coordinates(self, clicks: list[bool]) -> Optional[tuple[float, float]]:
        """Depending on where the player clicks on the game surface (given through the
        index of the list, clicks), return the pygame coordinates for where the token should be placed."""

        index_of_click = clicks.index(True)
        clicked_circle = self.slots[index_of_click]

        x_cord = clicked_circle.centerx + 0.5  # In order to ensure a float is returned.
        y_cord = self.remaining_column_space(x_cord)
        if y_cord is not None:
            return (x_cord, y_cord)
        else:
            return None

    def visualize_and_record_move(self, move: Piece, surface: pygame.Surface) -> None:
        """Record the move within the board graph and equally display the move on the
        game surface."""

        coordinates = move.location

        # Visualize move:
        if not isinstance(coordinates[0], float):
            coordinates = self.convert_coordinates(coordinates)

        self.piece_drop_animation(coordinates[0], surface)
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
                self.fill_winner_colour(surface)
                pygame.display.update()
                pygame.display.quit()

            else:
                surface.fill(BA_LAVANDAR)
                pygame.display.update()
                pygame.display.quit()

            # display the menu again with new game options.
            self.__init__()
            self.run_game()

    def fill_winner_colour(self, surface: pygame.Surface) -> None:
        """If a player has won, fill the winning sequence of moves with a darker colour."""

        dark_red = (220, 20, 60)
        dark_orange = (255, 255, 0)

        player = self.get_winner()[0]
        sequence = self.get_winner()[1]

        if player == 'P1':
            for circle in sequence:
                coordinates = self.convert_coordinates(tuple(circle))
                pygame.draw.circle(surface=surface,
                                   color=dark_red,
                                   center=coordinates,
                                   radius=self._proportionality // 2 - 3)
                pygame.display.update()
        else:

            for circle in sequence:
                coordinates = self.convert_coordinates(tuple(circle))
                pygame.draw.circle(surface=surface,
                                   color=dark_orange,
                                   center=coordinates,
                                   radius=self._proportionality // 2 - 3)
                pygame.display.update()

        pygame.time.wait(2000)

    def piece_drop_animation(self, x_coordinate: float, surface: pygame.Surface) -> None:
        """Add a dropping effect to where a game piece is being placed."""

        y_coordinates = self.column_spaces[x_coordinate]
        y_coordinates.sort()
        for y in y_coordinates:
            pygame.draw.circle(surface=surface,
                               color=self.determine_colour(),
                               center=(x_coordinate, y),
                               radius=self._proportionality // 2 - 3)
            pygame.display.update()
            pygame.time.wait(80)
            pygame.draw.circle(surface=surface,
                               color=BA_LAVANDAR,
                               center=(x_coordinate, y),
                               radius=self._proportionality // 2 - 3)
            pygame.display.update()

    def draw_slider(self, coordinates: tuple[float, float], surface: pygame.Surface) -> None:
        """Given the coordinates of the mouse position from the game while loop, create a
        game picce slider that allows a player to see which token they are placing.
        Preconditions:
            - self.game_state == "PVP"
        """
        pygame.draw.rect(surface, BA_LAVANDAR, (0, 0, self.width * self._proportionality, self._proportionality))
        pygame.draw.circle(surface=surface,
                           color=self.determine_colour(),
                           center=coordinates,
                           radius=self._proportionality // 2 - 3)

        pygame.display.update()

    def display_ai_message(self, message: str, surface: pygame.Surface) -> None:
        """Given a message produced by the AI in Player-verses-AI game state, dispplay that message at the
        top of the board.
        """
        font_type = pygame.font.Font('game_elements/Pixeltype.ttf', 45)
        text = font_type.render(message, True, 'black')
        surface.blit(text, (20, 28))
        pygame.display.update()
        pygame.time.wait(1500)
        pygame.draw.rect(surface, BA_LAVANDAR, (0, 0, self.width * self._proportionality, self._proportionality))
        pygame.display.update()

    def create_and_display_menu(self) -> None:
        """Create and display a menu from which you can select the game state the player wishes."""

        ################################################################
        # Initialize all necessary components of pygame and the button class:

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Menu')

        size = (self.width * self._proportionality, (self.width + 1) * self._proportionality)
        game_surface = pygame.display.set_mode(size)
        game_surface.fill(BA_LAVANDAR)
        pygame.display.flip()
        clock = pygame.time.Clock()

        # loads different font sizes
        font = pygame.font.Font('game_elements/Pixeltype.ttf', 35)
        font1 = pygame.font.Font('game_elements/Pixeltype.ttf', 30)
        font2 = pygame.font.Font('game_elements/Pixeltype.ttf', 25)
        # load pvp button images
        pvp_image = pygame.image.load('game_elements/button1_f.png').convert_alpha()
        pvp_image = pygame.transform.scale(pvp_image, (140, 140))
        pvp_hover = pygame.image.load('game_elements/button1-hovered_f.png').convert_alpha()
        pvp_hover = pygame.transform.scale(pvp_hover, (140, 140))
        # load pvc button images
        pvc_image = pygame.image.load('game_elements/button2_f.png').convert_alpha()
        pvc_image = pygame.transform.scale(pvc_image, (140, 140))
        pvc_hover = pygame.image.load('game_elements/button2-hovered_f.png').convert_alpha()
        pvc_hover = pygame.transform.scale(pvc_hover, (140, 140))

        ################################################################

        pvp_button = Button(game_surface.get_rect().width // 2 - 160, game_surface.get_rect().height // 2 - 20,
                            pvp_image, 6)
        pvc_button = Button(game_surface.get_rect().width // 2 + 20, game_surface.get_rect().height // 2 - 20,
                            pvc_image, 6)

        running = True
        while running:
            # draws random circles around border for effect
            pygame.draw.circle(game_surface, color=random.choice(RANDOM_COLOURS),
                               center=(random.randint(0, 600), random.randint(0, 700)),
                               radius=random.randint(1, 150))
            pygame.time.wait(100)

            clock.tick(60)

            pygame.draw.rect(game_surface, THISTLE,
                             pygame.Rect(self._proportionality - 10, self._proportionality * 1.5 - 50,
                                         self.width * self._proportionality - self._proportionality * 2 + 18,
                                         self.width * self._proportionality - self._proportionality + 15),
                             border_radius=15)

            pvp_button.display_buttons(surface=game_surface, pvp_image=pvp_image, pvp_hovered=pvp_hover,
                                       pvc_image=pvc_image, pvc_hover=pvc_hover)
            pvc_button.display_buttons(surface=game_surface, pvp_image=pvp_image, pvp_hovered=pvp_hover,
                                       pvc_image=pvc_image, pvc_hover=pvc_hover)

            if pvp_button.pressed or pvc_button.pressed:
                running = False

            message1 = font.render("Welcome to FeelinConnected:", True, 'black')
            game_surface.blit(message1, (120, 150))
            message2 = font1.render("A Connect4 Special Edition", True, 'black')
            game_surface.blit(message2, (140, 185))
            message3 = font2.render("By Flying Turkeys", True, 'black')
            game_surface.blit(message3, (300, 500))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.update()
        pygame.display.quit()

        if pvp_button.pressed:
            self.game_state = "PVP"
        else:
            self.game_state = "PVC"

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

        slider_x = self._proportionality
        slider_y = self._proportionality - (self._proportionality // 2)

        running = True
        while running:
            self.check_winner(game_surface)

            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEMOTION:
                    mouse_x = event.pos[0]
                    if mouse_x < slider_x and slider_x > (self.width * self._proportionality) - (
                            self.width * self._proportionality - 40):
                        slider_x -= 10
                    if mouse_x > slider_x and slider_x < (self.width * self._proportionality - 40):
                        slider_x += 10

                    self.draw_slider((slider_x, slider_y), game_surface)

                if event.type == pygame.MOUSEBUTTONDOWN:

                    clicks = [slot.collidepoint(event.pos) for slot in self.slots]
                    if any(clicks):
                        self.check_winner(game_surface)
                        new_move = self.player_click_to_coordinates(clicks)
                        if new_move is None:
                            break
                        convert_cord = self.convert_coordinates(new_move)
                        game_piece = self.pieces[convert_cord]
                        self.visualize_and_record_move(game_piece, game_surface)
                        self.check_winner(game_surface)
            self.check_winner(game_surface)
            try:
                pygame.display.update()
            except pygame.error:
                return self.get_winner()

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
            self.check_winner(game_surface)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

            if not self.first_player_turn():
                new_move = ai_player.make_move(self)
                self.display_ai_message(new_move[1] + '...', game_surface)
                self.visualize_and_record_move(new_move[0], game_surface)
                convert_move = self.convert_coordinates(new_move[0].location)
                self.column_spaces[convert_move[0]].remove(convert_move[1])
                self.check_winner(game_surface)
                iteration += 1
            else:
                # self.display_ai_message("Your Turn", game_surface)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        clicks = [slot.collidepoint(event.pos) for slot in self.slots]
                        if any(clicks):
                            self.check_winner(game_surface)
                            new_move = self.player_click_to_coordinates(clicks)
                            if new_move is None:
                                break
                            convert_cord = self.convert_coordinates(new_move)
                            game_piece = self.pieces[convert_cord]
                            self.visualize_and_record_move(game_piece, game_surface)
                            self.check_winner(game_surface)
                            iteration += 1
                            if iteration >= 3:
                                tree = generate_game_tree(self.player_moves['P1'][-1], self, 3)
                                ai_player = GreedyPlayer(tree, 'P2')
            self.check_winner(game_surface)
            try:
                pygame.display.update()
            except pygame.error:
                return self.get_winner()

        quit()

    def run_game(self) -> None:
        """Run the game implementation."""

        self.create_and_display_menu()

        if self.game_state == 'PVP':
            self.run_pvp_state()
        elif self.game_state == 'PVC':
            self.run_pvc_state()
        else:
            pass


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'max-nested-blocks': 4,
        'extra-imports': ['game_tree',
                          'board',
                          'pygame',
                          'players',
                          'random',
                          'gameplay_additions',
                          'typing'],
        'disable': ['unused-import',
                    'too-many-branches',
                    'too-many-nested-blocks',
                    'too-many-locals'],

    })
