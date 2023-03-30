

"""CSC111 Winter 2023 Final Project: Feelin Connected
File Information
===============================
This file contains the tree used for the AI.
This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""
from __future__ import annotations
from typing import Optional
from board import Board, Piece
GAME_START_MOVE = '*'


class GameTree:
    """A decision tree for Connect 4 game.
    Each node in the tree stores a Connect 4 move.
    Instance Attributes:
        - move: the new game state being passed into the tree
    Representation Invariants:
        - self.move == GAME_START_MOVE or self.move is a Connect 4 move
        - all(key == self._subtrees[key].move for key in self._subtrees)
        - GAME_START_MOVE not in self._subtrees
        - 0.0 <= self.guesser_win_probability <= 1.0
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
        Note that this initializer uses optional arguments.
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
        """Return a string representation of this tree.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.
        The indentation level is specified by the <depth> parameter.
        Preconditions:
            - depth >= 0
        """
        if self.move == GAME_START_MOVE:
            turn = "P1"
        elif self.move.player == "P2":
            turn = "P2"
        else:
            turn = "P1"
        move_desc = f'{self.move} -> {turn} (% {self.player_winning_probability[turn] * 100})\n'
        str_so_far = '  ' * depth + move_desc
        for subtree in self._subtrees.values():
            str_so_far += subtree._str_indented(depth + 1)
        return str_so_far

    def add_subtree(self, subtree: GameTree) -> None:
        """Add a subtree to this game tree."""
        self._subtrees[subtree.move] = subtree
        self._update_player_win_probability()

    def _update_player_win_probability(self) -> None:
        """Recalculate the player win probability of this tree.
        """
        if self._subtrees:
            percentages_so_far_p1 = [subtree.player_winning_probability["P1"] for subtree in self.get_subtrees()]
            percentages_so_far_p2 = [subtree.player_winning_probability["P2"] for subtree in self.get_subtrees()]
            if self.first_player_turn():
                self.player_winning_probability["P1"] = sum(percentages_so_far_p1) / len(self.get_subtrees())
                self.player_winning_probability["P2"] = max(percentages_so_far_p2)
            else:
                self.player_winning_probability["P1"] = max(percentages_so_far_p1)
                self.player_winning_probability["P2"] = sum(percentages_so_far_p2) / len(self.get_subtrees())


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
