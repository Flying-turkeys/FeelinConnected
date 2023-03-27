"""CSC111 Winter 2023 Final Project: Feelin Connected

File Information
===============================
This file contains the tree used for the AI.

This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""
from __future__ import annotations
from typing import Optional
from board import Board

GAME_START_MOVE = '-'
class GameTree:
    """A decision tree for Connect 4 game.

    Each node in the tree stores a Connect 4 move.

    Instance Attributes:
        - move: the new game state being passed into the tree
    Representation Invariants:
        - self.move == GAME_START_MOVE or self.move is a valid Adversarial Wordle move
        - all(key == self._subtrees[key].move for key in self._subtrees)
        - GAME_START_MOVE not in self._subtrees  # since it can only appear at the very top of a game tree
        - 0.0 <= self.guesser_win_probability <= 1.0
    """
    move: tuple[int, int]
    player_winning_probability: dict[str, float]
    _subtrees: dict[tuple[int, int], GameTree]

    # Private Instance Attributes:
    #  - _subtrees:
    #      the subtrees of this tree, which represent the game trees after a possible
    #      move by the current player. Unlike the Tree representation in lecture,
    #      this collection is a MAPPING where the values are GameTrees, and associated
    #      keys are the moves at the root of each subtree. See the last representation
    #      invariant above.
    def __init__(self, move: tuple[int, int] = GAME_START_MOVE,
                 p1_win_prob: float = 0.0, p2_win_prob: float = 0.0) -> None:
        """Initialize a new game tree.

        Note that this initializer uses optional arguments.

        >>> game = GameTree()
        >>> game.move == GAME_START_MOVE
        True
        """
        self.move = move
        self._subtrees = {}
        self.player_winning_probability['P1'] = p1_win_prob
        self.player_winning_probability['P2'] = p2_win_prob

    def get_subtrees(self) -> list[GameTree]:
        """Return the subtrees of this game tree."""
        return list(self._subtrees.values())

    def find_subtree_by_move(self, move: tuple[int, int]) -> Optional[GameTree]:
        """Return the subtree corresponding to the given move.

        Return None if no subtree corresponds to that move.
        """
        if move in self._subtrees:
            return self._subtrees[move]
        else:
            return None
