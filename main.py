import chess
from mpi4py import MPI
from time import time

from moves import make_greedy_move, make_random_move, make_minimax_move

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    board = chess.Board()

    while not board.is_game_over():
        if board.turn:
            # Human makes move.
            if rank == 0:
                print("Current Number of Moves:", board.fullmove_number)
                print("Current Board:")
                print(board)

                move = make_random_move(board)
                board.push(move)
        else:
            # Minimax makes move.
            move = make_minimax_move(board, 5)
            if rank == 0:
                board.push(move)
        
        # used to sync the processes
        board = comm.bcast(board, 0)

    if rank == 0:
        if board.is_insufficient_material():
            print("Draw due to insufficient material.")
        elif board.is_fivefold_repetition():
            print("Draw due to five-fold repitition.")
        elif board.is_seventyfive_moves():
            print("Draw due to seventy-five moves.")
        elif board.is_stalemate():
            print("Stalemate.")
        elif board.is_checkmate():
            if board.turn:
                print("Black Won.")
            else:
                print("White Won.")
        
        print(board.result())


if __name__ == "__main__":
    main()