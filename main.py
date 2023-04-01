"""CSC111 Winter 2023 Final Project: Feelin Connected
File Information
===============================
This file contains the the functions calls to run the program from start to finish.
This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""


if __name__ == '__main__':
    from board import Board
    from gameplay import GameBoard
    # from players import GreedyPlayer, RandomPlayer, generate_game_tree

    b = GameBoard()
    b.run_pvc_state()

    # bd = Board(6)
    # tree = None
    # #bd.make_move(bd.pieces[(1, 2)], "P2")
    #
    # p1 = Person()
    # p2 = GreedyPlayer(tree, "P2")
    #
    # print("START")
    # for i in range(len(bd.board_to_tabular())):
    #     print(bd.board_to_tabular()[len(bd.board_to_tabular()) - i - 1])
    # count = 0
    # while bd.get_winner() is None:
    #     if bd.get_winner() is None:
    #         move1 = p1.make_move(bd)
    #         bd.make_move(move1, "P1")
    #         if count >= 1:
    #             tree = generate_game_tree(bd.player_moves['P1'][-1], bd, 4)
    #             p2 = GreedyPlayer(tree, "P2")
    #     print("P1 MOVE --------")
    #     for i in range(len(bd.board_to_tabular())):
    #         print(bd.board_to_tabular()[len(bd.board_to_tabular()) - i - 1])
    #     if bd.get_winner() is None:
    #         print("P2 MOVE --------")
    #         move2 = p2.make_move(bd)
    #         bd.make_move(move2, "P2")
    #         for i in range(len(bd.board_to_tabular())):
    #             print(bd.board_to_tabular()[len(bd.board_to_tabular()) - i - 1])
    #     count += 1
    # print(bd.get_winner())
