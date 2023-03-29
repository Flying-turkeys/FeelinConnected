"""CSC111 Winter 2023 Final Project: Feelin Connected

File Information
===============================
This file contains the the functions calls to run the program from start to finish.

This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""
from board import Board
from players import Person, GreedyPlayer, RandomPlayer, generate_game_tree

if __name__ == '__main__':
    bd = Board(4)
    p1 = Person()
    tree = generate_game_tree("*", bd, 7)
    p2 = GreedyPlayer(tree, 0)
    print("START")
    for i in range(len(bd.board_to_tabular())):
        print(bd.board_to_tabular()[len(bd.board_to_tabular()) - i - 1])
    while bd.get_winner() is None:
        move1 = p1.make_move(bd)
        bd.make_move(move1, "P1")
        print("P1 MOVE --------")
        for i in range(len(bd.board_to_tabular())):
            print(bd.board_to_tabular()[len(bd.board_to_tabular()) - i - 1])
        print("P2 MOVE --------")
        move2 = p2.make_move(bd)
        bd.make_move(move2, "P2")
        for i in range(len(bd.board_to_tabular())):
            print(bd.board_to_tabular()[len(bd.board_to_tabular()) - i - 1])
