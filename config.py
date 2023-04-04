import chess

PIECES_WEIGHTS = {
    chess.PAWN: 1,
    chess.BISHOP: 3,
    chess.KNIGHT: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
}

RESULT_WEIGHTS = {
    "WIN": 1000,
    "LOSS": -1000,
    "TIE": 0,
}