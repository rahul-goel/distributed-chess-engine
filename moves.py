import chess
import random
from math import inf
from mpi4py import MPI

from config import *
from interface import *

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

def minimax(board: chess.Board, depth: int, alpha: float=-inf, beta: float=+inf):
    player = board.turn
    if depth == 0 or board.is_game_over():
        return get_score(board, player), None
    
    if player:
        # maximizing player
        max_score, best_move = -inf, None
        for move in board.legal_moves:
            new_board = board.copy()
            new_board.push(move)
            score, _ = minimax(new_board, depth - 1, alpha, beta)

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
            score, _ = minimax(new_board, depth - 1, alpha, beta)

            beta = min(beta, score)
            if beta <= alpha:
                break

            if score < min_score:
                min_score, best_move = score, move
        return min_score, best_move

def make_random_move(board: chess.Board):
    legal_moves = list(board.legal_moves)
    random_move = random.choice(legal_moves)
    return random_move

def make_greedy_move(board: chess.Board):
    player = board.turn
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
    
    return best_move

def make_parallel_minimax_move(board: chess.Board, depth: int=3):
    # get MPI info
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        # get all the possibe next game states
        legal_moves = list(board.legal_moves)
        boards_list = [board.copy().push(move) for move in legal_moves]
    else:
        boards_list = []
    
    my_boards = scatter_boards_among_processes(boards_list)

    my_moves = [random.choice(list(board.legal_moves)) for board in my_boards]
    my_scores = [random.randint(0, 10) for _ in range(len(moves_list))]

    moves_list = gather_moves_from_processes(my_moves, len(boards_list))
    scores_list = gather_moves_from_processes(my_scores, len(boards_list))

    # finally which move should i make?
    if rank == 0:
        best_score = -1
        best_move = legal_moves[0]

        for move, score in zip(legal_moves, scores_list):
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    else:
        return None

def make_minimax_move(board: chess.Board, depth: int=3):
    _, move = minimax(board, depth)
    return move
    

def make_human_move(board: chess.Board):
    human_move_str = input("What move do you want to make? ")
    while chess.Move.from_uci(human_move_str) not in board.legal_moves:
        human_move_str = input("Illegal Move! What move do you want to make? ")
    return chess.Move.from_uci(human_move_str)