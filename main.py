"""CSC111 Winter 2023 Final Project: Feelin Connected

File Information
===============================
This file contains the the functions calls to run the program from start to finish.

This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""


if __name__ == '__main__':
    from gameplay import GameBoard
    from players import GreedyPlayer, Person, generate_game_tree
    from board import Board
    
    b = GameBoard()
    b.run_game()

    ################################
    # For testing AI accuracy in console, comment out the code above and run the following
    ################################
    
#     bd = Board(7)
#     tree = None
#     p1 = Person()
#     p2 = GreedyPlayer(tree, "P2")

#     print("START")
#     for i in range(len(bd.board_to_tabular())):
#         print(bd.board_to_tabular()[len(bd.board_to_tabular()) - i - 1])
#     count = 0
#     while bd.get_winner() is None:
#         if bd.get_winner() is None:
#             move1 = p1.make_move(bd)
#             bd.make_move(move1, "P1")
#             if count >= 1:
#                 tree = generate_game_tree(bd.player_moves['P1'][-1], bd, 4)
#                 p2 = GreedyPlayer(tree, "P2")
#         print("P1 MOVE --------")
#         for i in range(len(bd.board_to_tabular())):
#             print(bd.board_to_tabular()[len(bd.board_to_tabular()) - i - 1])
#         if bd.get_winner() is None:
#             print("P2 MOVE --------")
#             move2 = p2.make_move(bd)
#             bd.make_move(move2[0], "P2")
#             for i in range(len(bd.board_to_tabular())):
#                 print(bd.board_to_tabular()[len(bd.board_to_tabular()) - i - 1])
#         count += 1
#     print(bd.get_winner())
