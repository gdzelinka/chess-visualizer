# Chess Move Visualizer

A Python application that visualizes chess moves using pygame and python-chess. Supports both standard 8x8 chess and custom board sizes.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the program:
```bash
python chess_visualizer.py
```

## Features
- Visual chess board representation
- Support for custom board sizes (4x4 to 20x20)
- Move validation for standard 8x8 chess
- Interactive piece movement
- Legal move highlighting
- Settings bar for board size adjustment

## Controls
- Click on a piece to select it
- Click on a valid square to move the selected piece
- Press 'r' to reset the board
- Press 'q' to quit the game
- Use the settings bar to adjust board size:
  - Click "- Board" to decrease size
  - Click "+ Board" to increase size

## Custom Board Sizes
- For non-standard board sizes (not 8x8):
  - Pieces are represented as simple pawns
  - No chess rules are enforced
  - You can move pieces freely
  - Board is initialized with pawns in the top and bottom two rows 