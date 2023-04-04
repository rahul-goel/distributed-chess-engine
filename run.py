import chess
import random

def get_score(board: chess.Board, player: bool):
    cnts = []
    for piece_id in range(1, 7):
        cnts.append(str(board.pieces(piece_id, player)).count('1'))
    return cnts[0] + cnts[1] * 3 + cnts[2] * 3 + cnts[3] * 5 + cnts[4] * 9

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
        tmp_score = get_score(board, player) - get_score(board, ~player)

        if tmp_score > best_score:
            best_score = tmp_score
            best_move = move
    
    board.push(best_move)

def make_human_move(board: chess.Board):
    human_move_str = input("What move do you want to make? ")
    while chess.Move.from_uci(human_move_str) not in board.legal_moves:
        human_move_str = input("Illegal Move! What move do you want to make? ")
    board.push_uci(human_move_str)

def main():
    board = chess.Board()

    while not board.is_game_over():
        # print("Current Number of Moves:", board.fullmove_number)
        # print(board)
        if board.turn:
            make_random_move(board)
        else:
            make_greedy_move(board, board.turn)
    
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