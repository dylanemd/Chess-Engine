import pygame
from config import SQUARE, WIDTH, HEIGHT, LIGHT_SQUARE, DARK_SQUARE

PROMOTION_CHOICES = ["Queen", "Rook", "Bishop", "Knight"]


def draw_board(screen):
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                color = LIGHT_SQUARE
            else:
                color = DARK_SQUARE
            pygame.draw.rect(screen, color, (col * SQUARE, row * SQUARE, SQUARE, SQUARE))


def draw_pieces(screen, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece is not None:
                screen.blit(piece.image, (col * SQUARE, row * SQUARE))


def highlight_moves(screen, moves):
    dot_color = (30, 30, 30)
    for x, y in moves:
        center = (x * SQUARE + SQUARE // 2, y * SQUARE + SQUARE // 2)
        pygame.draw.circle(screen, dot_color, center, SQUARE // 8)


def draw_promotion_prompt(screen, color, images):
    box_width = SQUARE * len(PROMOTION_CHOICES)
    start_x = (WIDTH - box_width) // 2
    y = (HEIGHT - SQUARE) // 2

    pygame.draw.rect(screen, (50, 50, 50), (start_x, y, box_width, SQUARE))

    rects = []
    for i, piece_type in enumerate(PROMOTION_CHOICES):
        rect = pygame.Rect(start_x + i * SQUARE, y, SQUARE, SQUARE)
        pygame.draw.rect(screen, (220, 220, 220), rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        image = images.get((color, piece_type))
        if image:
            screen.blit(image, rect.topleft)
        rects.append((rect, piece_type))

    return rects