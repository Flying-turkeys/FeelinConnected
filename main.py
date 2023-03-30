"""CSC111 Winter 2023 Final Project: Feelin Connected

File Information
===============================
This file contains the the functions calls to run the program from start to finish.

This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""


if __name__ == '__main__':
    pass
    from board import Board
    from players import Person, GreedyPlayer, RandomPlayer, generate_game_tree

    if __name__ == '__main__':
        bd = Board(6)
        # bd.make_move(bd.pieces[(0, 0)], "P1")
        # bd.make_move(bd.pieces[(1, 0)], "P2")
        # bd.make_move(bd.pieces[(0, 1)], "P1")
        # bd.make_move(bd.pieces[(1, 1)], "P2")
        # bd.make_move(bd.pieces[(0, 2)], "P1")
        tree = generate_game_tree("*", bd, 4)
        #bd.make_move(bd.pieces[(1, 2)], "P2")


        p2 = Person()
        p1 = GreedyPlayer(tree, "P1")

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
        print(bd.get_winner())
