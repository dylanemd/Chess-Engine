import pygame
from config import WIDTH, HEIGHT, SQUARE
from assets import load_images
from game_state import GameState
from renderer import draw_board, draw_pieces, highlight_moves, draw_promotion_prompt
import engine

HUMAN_COLOR = "White"
COMPUTER_COLOR = "Black"
ENGINE_DEPTH = 3 

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

images = load_images()
state = GameState(images)

selected_piece = None
valid_moves = []
awaiting_promotion = None  
running = True


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
    global awaiting_promotion
    result = engine.choose_move(state.board, COMPUTER_COLOR, state.en_passant_target, ENGINE_DEPTH)
    if result is None:
        return
    piece, move = result
    state.move_piece(piece, move)
    if state.needs_promotion(piece):
        state.promote_pawn(piece, "Queen")  # computer always promotes to queen
    check_game_over(state.turn)


while running:
    draw_board(screen)
    draw_pieces(screen, state.board)
    if selected_piece is not None and awaiting_promotion is None:
        highlight_moves(screen, valid_moves)

    promotion_rects = []
    if awaiting_promotion is not None:
        promotion_rects = draw_promotion_prompt(screen, awaiting_promotion.color, images)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and (awaiting_promotion is not None or state.turn == HUMAN_COLOR):
            mouse_pos = pygame.mouse.get_pos()

            if awaiting_promotion is not None:
                for rect, piece_type in promotion_rects:
                    if rect.collidepoint(mouse_pos):
                        state.promote_pawn(awaiting_promotion, piece_type)
                        awaiting_promotion = None
                        if not check_game_over(state.turn) and state.turn == COMPUTER_COLOR:
                            computer_turn()
                        break
                continue

            x, y = mouse_pos[0] // SQUARE, mouse_pos[1] // SQUARE

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
                    elif not check_game_over(state.turn) and state.turn == COMPUTER_COLOR:
                        computer_turn()
                else:
                    selected_piece = None
                    valid_moves = []

    pygame.display.update()

pygame.quit()

        





        
    