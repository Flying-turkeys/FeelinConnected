"""All testing not for handing in"""

from board import Board


def test_tabular_data() -> None:
    bd = Board(5)
    bd.make_move(bd._pieces[(0, 0)], "P1")
    bd.make_move(bd._pieces[(0, 1)], "P2")
    bd.make_move(bd._pieces[(3, 0)], "P1")
    bd.make_move(bd._pieces[(4, 1)], "P2")
    b = bd.board_to_tabular()
    for i in range(len(b)):
        print(b[len(b) - i - 1])
