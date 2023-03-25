"""CSC111 Winter 2023 Final Project: Feelin Connected

File Information
===============================
This file contains the data classes that will compose the AI used to create the Connect 4 game.

This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""

from board import Board


class AbstractPlayer:
    """Abstract data type for a specific player playing the game"""
    status: Board

    def __init__(self) -> None:

        """Abstract method for initializing this player"""
        raise NotImplementedError

    def make_move(self) -> None:
        """Abstract method for a player making a move on the board"""
        raise NotImplementedError


class Person(AbstractPlayer):
    """Abstract player who represents a real person playing"""
    def __init__(self, board: Board) -> None:
        """Abstract method for initializing this player"""

    def make_move(self) -> None:
        """Abstract method for a player making a move on the board"""


class RandomGuesser(AbstractPlayer):
    """Abstract player which uses random guesses to play"""
    def __init__(self, board: Board) -> None:
        """Abstract method for initializing this player"""

    def make_move(self) -> None:
        """Abstract method for a player making a move on the board"""


class GreedyGuesser(AbstractPlayer):
    """Abstract player which uses AI to play"""
    def __init__(self, board: Board) -> None:
        """Abstract method for initializing this player"""

    def make_move(self) -> None:
        """Abstract method for a player making a move on the board"""


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
