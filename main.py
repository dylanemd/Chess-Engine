import copy
from concurrent.futures import ThreadPoolExecutor
from threading import Event

import pygame
from config import WIDTH, HEIGHT, SQUARE
from assets import load_images
from game_state import GameState
from renderer import draw_board, draw_pieces, highlight_moves, draw_promotion_prompt
import engine

HUMAN_COLOR = "White"
COMPUTER_COLOR = "Black"
ENGINE_DEPTH = 3

if HUMAN_COLOR not in ("White", "Black") or COMPUTER_COLOR not in ("White", "Black"):
    raise ValueError("Player colors must be White or Black")
if HUMAN_COLOR == COMPUTER_COLOR:
    raise ValueError("The human and computer must play different colors")
if ENGINE_DEPTH < 1:
    raise ValueError("Search depth must be at least 1")

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

images = load_images()
state = GameState(images)

selected_piece = None
valid_moves = []
awaiting_promotion = None
running = True
search_pool = ThreadPoolExecutor(max_workers=1)
search_future = None
cancel_search = Event()


def check_game_over(color):
    global running
    if state.is_checkmate(color):
        if color == "White":
            winner = "Black"
        else:
            winner = "White"
        print(f"Checkmate! {winner} wins")
        running = False
        return True
    if state.is_stalemate(color):
        print("Stalemate - draw")
        running = False
        return True
    return False


def computer_turn():
    global search_future
    if search_future is None:
        # Search a copy so the game board stays on the main thread.
        board_copy = copy.deepcopy(state.board)
        search_future = search_pool.submit(
            engine.choose_move, board_copy, COMPUTER_COLOR,
            state.en_passant_target, ENGINE_DEPTH, cancel_search
        )
        return

    if not search_future.done():
        return

    result = search_future.result()
    search_future = None
    if result is None:
        check_game_over(state.turn)
        return
    searched_piece, move = result
    x, y = searched_piece.position
    piece = state.board[y][x]
    state.move_piece(piece, move)
    if state.needs_promotion(piece):
        state.promote_pawn(piece, "Queen")  # computer always promotes to queen
    check_game_over(state.turn)


try:
    while running:
        draw_board(screen)
        draw_pieces(screen, state.board)
        if selected_piece is not None and awaiting_promotion is None:
            highlight_moves(screen, valid_moves)

        promotion_rects = []
        if awaiting_promotion is not None:
            promotion_rects = draw_promotion_prompt(screen, awaiting_promotion.color, images)

        for event in pygame.event.get():
            if not running:
                break
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN and (awaiting_promotion is not None or state.turn == HUMAN_COLOR):
                mouse_pos = event.pos

                if awaiting_promotion is not None:
                    for rect, piece_type in promotion_rects:
                        if rect.collidepoint(mouse_pos):
                            state.promote_pawn(awaiting_promotion, piece_type)
                            awaiting_promotion = None
                            check_game_over(state.turn)
                            break
                    continue

                x, y = mouse_pos[0] // SQUARE, mouse_pos[1] // SQUARE
                if not (0 <= x < 8 and 0 <= y < 8):
                    continue

                if selected_piece is None:
                    piece = state.board[y][x]
                    if piece is not None and piece.color == state.turn:
                        selected_piece = piece
                        valid_moves = state.get_legal_moves(piece)
                else:
                    if (x, y) in valid_moves:
                        moved_piece = selected_piece
                        state.move_piece(moved_piece, (x, y))
                        selected_piece = None
                        valid_moves = []

                        if state.needs_promotion(moved_piece):
                            awaiting_promotion = moved_piece
                        else:
                            check_game_over(state.turn)
                    else:
                        selected_piece = None
                        valid_moves = []

        if not running:
            break

        pygame.display.update()
        if awaiting_promotion is None and state.turn == COMPUTER_COLOR:
            computer_turn()
        clock.tick(60)
finally:
    cancel_search.set()
    search_pool.shutdown(wait=True, cancel_futures=True)
    pygame.quit()

        





        
    