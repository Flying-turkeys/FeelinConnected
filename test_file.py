"""All testing not for handing in"""

from board import Board, Piece
from players import generate_game_tree


def test_game_tree():
    bd = Board(5)
    bd.make_move(bd.pieces[(0, 0)], "P1")
    bd.make_move(bd.pieces[(0, 1)], "P2")
    bd.make_move(bd.pieces[(0, 2)], "P1")
    bd.make_move(bd.pieces[(0, 3)], "P2")
    bd.make_move(bd.pieces[(0, 4)], "P1")
    print(generate_game_tree('*', bd, 4))


def test_copy():
    bd = Board(5)
    c = bd.copy_and_record_move((0, 0), "P1")
    b = c.board_to_tabular()
    for i in range(len(b)):
        print(b[len(b) - i - 1])

    k = c.copy_and_record_move((1, 0), "P2")
    print("--------------")
    b = k.board_to_tabular()
    for i in range(len(b)):
        print(b[len(b) - i - 1])

    print("--------------")
    original = bd.board_to_tabular()
    for i in range(len(original)):
        print(original[len(original) - i - 1])
