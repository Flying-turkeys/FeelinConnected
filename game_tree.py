"""CSC111 Winter 2023 Final Project: Feelin Connected

File Information
===============================
This file contains the tree used for the AI.

This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""

from board import Board


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
    move: list[list[int]]  # The vertical bar | means "or"

    # Private Instance Attributes:
    #  - _subtrees:
    #      the subtrees of this tree, which represent the game trees after a possible
    #      move by the current player. Unlike the Tree representation in lecture,
    #      this collection is a MAPPING where the values are GameTrees, and associated
    #      keys are the moves at the root of each subtree. See the last representation
    #      invariant above.
