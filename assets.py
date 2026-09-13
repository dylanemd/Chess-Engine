import pygame
from config import SQUARE
 
FILE_PREFIX = {"White": "w", "Black": "b"}
TYPE_CODE = {
    "Pawn": "p", "Rook": "r", "Knight": "n",
    "Bishop": "b", "Queen": "q", "King": "k",
}
 
 
def load_images():
    images = {}
    for color, prefix in FILE_PREFIX.items():
        for piece_type, code in TYPE_CODE.items():
            path = f"images/{prefix}{code}.png"
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.smoothscale(image, (SQUARE, SQUARE))
            images[(color, piece_type)] = image
    return images