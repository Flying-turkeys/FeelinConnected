"""CSC111 Winter 2023 Final Project: Feelin Connected

File Information
===============================
This file contains the data classes that will compose the AI used to create the Connect 4 game.

This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""

import random
from typing import Optional
from board import Board
from board import Piece
import game_tree as gt


def generate_game_tree(root_move: Piece, game_state: Board, d: int) -> gt.GameTree:
    """Generate a complete game tree of depth d for all valid moves from the current game_state.
    Note that this function can only generate subtrees if the game_state is not a starting state.
    For the returned GameTree:
        - Its root move is root_move.
        - It contains all possible move sequences of length <= d from game_state.
        - If d == 0, a size-one GameTree is returned.
    Preconditions:
        - d >= 0
        - game_state is not a starting game state
        - root_move is the last move made in game_state
    """
    game_tree = gt.GameTree(root_move)
    possibles = game_state.possible_moves()
    if root_move in possibles:
        possibles.remove(root_move)
    if game_state.get_winner() is not None:
        if game_state.get_winner()[0] == 'P1':
            game_tree.player_winning_probability['P1'] = 1.0
        if game_state.get_winner()[0] == 'P2':
            game_tree.player_winning_probability['P2'] = 1.0
        return game_tree
    if d == 0:
        return game_tree
    elif game_state.first_player_turn():
        for move in possibles:
            if gt.score_of_move(move, game_state, 'P1') >= 1:
                new_state = game_state.copy_and_record_move(move.location, 'P1')
                game_tree.add_subtree(generate_game_tree(new_state.pieces[move.location], new_state, d - 1))
    else:
        for move in possibles:
            if gt.score_of_move(move, game_state, 'P2') >= 1:
                new_state = game_state.copy_and_record_move(move.location, 'P2')
                game_tree.add_subtree((generate_game_tree(new_state.pieces[move.location], new_state, d - 1)))
    return game_tree


class AbstractPlayer:
    """Abstract class representing a specific player playing the game"""
    status: Board

    def make_move(self, board: Board) -> None:
        """Abstract method for a player making a move on the board"""
        raise NotImplementedError


class RandomPlayer(AbstractPlayer):
    """Connect 4 player which uses random moves to play"""

    def make_move(self, board: Board) -> Piece:
        """Makes a random move based off of a boards possible moves"""
        possible_moves = board.possible_moves()
        return random.choice(list(possible_moves))


class GreedyPlayer(AbstractPlayer):
    """Connect 4 player which uses a game tree and other logical calculations to play"""
    # Private Instance Attributes:
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves. If None, then this
    #       player behaves random
    _game_tree: Optional[gt.GameTree]
    player_id: str
    opponent_id: str

    def __init__(self, tree: Optional[gt.GameTree], player_id: str) -> None:
        """Initializing this player with corresponding type of player
        Preconditons:
            - player_id == "P1" or player_id == "P2"
            - tree is valid tree when paramater is passed
        """
        self._game_tree = tree
        self.player_id = player_id
        if player_id == 'P1':
            self.opponent_id = 'P2'
        else:
            self.opponent_id = 'P1'

    def make_move(self, board: Board) -> tuple[Piece, str]:
        """Uses logical calculations and a game tree to make a good move on the board
        Returns a tuple with the move and the message displayed"""
        possible_moves = board.possible_moves()

        random_move = random.choice(list(possible_moves))
        opponent_move = board.player_moves[self.opponent_id][-1]
        for move in possible_moves:
            if move.location[0] in {opponent_move.location[0] - 1, opponent_move.location[0] + 1}:
                random_move = move
                break

        if self._game_tree is None:  # The first move of the AI
            assert all(random_move not in board.player_moves[key] for key in board.player_moves)
            return (random_move, 'Random Move')

        else:
            # Goes into opponents move in the subtree
            if opponent_move != self._game_tree.move:
                self._game_tree = self._game_tree.find_subtree_by_move(opponent_move.location)

            # Checks if there is a crucial move to make
            crucial_move = self.check_crucial_move(possible_moves, board)
            if crucial_move:
                return crucial_move

            # Orders moves based on best winning probability from game tree
            sorted_subs = sorted(self._game_tree.get_subtrees(),
                                 key=lambda subtree: subtree.player_winning_probability[self.player_id],
                                 reverse=True)
            # Gets best move and checks if the move leads to a winning move for opponent
            # If it leads to an opponent next winning move, take the next best move
            i = 0
            sub = sorted_subs[i]
            while sub.player_winning_probability[self.opponent_id] == 1.0 and i < len(sorted_subs) - 1:
                i += 1
                sub = sorted_subs[i]

            # If every move in the tree make leads to a good move for the opponent
            # Make an educated move instead, avoiding the game tree moves
            new_possibles = {move for move in possible_moves if move.location != sub.move.location}
            if sub.player_winning_probability[self.opponent_id] == 1.0 and new_possibles != set():
                return (self.educated_move(new_possibles, board), 'Educated Move')

            self._game_tree = sub
            assert all(sub.move not in board.player_moves[key] for key in board.player_moves)
            return (sub.move, "Umm let me think")

    def check_crucial_move(self, possible_moves: set[Piece], board: Board) -> Optional[tuple[Piece, str]]:
        """Returns a move if either p1 or p2 are can make a move to win. If AI has a winning move
        it will take that move. If the opponent has a winning move it will block that move. If both have an
        opprotunity to win the AI will choose the move to make itself win.
        Preconditions:
            - possible_moves are valid moves on the board
        """
        for move in possible_moves:
            hypo1 = board.copy_and_record_move(move.location, self.player_id)
            if hypo1.get_winner() is not None and hypo1.get_winner()[0] == self.player_id:
                assert all(move not in board.player_moves[key] for key in board.player_moves)
                return (move, 'I win')
        for move in possible_moves:
            hypo2 = board.copy_and_record_move(move.location, self.opponent_id)
            if hypo2.get_winner() is not None and hypo2.get_winner()[0] == self.opponent_id:
                assert all(move not in board.player_moves[key] for key in board.player_moves)
                return (move, 'Get Blocked')
        return None

    def educated_move(self, possible_moves: set[Piece], board: Board) -> Piece:
        """Returns a piece/move that makes the most connections in a weighted form
        Precondition:
            - possible_moves are valid moves on the board
        """
        score_so_far = {}
        for move in possible_moves:
            hypo_state = board.copy_and_record_move(move.location, self.player_id)
            lengths_so_far = []
            for direction in move.connections:
                num_connection = len(hypo_state.pieces[move.location].find_path(set(), direction))
                if num_connection != 1:
                    lengths_so_far.append(num_connection)
            if len(lengths_so_far) == 0:
                score_so_far[move] = 0
            else:
                score_so_far[move] = sum(lengths_so_far) / len(lengths_so_far)
        return max(score_so_far, key=lambda key: score_so_far[key])


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'max-nested-blocks': 4,
        'extra-imports': ['random', 'game_tree', 'board'],
    })
