from util import *

# stupid class to represent a piece
class Piece:
    # number of pieces instantiated for each player
    num_pieces = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0
    }

    def __init__(self, player_id):
        self.player_id = player_id
        self.piece_id = Piece.num_pieces[self.player_id]
        self.color = COLOR_MAP[player_id]
        Piece.num_pieces[self.player_id] += 1

    def __repr__(self):
        return f"Piece(player_id={self.player_id}, piece_id={self.piece_id})"
        
