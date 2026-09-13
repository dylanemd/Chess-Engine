import copy
import rules
from pieces import Queen

PIECE_VALUES = {
    "Pawn": 100, "Knight": 320, "Bishop": 330,
    "Rook": 500, "Queen": 900, "King": 20000,
}


# Positive Score favors White
# Negative Score favors Black
def evaluate(board):
    score = 0
    for row in board:
        for piece in row:
            if piece is None:
                continue
            value = PIECE_VALUES[piece.type]
            if piece.color == "White":
                score += value
            else:
                score -= value
    return score


def get_all_pieces(board, color):
    pieces = []
    for row in board:
        for square in row:
            if square is not None and square.color == color:
                pieces.append(square)
    return pieces


def apply_move(board, piece, move, en_passant_target):
    x, y = piece.position
    new_x, new_y = move

    # Castling
    if piece.type == "King" and abs(new_x - x) == 2:
        row = y
        if new_x == 6:
            rook = board[row][7]
            board[row][7] = None
            board[row][5] = rook
            rook.position = (5, row)
            rook.has_moved = True
        elif new_x == 2:
            rook = board[row][0]
            board[row][0] = None
            board[row][3] = rook
            rook.position = (3, row)
            rook.has_moved = True

    # En passant capture
    if piece.type == "Pawn" and move == en_passant_target and board[new_y][new_x] is None:
        board[y][new_x] = None

    board[y][x] = None
    board[new_y][new_x] = piece
    piece.position = (new_x, new_y)
    piece.has_moved = True

    # Always auto-promotes to Queen
    if piece.type == "Pawn" and (new_y == 0 or new_y == 7):
        board[new_y][new_x] = Queen(piece.color, "Queen", (new_x, new_y), True, piece.image)

    if piece.type == "Pawn" and abs(new_y - y) == 2:
        return (x, (y + new_y) // 2)
    return None


def minimax(board, depth, alpha, beta, maximizing, en_passant_target):
    if maximizing:
        color = "White"
    else:
        color = "Black"

    if depth == 0:
        return evaluate(board), None

    best_move = None
    if maximizing:
        best_score = float("-inf")
    else:
        best_score = float("inf")

    any_legal_move = False

    for piece in get_all_pieces(board, color):
        for move in rules.get_legal_moves(piece, board, en_passant_target):
            any_legal_move = True

            board_copy = copy.deepcopy(board)
            piece_copy = board_copy[piece.position[1]][piece.position[0]]
            new_ep = apply_move(board_copy, piece_copy, move, en_passant_target)

            score, _ = minimax(board_copy, depth - 1, alpha, beta, not maximizing, new_ep)

            if maximizing:
                if score > best_score:
                    best_score, best_move = score, (piece, move)
                alpha = max(alpha, best_score)
            else:
                if score < best_score:
                    best_score, best_move = score, (piece, move)
                beta = min(beta, best_score)

            if beta <= alpha:
                break
        if beta <= alpha:
            break

    if not any_legal_move:
        if rules.is_check(board, color):
            # Checkmate: bad for whoever is stuck. The depth bonus makes a
            # faster mate score better than a slower one.
            if maximizing:
                return -999999 - depth, None
            else:
                return 999999 + depth, None
        return 0, None  # stalemate

    return best_score, best_move


def choose_move(board, color, en_passant_target, depth=2):
    if color == "White":
        maximizing = True
    else:
        maximizing = False
    _ , best_move = minimax(board, depth, float("-inf"), float("inf"), maximizing, en_passant_target)
    return best_move