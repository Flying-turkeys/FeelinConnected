"""All testing not for handing in"""

from board import Board


def test_winner():
    bd = Board(5)
    bd.make_move(bd._pieces[(0, 0)], "P1")
    bd.make_move(bd._pieces[(0, 1)], "P1")
    bd.make_move(bd._pieces[(0, 2)], "P1")
    bd.make_move(bd._pieces[(0, 3)], "P1")
    bd.make_move(bd._pieces[(0, 4)], "P1")
    print(bd.get_winner_v2())

def test_tabular_data() -> None:
    bd = Board(5)
    bd.make_move(bd._pieces[(0, 0)], "P1")
    bd.make_move(bd._pieces[(0, 1)], "P2")
    bd.make_move(bd._pieces[(0, 2)], "P1")
    bd.make_move(bd._pieces[(0, 3)], "P2")
    bd.make_move(bd._pieces[(1, 0)], "P2")
    b = bd.board_to_tabular()
    for i in range(len(b)):
        print(b[len(b) - i - 1])
# (0,2), (1,0), (2,0), (3,1), (4,1)
