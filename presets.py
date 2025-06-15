"""
This module defines custom board presets for the chess visualizer.
Each preset is a dictionary containing:
- name: A descriptive name for the preset
- size: The board size (width and height)
- pieces: A dictionary mapping (row, col) tuples to piece keys (e.g., 'wp' for white pawn)
"""

# Standard chess starting position
STANDARD_CHESS = {
    'name': 'Standard Chess',
    'size': 8,
    'pieces': {
        # White pieces - positioned on highest two rows
        # Rooks
        (7, 0): 'White_Rook', (7, 7): 'White_Rook',
        # Knights
        (7, 1): 'White_Knight', (7, 6): 'White_Knight',
        # Bishops
        (7, 2): 'White_Bishop', (7, 5): 'White_Bishop',
        # Queen and King
        (7, 3): 'White_Queen', (7, 4): 'White_King',
        # Pawns
        (6, 0): 'White_Pawn', (6, 1): 'White_Pawn', (6, 2): 'White_Pawn', (6, 3): 'White_Pawn',
        (6, 4): 'White_Pawn', (6, 5): 'White_Pawn', (6, 6): 'White_Pawn', (6, 7): 'White_Pawn',
        
        # Black pieces - positioned on lowest two rows
        # Rooks
        (0, 0): 'Black_Rook', (0, 7): 'Black_Rook',
        # Knights
        (0, 1): 'Black_Knight', (0, 6): 'Black_Knight',
        # Bishops
        (0, 2): 'Black_Bishop', (0, 5): 'Black_Bishop',
        # Queen and King
        (0, 3): 'Black_Queen', (0, 4): 'Black_King',
        # Pawns
        (1, 0): 'Black_Pawn', (1, 1): 'Black_Pawn', (1, 2): 'Black_Pawn', (1, 3): 'Black_Pawn',
        (1, 4): 'Black_Pawn', (1, 5): 'Black_Pawn', (1, 6): 'Black_Pawn', (1, 7): 'Black_Pawn'
    }
}

# Small board with just kings and pawns
SMALL_KINGS_PAWNS = {
    'name': 'Small Kings and Pawns',
    'size': 6,
    'pieces': {
        # White pieces
        (5, 0): 'White_King', (5, 5): 'White_King',
        (4, 0): 'White_Pawn', (4, 1): 'White_Pawn', (4, 2): 'White_Pawn',
        (4, 3): 'White_Pawn', (4, 4): 'White_Pawn', (4, 5): 'White_Pawn',
        
        # Black pieces
        (0, 0): 'Black_King', (0, 5): 'Black_King',
        (1, 0): 'Black_Pawn', (1, 1): 'Black_Pawn', (1, 2): 'Black_Pawn',
        (1, 3): 'Black_Pawn', (1, 4): 'Black_Pawn', (1, 5): 'Black_Pawn'
    }
}

# Large board with multiple queens
LARGE_MULTIQUEEN = {
    'name': 'Large Multi-Queen',
    'size': 12,
    'pieces': {
        # White pieces
        (11, 0): 'White_Queen', (11, 11): 'White_Queen',
        (10, 1): 'White_Queen', (10, 10): 'White_Queen',
        (9, 2): 'White_Queen', (9, 9): 'White_Queen',
        
        # Black pieces
        (0, 0): 'Black_Queen', (0, 11): 'Black_Queen',
        (1, 1): 'Black_Queen', (1, 10): 'Black_Queen',
        (2, 2): 'Black_Queen', (2, 9): 'Black_Queen'
    }
}

# Shogi starting position
SHOGI_STANDARD = {
    'name': 'Shogi Standard',
    'size': 9,
    'pieces': {
        # White pieces
        (8, 0): 'White_Lance', (8, 1): 'White_Shogi_Knight', (8, 2): 'White_Silver', (8, 3): 'White_Gold',
        (8, 4): 'White_King', (8, 5): 'White_Gold', (8, 6): 'White_Silver', (8, 7): 'White_Shogi_Knight',
        (8, 8): 'White_Lance',
        (7, 1): 'White_Bishop', (7, 7): 'White_Rook',
        (6, 0): 'White_Shogi_Pawn', (6, 1): 'White_Shogi_Pawn', (6, 2): 'White_Shogi_Pawn', (6, 3): 'White_Shogi_Pawn', (6, 4): 'White_Shogi_Pawn',
        (6, 5): 'White_Shogi_Pawn', (6, 6): 'White_Shogi_Pawn', (6, 7): 'White_Shogi_Pawn', (6, 8): 'White_Shogi_Pawn',
        
        # Black pieces  
        (0, 0): 'Black_Lance', (0, 1): 'Black_Shogi_Knight', (0, 2): 'Black_Silver', (0, 3): 'Black_Gold',
        (0, 4): 'Black_King', (0, 5): 'Black_Gold', (0, 6): 'Black_Silver', (0, 7): 'Black_Shogi_Knight',
        (0, 8): 'Black_Lance',
        (1, 1): 'Black_Rook', (1, 7): 'Black_Bishop',
        (2, 0): 'Black_Shogi_Pawn', (2, 1): 'Black_Shogi_Pawn', (2, 2): 'Black_Shogi_Pawn', (2, 3): 'Black_Shogi_Pawn', (2, 4): 'Black_Shogi_Pawn',
        (2, 5): 'Black_Shogi_Pawn', (2, 6): 'Black_Shogi_Pawn', (2, 7): 'Black_Shogi_Pawn', (2, 8): 'Black_Shogi_Pawn',
    }
}

# Dictionary of all available presets
PRESETS = {
    'standard': STANDARD_CHESS,
    'small_kings_pawns': SMALL_KINGS_PAWNS,
    'large_multiqueen': LARGE_MULTIQUEEN,
    'shogi_standard': SHOGI_STANDARD
}

def get_preset(preset_name, board_size=None):
    """Get a preset by name."""
    preset = PRESETS.get(preset_name)
    if preset and preset_name == 'standard':
        # For standard preset, adjust piece positions based on board size
        size = board_size if board_size is not None else preset['size']
        pieces = {}
        
        # White pieces - positioned on highest two rows
        # Rooks
        pieces[(size-1, 0)] = 'White_Rook'
        pieces[(size-1, size-1)] = 'White_Rook'
        # Knights
        pieces[(size-1, 1)] = 'White_Knight'
        pieces[(size-1, size-2)] = 'White_Knight'
        # Bishops
        pieces[(size-1, 2)] = 'White_Bishop'
        pieces[(size-1, size-3)] = 'White_Bishop'
        # Queen and King
        pieces[(size-1, 3)] = 'White_Queen'
        pieces[(size-1, 4)] = 'White_King'
        # Pawns
        for col in range(size):
            pieces[(size-2, col)] = 'White_Pawn'
        
        # Black pieces - positioned on lowest two rows
        # Rooks
        pieces[(0, 0)] = 'Black_Rook'
        pieces[(0, size-1)] = 'Black_Rook'
        # Knights
        pieces[(0, 1)] = 'Black_Knight'
        pieces[(0, size-2)] = 'Black_Knight'
        # Bishops
        pieces[(0, 2)] = 'Black_Bishop'
        pieces[(0, size-3)] = 'Black_Bishop'
        # Queen and King
        pieces[(0, 3)] = 'Black_Queen'
        pieces[(0, 4)] = 'Black_King'
        # Pawns
        for col in range(size):
            pieces[(1, col)] = 'Black_Pawn'
        
        return {
            'name': preset['name'],
            'size': size,
            'pieces': pieces
        }
    return preset

def get_all_presets():
    """Get all available presets."""
    return PRESETS

def add_preset(name, size, pieces):
    """Add a new preset to the collection."""
    PRESETS[name] = {
        'name': name,
        'size': size,
        'pieces': pieces
    } 