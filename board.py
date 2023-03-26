"""CSC111 Winter 2023 Final Project: Feelin Connected

File Information
===============================
This file contains the data classes that will compose the graph used to create the Connect 4 game.

This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""

from __future__ import annotations
from typing import Optional
from players import AbstractPlayer as Player


class Piece:
    """A node that represents a piece in a Connect 4 board.

    Instance Attributes
        - player:
            The player who this piece belongs to. Can be None if no player has
            made a move in the location of the piece.
        - location:
            The address (i.e., unique identifier) of this node.
        - connections:
            A dictionary mapping the location of connection to a connection.

    Representation Invariants:
        - all(key in {'vertical', 'horizontal', 'left-diagonal', 'right-diagonal'} for key in self.connections)
        - all(point >= 0 for point in self.location)
        - all(self in conn.endpoints for conn in self.connections)
    """
    player: Optional[str]
    location: tuple[int, int]
    connections: dict[str, list[Connection]]

    def __init__(self, location: tuple[int, int]) -> None:
        """Initialize this piece with the given location and no connections to other pieces."""
        self.player = None
        self.location = location
        self.connections = {'vertical': [], 'horizontal': [], 'right-diagonal': [], 'left-diagonal': []}

    def update_piece(self, player: str) -> None:
        """Updates the player of the piece"""
        self.player = player

    def update_piece(self, player: str) -> None:
        """Updates the player of the piece"""
        self.player = player

    def __repr__(self) -> str:
        """Return a string representing this piece.

        >>> piece = Piece((0, 0))
        >>> piece
        Piece(0, 0)
        """
        return f'Piece{self.location}'


class Connection:
    """A link (or "edge") connecting two pieces on a Connect 4 board.

    Instance Attributes:
        - type: The direction (type) of connection two pieces make.
        - endpoints: The two pieces that are linked by this connection.

    Representation Invariants:
        - len(self.endpoints) == 2
        - self.type in {'vertical', 'horizontal', 'left-diagonal', 'right-diagonal'}
    """
    type: str
    endpoints: set[Piece]

    def __init__(self, n1: Piece, n2: Piece, direction: str) -> None:
        """Initialize an empty connection with the two given pieces.

        Also add this connection to n1 and n2.

        Raise ValueError if the connection is not valid. That is, the pieces are not adjacent in any way.

        Preconditions:
            - n1 != n2
            - n1 and n2 are not already connected by a connection
            - n1 and n2 make a valid connection on the board
        """
        self.type = direction
        self.endpoints = {n1, n2}

    def get_other_endpoint(self, piece: Piece) -> Piece:
        """Return the endpoint of this connection that is not equal to the given piece.

        Preconditions:
            - piece in self.endpoints
        """
        return (self.endpoints - {piece}).pop()

    def __repr__(self) -> str:
        """Return a string representing this connection.

        >>> connection = Connection(Piece((0, 0)), Piece((0, 1)))
        >>> repr(connection) in {'Connection(Piece(0, 0), Piece(0, 1))', 'Connection(Piece(0, 1), Piece(0, 0))'}
        True
        """
        endpoints = list(self.endpoints)
        return f'Connection({endpoints[0]}, {endpoints[1]})'


class Board:
    """A graph that represents a Connect 4 board and holds all empty and non-empty spaces/pieces.

    Instance Attributes:
        - moves: a mapping of all pieces to their location.
        - player_moves: moves categroized with p1 and p2
        - width: width of the board

    Representation Invariants:
        - len(self.player_moves) == 2
        - all(type in {'P1', 'P2'} for type in self.player_moves)
        - 5 <= self.width <= 9
    """
    _pieces: dict[tuple[int, int], Piece]
    player_moves: dict[str, list[Piece]]
    width: int

    def __init__(self, width: int) -> None:
        """Initialize this board with the dimensions of width by width.

        Preconditions:
            - 5 <= width <= 9
        """
        for i in range(width):
            for j in range(width):
                self._pieces[(i, j)] = Piece((i, j))
        self.width = width

    def _copy(self) -> Board:
        """Return a copy of this game state."""
        new_game = Board(self.width)
        new_game._pieces = self._pieces
        new_game.player_moves = self.player_moves
        return new_game

    def first_player_turn(self) -> bool:
        """Return whether it is the first player turn."""
        if len(self.player_moves['P1']) == len(self.player_moves['P2']):
            return True
        else:
            return False

    def possible_moves(self) -> set[Piece]:
        """Returns a set of possible moves as vertices"""
        possible_moves = set()
        for j in range(self.width):
            i = 0
            while self._pieces[(i, j)].player is not None and i < self.width:
                i += 1
            if self._pieces[(i, j)].player is None:
                possible_moves.add(self._pieces[(i, j)])
        return possible_moves

    def get_all_paths(self, direction: str, player: str) -> list[set[Piece]]:
        pieces = self.player_moves[player]
        all_paths = []
        for piece in pieces:
            path = set()
            path.add(piece)
            for connection in piece.connections[direction]:
                next_piece = connection.get_other_endpoint(piece)
                path.add(next_piece)
                for connection1 in next_piece.connections[direction]:
                    next_next_piece = connection1.get_other_endpoint(piece)
                    path.add(next_next_piece)
            all_paths.append(path)
        return all_paths



        # aabha
    def get_winner(self) -> Optional[str]:
        """Returns corresponding player if one of the two have 3 connections
        (4 piecs) in the same direction.
        """

        #Aabha
    def add_connection(self, n1: Piece, n2: Piece, connection_type: str) -> bool:
        """Given two Pieces adds an edge between two pieces given the specific type (direction)
        of their connection. Returns whether the connecton was added successfully.

         Preconditions:
            - n1.player is not None and n2.player is not None
            - n1.player == n2.player
            - n1 and n2 make a valid connection on the board
         """
        connection = Connection(n1, n2, connection_type)
        if connection in n1.connections[connection_type]:
            return False
        else:
            n1.connections[connection_type].append(connection)
            n2.connections[connection_type].append(connection)
            return True

        #ALI
    def get_connection_direction(self, n1: Piece, n2: Piece) -> str:
        """Returns direction of connection between the two pieces.
        raises a ValueError if there is not an existing connection between the pieces.
        """
        # TODO: figure out when this is used?
        location1 = n1.location
        location2 = n2.location

        # ALI
    def make_move(self, move: Piece, player: str) -> None:
        """Assigns Piece to player and adds it to the board’s corresponding
        player moves attribute. Also updates any connections this move may make.

        Preconditions:
            - move.player is None
            - move.location is a valid position to drop a piece (not a floating piece)
        """
        move.update_piece(player)

        self.moves.append(move)
        if self.player_moves[player]:
            self.player_moves[player].append(move)
        else:
            self.player_moves[player] = [move]

        x_pos = move.location[0]
        y_pos = move.location[1]
        for piece in self.player_moves[player]:
            if piece.location in {(x_pos + 1, y_pos + 1), (x_pos - 1, y_pos - 1)}:
                self.add_connection(move, piece, 'right-diagonal')
            elif piece.location in {(x_pos + 1, y_pos), (x_pos - 1, y_pos)}:
                self.add_connection(move, piece, 'vertical')
            elif piece.location in {(x_pos, y_pos + 1), (x_pos, y_pos - 1)}:
                self.add_connection(move, piece, 'horizontal')
            elif piece.location in {(x_pos + 1, y_pos - 1), (x_pos - 1, y_pos + 1)}:
                self.add_connection(move, piece, 'left-diagonal')

    def copy_and_record_move(self, move: Piece, player: str) -> Board:
        """Return a copy of this game state with the given status recorded.

        Preconditions:
        - not self.is_guesser_turn()
        - len(status) == self.word_size
        - _is_valid_status(status)
        """
        new_game = self._copy()
        new_game.make_move(move, player)
        return new_game


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
