#This is a method ot determine the legal moves when given an array of possible moves
import chess

#instantiates a chessboard
board = chess.Board()

def checkLegalMoves(possibleMoves):
    for h in range(0, len(possibleMoves)):
        for q in range(0, len(possibleMoves)):
            if(h != q):
                move = str(possibleMoves[h]) + str(possibleMoves[q])
                if(chess.Move.from_uci(str(move)) in board.legal_moves):
                    return move

moves = ['e2', 'e1', 'c4', 'g1', 'f3']
checkLegalMoves(moves)
