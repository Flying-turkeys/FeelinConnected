"""CSC111 Winter 2023 Final Project: Feelin Connected

File Information
===============================
This file contains the data classes that will compose the AI used to create the Connect 4 game.

This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""
from board import Board


class Player:
    """"""
    status: Board
    def __init__(self):
        """"""
        raise NotImplementedError

    def make_move(self):
        """"""
        raise NotImplementedError



class RandomGuesser(Player):
    """"""


class GreedyGuesser(Player):
    """"""


class Person(Player):
    """"""
