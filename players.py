"""CSC111 Winter 2023 Final Project: Feelin Connected

File Information
===============================
This file contains the data classes that will compose the AI used to create the Connect 4 game.

This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""

from board import Board
from board import Piece
import copy
import random


class AbstractPlayer:
    """Abstract class representing a specific player playing the game"""
    status: Board

    # def __init__(self) -> None:
    #
    #     """Abstract method for initializing this player"""
    #     raise NotImplementedError

    def make_move(self, board: Board) -> None:
        """Abstract method for a player making a move on the board"""
        raise NotImplementedError


class Person(AbstractPlayer):
    """Abstract player who represents a real person playing"""

    # def __init__(self, board: Board) -> None:
    #     """Abstract method for initializing this player"""

    def make_move(self, board: Board) -> None:
        """Abstract method for a player making a move on the board"""


class RandomPlayer(AbstractPlayer):
    """Abstract player which uses random moves to play"""

    def make_move(self, board: Board) -> Piece:
        """Abstract method for a player making a move on the board"""
        possible_moves = board.possible_moves()
        return random.choice(list(possible_moves))


class GreedyPlayer(AbstractPlayer):
    """Abstract player which uses AI to play"""

    # def __init__(self, board: Board) -> None:
    #     """Abstract method for initializing this player"""

    def make_move(self, board: Board) -> None:
        """Abstract method for a player making a move on the board"""



if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
