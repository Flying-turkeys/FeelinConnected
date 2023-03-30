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
    from game_tree import GameTree



def run_game(p1 , p2, bd):
    while bd.get_winner() is None:
        move_1 = p1.make_move(bd)
        bd.make_move(move_1, "P1")
        move_2 = p2.make_move(bd)
        bd.make_move(move_2, "P2")
    return bd.get_winner()[0]

def run_learning_algorithm(exploration_probabilities: list[float]):
    results = []
    game_tree = GameTree()
    for prob in exploration_probabilities:
        board = Board(6)
        p1 = GreedyPlayer(game_tree, 'P1', prob)
        p2 = RandomPlayer()#GreedyPlayer(game_tree, 'P2', prob)
        game = run_game(p1, p2, board)
        move_sequence = board.sequence()
        if game == 'P1':
            game_tree.t(move_sequence, 1.0)
        else:
            game_tree.t(move_sequence, 0.0)

        results.append(game)
    print(results)
    return game_tree


def part3_runner():
    """Run example for Part 3.

    Please note that unlike part1_runner and part2_runner, this function is NOT tested.
    We encourage you to experiment with different exploration probability sequences
    to see how quickly you can develop a "winning" GameTree!
    """
    probabilities = []
    n = 200
    m = 100
    for i in range(n):
        probabilities.append(1 - i / n)
    probabilities.extend([0.0] * m)

    return run_learning_algorithm(probabilities)

if __name__ == '__main__':
    #part3_runner()
    bd = Board(4)
    tree = generate_game_tree("*", bd, 7)
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
