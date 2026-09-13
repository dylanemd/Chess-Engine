import copy


def is_square_attacked(board, x, y, by_color):
    for row in board:
        for piece in row:
            if piece is not None and piece.color == by_color:
                if (x, y) in piece.possibleMoves(board):
                    return True
    return False


def is_check(board, color):
    king_pos = None
    for row in board:
        for p in row:
            if p is not None and p.type == "King" and p.color == color:
                king_pos = p.position

    if color == "White":
        enemy_color = "Black"
    else:
        enemy_color = "White"
    return is_square_attacked(board, king_pos[0], king_pos[1], enemy_color)


def get_castling_moves(board, color):
    if color == "White":
        row = 7
    else:
        row = 0
    king = board[row][4]
    moves = []

    if king is None or king.type != "King" or king.has_moved:
        return moves
    if is_check(board, color):
        return moves

    if color == "White":
        enemy_color = "Black"
    else:
        enemy_color = "White"

    # Kingside 
    rook = board[row][7]
    if rook is not None and rook.type == "Rook" and not rook.has_moved:
        if board[row][5] is None and board[row][6] is None:
            if not is_square_attacked(board, 5, row, enemy_color) and \
               not is_square_attacked(board, 6, row, enemy_color):
                moves.append((6, row))

    # Queenside 
    rook = board[row][0]
    if rook is not None and rook.type == "Rook" and not rook.has_moved:
        if board[row][1] is None and board[row][2] is None and board[row][3] is None:
            if not is_square_attacked(board, 2, row, enemy_color) and \
               not is_square_attacked(board, 3, row, enemy_color):
                moves.append((2, row))

    return moves


def get_legal_moves(piece, board, en_passant_target=None):
    legal_moves = []
    possible_moves = piece.possibleMoves(board, en_passant_target)

    for move in possible_moves:
        board_copy = copy.deepcopy(board)
        piece_copy = board_copy[piece.position[1]][piece.position[0]]
        x, y = piece_copy.position
        new_x, new_y = move

        if piece.type == "Pawn" and move == en_passant_target and board_copy[new_y][new_x] is None:
            board_copy[y][new_x] = None

        board_copy[y][x] = None
        board_copy[new_y][new_x] = piece_copy
        piece_copy.position = (new_x, new_y)

        if not is_check(board_copy, piece.color):
            legal_moves.append(move)

    if piece.type == "King":
        legal_moves.extend(get_castling_moves(board, piece.color))

    return legal_moves


def has_legal_moves(board, pieces_list, en_passant_target=None):
    for piece in pieces_list:
        if len(get_legal_moves(piece, board, en_passant_target)) > 0:
            return True
    return False


def is_checkmate(board, color, pieces_list, en_passant_target=None):
    if not is_check(board, color):
        return False
    return not has_legal_moves(board, pieces_list, en_passant_target)


def is_stalemate(board, color, pieces_list, en_passant_target=None):
    if is_check(board, color):
        return False
    return not has_legal_moves(board, pieces_list, en_passant_target)
