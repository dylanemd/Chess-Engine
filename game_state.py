from pieces import Rook, Knight, Bishop, Queen, King, Pawn
import rules
 
 
def create_empty_board():
    board = []
    for _ in range(8):
        row = []
        for _ in range(8):
            row.append(None)
        board.append(row)
    return board
 
 
class GameState:
    BACK_RANK = [
        (Rook, "Rook", 0), (Knight, "Knight", 1), (Bishop, "Bishop", 2),
        (Queen, "Queen", 3), (King, "King", 4),
        (Bishop, "Bishop", 5), (Knight, "Knight", 6), (Rook, "Rook", 7),
    ]
 
    def __init__(self, images=None):
        if images is None:
            self.images = {}
        else:
            self.images = images
        self.board = create_empty_board()
        self.white_pieces = []
        self.black_pieces = []
        self.turn = "White"
        self.en_passant_target = None
        self._setup_pieces()
 
    def _image_for(self, color, piece_type):
        return self.images.get((color, piece_type))
 
    def _setup_pieces(self):
        for i in range(8):
            white_pawn = Pawn("White", "Pawn", (i, 6), False, self._image_for("White", "Pawn"))
            self.board[6][i] = white_pawn
            self.white_pieces.append(white_pawn)
 
            black_pawn = Pawn("Black", "Pawn", (i, 1), False, self._image_for("Black", "Pawn"))
            self.board[1][i] = black_pawn
            self.black_pieces.append(black_pawn)
 
        for cls, name, col in self.BACK_RANK:
            white_piece = cls("White", name, (col, 7), False, self._image_for("White", name))
            self.board[7][col] = white_piece
            self.white_pieces.append(white_piece)
 
            black_piece = cls("Black", name, (col, 0), False, self._image_for("Black", name))
            self.board[0][col] = black_piece
            self.black_pieces.append(black_piece)
 
    # --- rules delegation -------------------------------------------------
 
    def get_legal_moves(self, piece):
        return rules.get_legal_moves(piece, self.board, self.en_passant_target)
 
    def is_check(self, color):
        return rules.is_check(self.board, color)
 
    def is_checkmate(self, color):
        if color == "White":
            pieces_list = self.white_pieces
        else:
            pieces_list = self.black_pieces
        return rules.is_checkmate(self.board, color, pieces_list, self.en_passant_target)
 
    def is_stalemate(self, color):
        if color == "White":
            pieces_list = self.white_pieces
        else:
            pieces_list = self.black_pieces
        return rules.is_stalemate(self.board, color, pieces_list, self.en_passant_target)
 
    # --- mutation -----------------------------------------------------------
 
    def move_piece(self, piece, new_position):
        x, y = piece.position
        new_x, new_y = new_position
 
        # Castling: king moves two squares horizontally - bring the rook along
        if piece.type == "King" and abs(new_x - x) == 2:
            row = y
            if new_x == 6:  # kingside
                rook = self.board[row][7]
                self.board[row][7] = None
                self.board[row][5] = rook
                rook.position = (5, row)
                rook.has_moved = True
            elif new_x == 2:  # queenside
                rook = self.board[row][0]
                self.board[row][0] = None
                self.board[row][3] = rook
                rook.position = (3, row)
                rook.has_moved = True
 
        # En passant: destination square is empty, captured pawn sits beside us
        if piece.type == "Pawn" and new_position == self.en_passant_target and self.board[new_y][new_x] is None:
            captured = self.board[y][new_x]
            if captured is not None:
                self._remove_piece(captured)
                self.board[y][new_x] = None
 
        # Normal capture
        if self.board[new_y][new_x] is not None:
            self._remove_piece(self.board[new_y][new_x])
 
        self.board[y][x] = None
        self.board[new_y][new_x] = piece
        piece.position = (new_x, new_y)
        piece.has_moved = True
 
        if piece.type == "Pawn" and abs(new_y - y) == 2:
            self.en_passant_target = (x, (y + new_y) // 2)
        else:
            self.en_passant_target = None
 
        if self.turn == "White":
            self.turn = "Black"
        else:
            self.turn = "White"
 
    def _remove_piece(self, piece):
        if piece.color == "White":
            self.white_pieces.remove(piece)
        else:
            self.black_pieces.remove(piece)
 
    # --- promotion -----------------------------------------------------
 
    PROMOTION_CLASSES = {"Queen": Queen, "Rook": Rook, "Bishop": Bishop, "Knight": Knight}
 
    def needs_promotion(self, piece):
        if piece.type != "Pawn":
            return False
        _, y = piece.position
        return y == 0 or y == 7
 
    def promote_pawn(self, pawn, new_type):
        x, y = pawn.position
        cls = self.PROMOTION_CLASSES[new_type]
        new_piece = cls(pawn.color, new_type, (x, y), True, self._image_for(pawn.color, new_type))
        self.board[y][x] = new_piece
 
        if pawn.color == "White":
            pieces_list = self.white_pieces
        else:
            pieces_list = self.black_pieces
        pieces_list[pieces_list.index(pawn)] = new_piece
        return new_piece