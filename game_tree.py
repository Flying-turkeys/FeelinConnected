"""CSC111 Winter 2023 Final Project: Feelin Connected

File Information
===============================
This file contains the tree used for the AI.

This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""

from __future__ import annotations
from typing import Optional
from board import Board
from board import Piece
GAME_START_MOVE = '*'


class GameTree:
    """A decision tree for Connect 4 game.
    Each node in the tree stores a Connect 4 move (Piece).
    Instance Attributes:
        - move: the new game state being passed into the tree
    Representation Invariants:
        - self.move == GAME_START_MOVE or isinstance(self.move, Piece)
        - all(key == self._subtrees[key].move for key in self._subtrees)
        - GAME_START_MOVE not in self._subtrees
        - all(key in {"P1", "P2} for key in self.player_winning_probability)
        - 0.0 <= self.player_winning_probability["P1"] <= 1.0
        - 0.0 <= self.player_winning_probability["P2"] <= 1.0
    """
    move: Piece | str
    player_winning_probability: dict[str, float]
    _subtrees: dict[Piece, GameTree]

    # Private Instance Attributes:
    #  - _subtrees:
    #      the subtrees of this tree, which represent the game trees after a possible
    #      move by the current player.
    def __init__(self, move: Piece | str = GAME_START_MOVE,
                 p1_win_prob: float = 0.0, p2_win_prob: float = 0.0) -> None:
        """Initialize a new game tree.
        >>> game = GameTree()
        >>> game.move == GAME_START_MOVE
        True
        """
        self.move = move
        self.player_winning_probability = {'P1': p1_win_prob, 'P2': p2_win_prob}
        self._subtrees = {}

    def get_subtrees(self) -> list[GameTree]:
        """Return the subtrees of this game tree."""
        return list(self._subtrees.values())

    def find_subtree_by_move(self, location: tuple[int, int]) -> Optional[GameTree]:
        """Return the subtree corresponding to the given move.
        Return None if no subtree corresponds to that move.
        """
        for piece in self._subtrees:
            if piece.location == location:
                return self._subtrees[piece]
        return None

    def first_player_turn(self) -> bool:
        """Return whether the NEXT move should be made by first player (P1)."""
        return self.move == GAME_START_MOVE or self.move.player == 'P2'

    def __str__(self) -> str:
        """Return a string representation of this tree."""
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.
        Preconditions:
            - depth >= 0
        """
        if self.move == GAME_START_MOVE:
            move_desc = f'{self.move} -> {"Start of Game Tree"}\n'
        elif self.move.player == "P2":
            move_desc = f'{self.move} -> {"P2"} ({self.player_winning_probability["P2"]})\n'
        else:
            move_desc = f'{self.move} -> {"P1"} ({self.player_winning_probability["P1"]})\n'
        str_so_far = '        ' * depth + move_desc
        for subtree in self._subtrees.values():
            str_so_far += subtree._str_indented(depth + 1)
        return str_so_far

    def add_subtree(self, subtree: GameTree) -> None:
        """Add a subtree to this game tree and update its winning probability"""
        self._subtrees[subtree.move] = subtree
        self._update_player_win_probability()

    def _update_player_win_probability(self) -> None:
        """Recalculate the player win probability of this tree for both players"""
        if self._subtrees:
            subs = self.get_subtrees()
            if self.first_player_turn():
                self.player_winning_probability["P1"] = max(subtree.player_winning_probability["P1"]
                                                            for subtree in subs)
                self.player_winning_probability["P2"] = sum(subtree.player_winning_probability["P2"]
                                                            for subtree in subs) / len(subs)
            else:
                self.player_winning_probability["P1"] = sum(subtree.player_winning_probability["P1"]
                                                            for subtree in subs) / len(subs)
                self.player_winning_probability["P2"] = max(subtree.player_winning_probability["P2"]
                                                            for subtree in subs)


def score_of_move(move: Piece, board: Board, player_id) -> float:
    """Returns score of connection"""
    hypo_state = board.copy_and_record_move(move.location, player_id)
    lengths_so_far = []
    for direction in move.connections:
        num_connection = len(hypo_state.pieces[move.location].find_path(set(), direction))
        if num_connection != 1:
            lengths_so_far.append(num_connection)
    if len(lengths_so_far) == 0:
        return 0
    else:
        return sum(lengths_so_far) / len(lengths_so_far)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'max-nested-blocks': 4,
        'extra-imports': ['board'],
    })
