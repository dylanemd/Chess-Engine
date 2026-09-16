import copy
from threading import Event
import unittest

import engine
from game_state import GameState, create_empty_board
import pieces
import rules


def square(name):
    return ord(name[0]) - ord("a"), 8 - int(name[1])


def make_position(entries, turn="White"):
    state = GameState()
    state.board = create_empty_board()
    state.white_pieces = []
    state.black_pieces = []
    state.turn = turn
    for color, kind, name, moved in entries:
        x, y = square(name)
        piece = getattr(pieces, kind)(color, kind, (x, y), moved, None)
        state.board[y][x] = piece
        if color == "White":
            state.white_pieces.append(piece)
        else:
            state.black_pieces.append(piece)
    return state


def piece_at(state, name):
    x, y = square(name)
    return state.board[y][x]


def play(state, start, end):
    piece = piece_at(state, start)
    if piece.color != state.turn or square(end) not in state.get_legal_moves(piece):
        raise AssertionError(f"Illegal test move: {start} to {end}")
    state.move_piece(piece, square(end))
    return piece


class ChessTests(unittest.TestCase):
    def test_starting_moves(self):
        state = GameState()
        self.assertEqual(sum(len(state.get_legal_moves(p)) for p in state.white_pieces), 20)

    def test_pawn_moves_and_attacks_are_different(self):
        state = make_position([
            ("White", "King", "e2", True),
            ("Black", "King", "h8", True),
            ("Black", "Pawn", "e4", True),
        ])
        pawn = piece_at(state, "e4")
        self.assertIn(square("e3"), pawn.possibleMoves(state.board))
        self.assertFalse(rules.is_square_attacked(state.board, *square("e3"), "Black"))
        self.assertTrue(rules.is_square_attacked(state.board, *square("d3"), "Black"))
        moves = state.get_legal_moves(piece_at(state, "e2"))
        self.assertIn(square("e3"), moves)
        self.assertNotIn(square("d3"), moves)

    def test_castling_avoids_pawn_attacks(self):
        for color, rank, pawn_rank, other_rank in [("White", "1", "2", "8"), ("Black", "8", "7", "1")]:
            enemy = "Black" if color == "White" else "White"
            for rook_file, pawn_file, destination in [("h", "e", "g"), ("a", "b", "c")]:
                with self.subTest(color=color, destination=destination):
                    state = make_position([
                        (color, "King", "e" + rank, False),
                        (color, "Rook", rook_file + rank, False),
                        (enemy, "King", "h" + other_rank, True),
                        (enemy, "Pawn", pawn_file + pawn_rank, True),
                    ], color)
                    self.assertNotIn(square(destination + rank), state.get_legal_moves(piece_at(state, "e" + rank)))

    def test_safe_castling_moves_both_pieces(self):
        for color, rank, other_rank in [("White", "1", "8"), ("Black", "8", "1")]:
            enemy = "Black" if color == "White" else "White"
            for rook_file, destination, rook_end in [("h", "g", "f"), ("a", "c", "d")]:
                with self.subTest(color=color, destination=destination):
                    state = make_position([
                        (color, "King", "e" + rank, False),
                        (color, "Rook", rook_file + rank, False),
                        (enemy, "King", "e" + other_rank, True),
                    ], color)
                    rook = piece_at(state, rook_file + rank)
                    king = play(state, "e" + rank, destination + rank)
                    self.assertIs(piece_at(state, rook_end + rank), rook)
                    self.assertTrue(king.has_moved and rook.has_moved)
                    self.assertIsNone(piece_at(state, rook_file + rank))

    def test_castling_rights_are_lost_after_moving(self):
        state = make_position([
            ("White", "King", "e1", False),
            ("White", "Rook", "h1", True),
            ("Black", "King", "e8", True),
        ])
        self.assertNotIn(square("g1"), state.get_legal_moves(piece_at(state, "e1")))
        piece_at(state, "h1").has_moved = False
        piece_at(state, "e1").has_moved = True
        self.assertNotIn(square("g1"), state.get_legal_moves(piece_at(state, "e1")))

    def test_king_is_not_a_capture_target(self):
        state = make_position([
            ("White", "King", "a1", True),
            ("White", "Rook", "h1", True),
            ("Black", "King", "h8", True),
        ], "Black")
        self.assertTrue(state.is_check("Black"))
        self.assertNotIn(square("h8"), state.get_legal_moves(piece_at(state, "h1")))

    def test_en_passant_capture(self):
        state = GameState()
        for start, end in [("e2", "e4"), ("a7", "a6"), ("e4", "e5"), ("d7", "d5")]:
            play(state, start, end)
        play(state, "e5", "d6")
        self.assertIsNone(piece_at(state, "d5"))
        self.assertEqual(piece_at(state, "d6").color, "White")
        self.assertEqual(len(state.black_pieces), 15)

    def test_en_passant_expires(self):
        state = GameState()
        for start, end in [("e2", "e4"), ("a7", "a6"), ("e4", "e5"), ("d7", "d5"), ("a2", "a3"), ("a6", "a5")]:
            play(state, start, end)
        self.assertNotIn(square("d6"), state.get_legal_moves(piece_at(state, "e5")))

    def test_en_passant_cannot_expose_king(self):
        state = make_position([
            ("White", "King", "e1", True),
            ("White", "Pawn", "e5", True),
            ("Black", "King", "a8", True),
            ("Black", "Rook", "e8", True),
            ("Black", "Pawn", "d5", True),
        ])
        state.en_passant_target = square("d6")
        self.assertNotIn(square("d6"), state.get_legal_moves(piece_at(state, "e5")))

    def test_promotion_choices(self):
        for color, start, end in [("White", "a7", "a8"), ("Black", "a2", "a1")]:
            for kind in ["Queen", "Rook", "Bishop", "Knight"]:
                with self.subTest(color=color, kind=kind):
                    state = make_position([
                        ("White", "King", "h1", True),
                        ("Black", "King", "h8", True),
                        (color, "Pawn", start, True),
                    ], color)
                    pawn = play(state, start, end)
                    self.assertTrue(state.needs_promotion(pawn))
                    promoted = state.promote_pawn(pawn, kind)
                    self.assertIs(piece_at(state, end), promoted)
                    self.assertEqual(promoted.type, kind)
                    self.assertNotIn(pawn, state.white_pieces + state.black_pieces)

    def test_checkmate(self):
        state = GameState()
        for start, end in [("f2", "f3"), ("e7", "e5"), ("g2", "g4"), ("d8", "h4")]:
            play(state, start, end)
        self.assertTrue(state.is_checkmate("White"))

    def test_terminal_scores_at_depth_zero(self):
        for winner, loser, king, queen, trapped in [
            ("White", "Black", "f6", "g7", "h8"),
            ("Black", "White", "f3", "g2", "h1"),
        ]:
            with self.subTest(winner=winner):
                state = make_position([
                    (winner, "King", king, True),
                    (winner, "Queen", queen, True),
                    (loser, "King", trapped, True),
                ], loser)
                self.assertTrue(state.is_checkmate(loser))
                score, _ = engine.minimax(state.board, 0, float("-inf"), float("inf"), loser == "White", None)
                self.assertEqual(score, 999999 if winner == "White" else -999999)

        state = make_position([
            ("White", "King", "f7", True),
            ("White", "Queen", "g6", True),
            ("Black", "King", "h8", True),
        ], "Black")
        self.assertTrue(state.is_stalemate("Black"))
        score, _ = engine.minimax(state.board, 0, float("-inf"), float("inf"), False, None)
        self.assertEqual(score, 0)

    def test_search_finds_mate_in_one(self):
        state = make_position([
            ("White", "King", "f6", True),
            ("White", "Queen", "g6", True),
            ("Black", "King", "h8", True),
        ])
        piece, move = engine.choose_move(state.board, "White", None, 1)
        state.move_piece(piece, move)
        self.assertTrue(state.is_checkmate("Black"))

    def test_search_preserves_the_board(self):
        state = GameState()
        before = copy.deepcopy(state.board)
        piece, move = engine.choose_move(state.board, "White", None, 2)
        self.assertIn(move, state.get_legal_moves(piece))
        for old_row, new_row in zip(before, state.board):
            for old, new in zip(old_row, new_row):
                if old is None:
                    self.assertIsNone(new)
                else:
                    self.assertEqual(vars(old), vars(new))

    def test_search_can_be_cancelled(self):
        stop = Event()
        stop.set()
        with self.assertRaises(engine.SearchCancelled):
            engine.choose_move(GameState().board, "White", None, 3, stop)

    def test_search_depth_must_be_positive(self):
        with self.assertRaises(ValueError):
            engine.choose_move(GameState().board, "White", None, 0)


if __name__ == "__main__":
    unittest.main()
