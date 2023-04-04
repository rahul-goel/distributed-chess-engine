import chess
import random

def make_random_move(board: chess.Board):
    legal_moves = list(board.legal_moves)
    random_move = random.choice(legal_moves)
    board.push(random_move)

def make_human_move(board: chess.Board):
    human_move_str = input("What move do you want to make? ")
    while chess.Move.from_uci(human_move_str) not in board.legal_moves:
        human_move_str = input("Illegal Move! What move do you want to make? ")
    board.push_uci(human_move_str)

def main():
    board = chess.Board()

    while not board.is_game_over():
        print("Current Number of Moves:", board.fullmove_number)
        print(board)
        if board.turn:
            make_random_move(board)
        else:
            make_random_move(board)
        

if __name__ == "__main__":
    main()