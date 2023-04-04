import chess
import argparse

from moves import make_random_move, make_greedy_move, make_human_move, make_minimax_move

def main(args):
    board = chess.Board()

    while not board.is_game_over():
        print("Current Number of Moves:", board.fullmove_number)
        print(board)
        if board.turn:
            make_random_move(board)
        else:
            make_minimax_move(board, board.turn)
    
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

    parser = argparse.ArgumentParser(description="Distributed Chess Engine.")
    parser.add_argument("--white", default="minimax_ab", type=str, choices=["minimax", "minimax_ab", "greedy", "random", "human"])
    parser.add_argument("--black", default="minimax_ab", type=str, choices=["minimax", "minimax_ab", "greedy", "random", "human"])
    args = parser.parse_args()

    main(args)