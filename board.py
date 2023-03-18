"""CSC111 Winter 2023 Final Project: Feelin Connected

File Information
===============================
This file contains the data classes that will compose the graph used to create the Connect 4 game.

This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""

from __future__ import annotations
from typing import Optional
from python_ta.contracts import check_contracts


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
        - self.player in {'P1', 'P2', None}
        - all(point >= 0 for point in self.location)
        - all(self in conn.endpoints for conn in self.connections)
    """
    player: Optional[str]
    location: tuple[int, int]
    connections: set[Connection]


@check_contracts
class Connection:
    """A link (or "edge") connecting two pieces on a Connect 4 board.

    Instance Attributes:
        - type: The direction (type) of connection two pices make.
        - endpoints: The two pieces that are linked by this connection.

    Representation Invariants:
        - len(self.endpoints) == 2
        - self.type in {'vertical', 'horizontal', 'left-diagonal', 'right-diagonal'}
    """
    type: str
    endpoints: set[Piece]


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
    """
    moves: set[Piece]
    player_moves: dict[str, set[Piece]]

    def __init__(self, width: int) -> None:
        """Initialize this board with the dimensions of width by width.

        Preconditions:
            - k >= 5
        """
