# Python Chess

A chess game written in Python with Pygame. You play against a computer opponent that uses minimax search with alpha-beta pruning.

## Features

- Piece movement, captures, and legal move checking
- Check, checkmate, and stalemate detection
- Kingside and queenside castling, plus en passant
- Pawn promotion with a choice of queen, rook, bishop, or knight
- A computer opponent that scores positions using piece values
- Click-to-move controls with legal moves highlighted

## Requirements

- Python 3.9+
- [Pygame](https://www.pygame.org/)

Install Pygame:

```bash
pip install pygame
```

## Setup

Put your piece images in an `images/` folder next to `main.py`. The filenames use `w` for White, `b` for Black, and a letter for the piece (`n` is the knight):

```
images/
  wp.png  wn.png  wb.png  wr.png  wq.png  wk.png
  bp.png  bn.png  bb.png  br.png  bq.png  bk.png
```

Piece images are not included in this download. Add all twelve PNG files before running the game.

## Running the game

From the project folder, run:

```bash
python main.py
```

By default, you play White and the computer plays Black. Click one of your pieces to see its legal moves, then click a highlighted square to move. When a pawn promotes, click the piece you want in the promotion prompt.

The computer searches in the background, so the window still responds while it thinks. Checkmate and stalemate results are printed in the terminal, and the window closes when the game ends.

## Project structure

| File | Purpose |
|---|---|
| `main.py` | Game loop, event handling, and turn management |
| `config.py` | Board/window dimensions and color constants |
| `assets.py` | Loads and scales piece images |
| `pieces.py` | Piece classes (`Rook`, `Knight`, `Bishop`, `Queen`, `King`, `Pawn`) and their raw move generation |
| `rules.py` | Legal move filtering (accounting for check), castling rules, checkmate/stalemate detection |
| `game_state.py` | `GameState` class: board setup, move application, promotion, turn tracking |
| `renderer.py` | Drawing the board, pieces, move highlights, and promotion prompt |
| `engine.py` | Minimax search with alpha-beta pruning for the computer opponent |
| `test_chess.py` | Tests for move rules, special moves, and search results |

## Configuring the engine

In `main.py`, you can adjust:

- `HUMAN_COLOR` and `COMPUTER_COLOR`: set these to opposite colors, `"White"` and `"Black"`. If you choose Black, the computer makes the first move. The board still has White at the bottom.
- `ENGINE_DEPTH`: the number of plies to search, currently `3`. A ply is one move by either player. Use a value of at least `1`. Increasing it searches further ahead but takes longer.

## Known limitations

- The computer always promotes to a queen. The search also assumes queen promotion when considering the human player's replies.
- Position evaluation only considers material. It does not score king safety, pawn structure, or control of the center.
- Draw detection only covers stalemate. There is no detection for dead positions (such as king versus king), threefold or fivefold repetition, or the fifty- and seventy-five-move rules.
