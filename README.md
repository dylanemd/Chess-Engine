# Python Chess

A playable chess game built with [Pygame](https://www.pygame.org/), featuring a simple AI opponent powered by minimax search with alpha-beta pruning.

## Features

- Full chess rules: legal move generation, check/checkmate/stalemate detection
- Castling (kingside and queenside) and en passant
- Pawn promotion (choose Queen, Rook, Bishop, or Knight when you promote)
- Computer opponent using minimax + alpha-beta pruning, evaluating positions by material
- Simple click-to-move UI with move highlighting

## Requirements

- Python 3.9+
- [Pygame](https://www.pygame.org/)

Install dependencies:

```bash
pip install pygame
```

## Setup

This project expects piece images in an `images/` folder at the project root, named using the standard `<color><piece>.png` convention (e.g. `wp.png` for white pawn, `bk.png` for black king):

```
images/
  wp.png  wn.png  wb.png  wr.png  wq.png  wk.png
  bp.png  bn.png  bb.png  br.png  bq.png  bk.png
```

You'll need to supply your own piece image set (many free sets are available online) and place them in the `images/` folder before running the game.

## Running the game

```bash
python main.py
```

You play as White; the computer plays Black. Click a piece to see its legal moves highlighted, then click a highlighted square to move.

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

## Configuring the engine

In `main.py`, you can adjust:

- `HUMAN_COLOR` / `COMPUTER_COLOR` — swap which side you play
- `ENGINE_DEPTH` — how many plies deep the AI searches (higher = stronger but slower)

## Known limitations

- The computer always promotes pawns to a Queen
- Position evaluation is material-only (no positional heuristics)
- No draw detection for threefold repetition or the fifty-move rule
