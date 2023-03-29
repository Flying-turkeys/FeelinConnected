"""CSC111 Winter 2023 Final Project: Feelin Connected
File Information
===============================
This file contains the data classes that will compose the AI used to create the Connect 4 game.
This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""
from typing import Optional
from board import Board, Piece
import game_tree as gt
import random


def generate_game_tree(root_move: Piece | str, game_state: Board, d: int) -> gt.GameTree:
    """Generate a complete game tree of depth d for all valid moves from the current game_state.

    For the returned GameTree:
        - Its root move is root_move.
        - It contains all possible move sequences of length <= d from game_state.
        - If d == 0, a size-one GameTree is returned.

    Preconditions:
        - d >= 0
        - root_move == a2_game_tree.GAME_START_MOVE or root_move is a valid move
        - if root_move == a2_game_tree.GAME_START_MOVE, then game_state is in the initial game state
        - if isinstance(root_move, str) and root_move != a2_game_tree.GAME_START_MOVE,\
            then (game_state.guesses[-1] == root_move) and (not game_state.is_guesser_turn())
        - if isinstance(root_move, tuple),\
            then (game_state.statuses[-1] == root_move) and game_state.is_guesser_turn()
    """
    game_tree = gt.GameTree(root_move)
    possibles = game_state.possible_moves()
    if root_move in possibles:
        possibles.remove(root_move)
    if d == 0:
        if game_state.get_winner() is not None:
            if game_state.get_winner()[0] == 'P1':
                game_tree.player_winning_probability['P1'] = 1.0
            if game_state.get_winner()[0] == 'P2':
                game_tree.player_winning_probability['P2'] = 1.0
        return game_tree
    elif game_state.first_player_turn():
        for move in possibles:
            new_state = game_state.copy_and_record_move(move.location, 'P1')
            game_tree.add_subtree(generate_game_tree(new_state.pieces[move.location], new_state, d - 1))
    else:
        for move in possibles:
            new_state = game_state.copy_and_record_move(move.location, 'P2')
            game_tree.add_subtree((generate_game_tree(new_state.pieces[move.location], new_state, d - 1)))
    return game_tree


class AbstractPlayer:
    """Abstract class representing a specific player playing the game"""
    status: Board

    # def __init__(self) -> None:
    #
    #     """Abstract method for initializing this player"""
    #     raise NotImplementedError

    def make_move(self, board: Board) -> None:
        """Abstract method for a player making a move on the board"""
        raise NotImplementedError


class Person(AbstractPlayer):
    """Abstract player who represents a real person playing"""

    # def __init__(self, board: Board) -> None:
    #     """Abstract method for initializing this player"""

    def make_move(self, board: Board) -> Piece:
        """Abstract method for a player making a move on the board"""


class RandomPlayer(AbstractPlayer):
    """Abstract player which uses random moves to play"""

    def make_move(self, board: Board) -> Piece:
        """Abstract method for a player making a move on the board"""
        possible_moves = board.possible_moves()
        return random.choice(list(possible_moves))


class GreedyPlayer(AbstractPlayer):
    """Abstract player which uses AI to play"""
    # Private Instance Attributes:
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves. If None, then this
    #       player behaves like aw.RandomGuesser.
    _game_tree: Optional[gt.GameTree]
    player_id: str
    opponent_id = str

    def __init__(self, tree: Optional[gt.GameTree], player_id: str) -> None:
        """Abstract method for initializing this player"""
        self._game_tree = tree
        self.player_id = player_id
        if player_id == 'P1':
            self.opponent_id = 'P2'
        else:
            self.opponent_id = 'P1'

    def make_move(self, board: Board) -> Piece:
        """Abstract method for a player making a move on the board"""
        possible_answers = board.possible_moves()
        random_move = random.choice(list(possible_answers))
        if self._game_tree is None:
            return random_move
        else:
            self._game_tree = self._game_tree.find_subtree_by_move(board.player_moves[self.opponent_id][-1])
            if self._game_tree is None or self._game_tree.get_subtrees() == []:
                return random_move
            else:
                sub = max(self._game_tree.get_subtrees(),
                          key=lambda subtree: subtree.player_winning_probability[self.player_id])
                sub_op = max(self._game_tree.get_subtrees(),
                             key=lambda subtree: subtree.player_winning_probability[self.opponent_id])
                if sub_op.player_winning_probability[self.opponent_id] == 1.0:
                    self._game_tree = sub_op
                    return sub_op.move
                self._game_tree = sub
                return sub.move


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
