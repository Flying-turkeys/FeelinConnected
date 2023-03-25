"""CSC111 Winter 2023 Final Project: Feelin Connected

File Information
===============================
This file contains the data classes that will compose the graph used to create the Connect 4 game.

This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""

from __future__ import annotations
from typing import Optional
from python_ta.contracts import check_contracts
from players import AbstractPlayer as Player


@check_contracts
class Piece:
    """A node that represents a piece in a Connect 4 board.

    Instance Attributes
        - player:
            The player who this piece belongs to. Can be None if no player has
            made a move in the location of the piece.
        - location:
            The address (i.e., unique identifier) of this node.
        - connections:
            A list containing the connections for this piece.

    Representation Invariants:
        - all(point >= 0 for point in self.location)
        - all(self in conn.endpoints for conn in self.connections)
    """
    player: Optional[Player]
    location: tuple[int, int]
    # should connections be a dictionary mapping either the address or the type of connection to connection?
    connections: set[Connection]

    def __init__(self, location: tuple[int, int]) -> None:
        """Initialize this piece with the given location and no connections to other pieces."""
        self.player = None
        self.location = location
        self.connections = set()

    def __repr__(self) -> str:
        """Return a string representing this piece.

        >>> piece = Piece((0, 0))
        >>> piece
        Piece(0, 0)
        """
        return f'Piece{self.location}'


@check_contracts
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
        location1 = n1.location
        location2 = n2.location
        if location2 in {(location1[0] + 1, location1[0] + 1), (location1[0] - 1, location1[0] - 1)}:
            self.type = 'right-diagonal'
            self.endpoints = {n1, n2}
        elif location2 in {(location1[0] + 1, location1[0]), (location1[0] - 1, location1[0])}:
            self.type = 'vertical'
            self.endpoints = {n1, n2}
        elif location2 in {(location1[0], location1[0] + 1), (location1[0], location1[0] - 1)}:
            self.type = 'horizontal'
            self.endpoints = {n1, n2}
        elif location2 in {(location1[0] + 1, location1[0] - 1), (location1[0] - 1, location1[0] + 1)}:
            self.type = 'left-diagonal'
            self.endpoints = {n1, n2}
        else:
            raise ValueError







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


@check_contracts
class Board:
    """A graph that represents a Connect 4 board and holds all empty and non-empty spaces/pieces.

    Instance Attributes:
        - type: The direction (type) of connection two pices make.
        - endpoints: The two pieces that are linked by this connection.

    Representation Invariants:
        - len(self.player_moves) == 2
        - all(type in {'P1', 'P2'} for type in self.player_moves)
        - all(isinstance(moves, int) for address in self._nodes)
        - 5 <= self.width <= 9
    """
    moves: set[Piece]
    player_moves: dict[str, set[Piece]]
    width: int

    def __init__(self, width: int) -> None:
        """Initialize this board with the dimensions of width by width.

        Preconditions:
            - 5 <= width <= 9
        """

    def _copy(self) -> Board:
        """Return a copy of this game state."""
        new_game = Board(self.width)
        new_game.moves = self.moves
        new_game.player_moves = self.player_moves
        return new_game

    def first_player_turn(self) -> bool:
        """Return whether it is the first player turn."""

    def possible_moves(self) -> set[Piece]:
        """Returns a set of possible moves as vertices"""

    def get_winner(self) -> Optional[Player]:
        """Returns corresponding player if one of the two have 3 connections
        (4 piecs) in the same direction.
        """

    def add_connection(self, n1: Piece, n2: Piece, connection_type: str) -> Connection:
        """Given two Pieces adds an edge between two pieces given the specific type (direction)
        of their connection. Returns the new connection.
        # TODO: Maybe we don't need to return connection but added it any way just in case (can change later)

         Preconditions:
            - n1.player is not None and n2.player is not None
            - n1.player == n2.player
            - n1 and n2 make a valid connection on the board
         """
    def get_connection_direction(self, n1: Piece, n2: Piece) -> str:
        """Returns direction of connection between the two pieces"""

    def make_move(self, move: Piece, player: Player) -> None:
        """Assigns Piece to player and adds it to the board’s corresponding
        player moves attribute. Also updates any connections this move may make.

        Preconditions:
            - move.player is None
            - move.location is a valid position to drop a piece (not a floating piece)
        """

    def copy_and_record_move(self, move: Piece, player: Player) -> Board:
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
