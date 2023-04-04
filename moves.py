import chess
import random
from math import inf

from config import *

def get_score(board: chess.Board, player: bool):
    if board.is_stalemate() or board.is_fivefold_repetition or board.is_insufficient_material() or board.is_seventyfive_moves():
        return RESULT_WEIGHTS["TIE"]
    elif board.is_checkmate() and board.turn == (not player):
        return RESULT_WEIGHTS["WIN"]
    elif board.is_checkmate() and board.turn == player:
        return RESULT_WEIGHTS["LOSS"]
    else:
        total = 0
        for piece, weight in PIECES_WEIGHTS:
            pos_cnt = str(board.pieces(piece, player)).count('1')
            neg_cnt = str(board.pieces(piece, not player)).count('1')

            total += (pos_cnt - neg_cnt) * weight

        return total
    

def make_random_move(board: chess.Board):
    legal_moves = list(board.legal_moves)
    random_move = random.choice(legal_moves)
    board.push(random_move)

def make_greedy_move(board: chess.Board, player: bool):
    legal_moves = list(board.legal_moves)

    best_score = -1
    best_move = legal_moves[0]

    for move in legal_moves:
        tmp_board = board.copy()
        tmp_board.push(move)
        tmp_score = get_score(board, player)
        if not player:
            tmp_score *= -1

        if tmp_score > best_score:
            best_score = tmp_score
            best_move = move
    
    board.push(best_move)

def make_minimax_move(board: chess.Board, player: bool):

    def minimax(board: chess.Board, player: bool, depth: int, alpha: float=-inf, beta: float=+inf):
        if depth == 0 or board.is_game_over():
            return get_score(board, player), None
        
        if player:
            # maximizing player
            max_score, best_move = -inf, None
            for move in board.legal_moves:
                new_board = board.copy()
                new_board.push(move)
                score, _ = minimax(new_board, not player, depth - 1, alpha, beta)

                alpha = max(alpha, score)
                if beta <= alpha:
                    break

                if score > max_score:
                    max_score, best_move = score, move
            return max_score, best_move
        else:
            # minimizing player
            min_score, best_move = +inf, None
            for move in board.legal_moves:
                new_board = board.copy()
                new_board.push(move)
                score, _ = minimax(new_board, player, depth - 1, alpha, beta)

                beta = min(beta, score)
                if beta <= alpha:
                    break

                if score < min_score:
                    min_score, best_move = score, move
            return min_score, best_move

    _, best_move = minimax(board, player, 3)
    board.push(best_move)
    

def make_human_move(board: chess.Board):
    human_move_str = input("What move do you want to make? ")
    while chess.Move.from_uci(human_move_str) not in board.legal_moves:
        human_move_str = input("Illegal Move! What move do you want to make? ")
    board.push_uci(human_move_str)