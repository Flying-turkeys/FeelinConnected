"""All testing not for handing in"""

from board import Board, Piece
from players import generate_game_tree


def test_game_tree():
    b = Board(5)
    print(generate_game_tree('*', b, 3))


def test_copy():
    bd = Board(5)
    c = bd.copy_and_record_move((0, 0), "P1")
    b = c.board_to_tabular()
    for i in range(len(b)):
        print(b[len(b) - i - 1])
    print(c.player_moves)

    k = c.copy_and_record_move((1, 0), "P2")
    print("--------------")
    b = k.board_to_tabular()
    for i in range(len(b)):
        print(b[len(b) - i - 1])
    print(k.player_moves)

    print("--------------")
    original = bd.board_to_tabular()
    for i in range(len(original)):
        print(original[len(original) - i - 1])


def test_winner():
    bd = Board(5)
    bd.make_move(bd.pieces[(0, 0)], "P1")
    bd.make_move(bd.pieces[(0, 1)], "P2")
    bd.make_move(bd.pieces[(0, 2)], "P1")
    bd.make_move(bd.pieces[(0, 3)], "P1")
    bd.make_move(bd.pieces[(0, 4)], "P1")

    bd.make_move(bd.pieces[(1, 0)], "P2")
    bd.make_move(bd.pieces[(1, 1)], "P2")
    bd.make_move(bd.pieces[(1, 2)], "P1")
    bd.make_move(bd.pieces[(1, 3)], "P1")
    bd.make_move(bd.pieces[(1, 4)], "P1")

    bd.make_move(bd.pieces[(2, 0)], "P1")
    bd.make_move(bd.pieces[(2, 1)], "P2")
    bd.make_move(bd.pieces[(2, 2)], "P2")
    bd.make_move(bd.pieces[(2, 3)], "P2")
    bd.make_move(bd.pieces[(2, 4)], "P1")

    bd.make_move(bd.pieces[(3, 0)], "P2")
    bd.make_move(bd.pieces[(3, 1)], "P1")
    bd.make_move(bd.pieces[(3, 2)], "P2")
    bd.make_move(bd.pieces[(3, 3)], "P1")
    bd.make_move(bd.pieces[(3, 4)], "P2")

    bd.make_move(bd.pieces[(4, 0)], "P1")
    bd.make_move(bd.pieces[(4, 1)], "P2")
    bd.make_move(bd.pieces[(4, 2)], "P1")
    bd.make_move(bd.pieces[(4, 3)], "P1")
    bd.make_move(bd.pieces[(4, 4)], "P1")

    b = bd.board_to_tabular()
    for i in range(len(b)):
        print(b[len(b) - i - 1])
    print(bd.possible_moves())


def test_tabular_data() -> None:
    bd = Board(5)
    bd.make_move(bd.pieces[(0, 0)], "P1")
    bd.make_move(bd.pieces[(0, 1)], "P1")
    bd.make_move(bd.pieces[(0, 2)], "P1")
    bd.make_move(bd.pieces[(0, 3)], "P2")
    bd.make_move(bd.pieces[(0, 4)], "P1")

    bd.make_move(bd.pieces[(2, 1)], "P1")
    bd.make_move(bd.pieces[(3, 2)], "P1")
    bd.make_move(bd.pieces[(4, 3)], "P1")
    bd.make_move(bd.pieces[(1, 0)], "P2")

    b = bd.board_to_tabular()
    for i in range(len(b)):
        print(b[len(b) - i - 1])
