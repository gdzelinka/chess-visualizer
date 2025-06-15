from enum import Enum
from typing import List, Tuple, Set

class PieceColor(Enum):
    WHITE = 'White'
    BLACK = 'Black'

class PieceType(Enum):
    PAWN = 'Pawn'
    KNIGHT = 'Knight'
    BISHOP = 'Bishop'
    ROOK = 'Rook'
    QUEEN = 'Queen'
    KING = 'King'
    GOLD_GENERAL = 'Gold'  # Custom piece from Shogi
    SILVER_GENERAL = 'Silver'
    SHOGI_KNIGHT = 'Shogi_Knight'
    LANCE = 'Lance'
    SHOGI_PAWN = 'Shogi_Pawn'
    DRAGON = 'Dragon'
    HORSE = 'Horse'

class PieceKey:
    def __init__(self, color, piece_type):
        self.color = color  # 'White' or 'Black'
        self.piece_type = piece_type  # 'Pawn', 'Knight', 'Bishop', 'Rook', 'Queen', 'King', 'Gold', 'Silver', 'Shogi_Knight', 'Lance', 'Shogi_Pawn', 'Dragon', 'Horse'
    
    @classmethod
    def from_string(cls, key_str):
        key_str = key_str.split('_', 1)
        return cls(key_str[0], key_str[1])
    
    def __str__(self):
        return f"{self.color}{self.piece_type}"

class Piece:
    def __init__(self, piece_type: str, color: str):
        self.piece_type = piece_type
        self.color = color
        self.symbol = color + '_' + piece_type

    def get_legal_moves(self, pos: Tuple[int, int], board_size: int) -> Set[Tuple[int, int]]:
        """Get all legal moves for this piece from the given position."""
        if self.piece_type == 'Pawn':
            return self._get_pawn_moves(pos, board_size)
        elif self.piece_type == 'Knight':
            return self._get_knight_moves(pos, board_size)
        elif self.piece_type == 'Bishop':
            return self._get_bishop_moves(pos, board_size)
        elif self.piece_type == 'Rook':
            return self._get_rook_moves(pos, board_size)
        elif self.piece_type == 'Queen':
            return self._get_queen_moves(pos, board_size)
        elif self.piece_type == 'King':
            return self._get_king_moves(pos, board_size)
        elif self.piece_type == 'Gold':
            return self._get_gold_moves(pos, board_size)
        elif self.piece_type == 'Silver':
            return self._get_silver_moves(pos, board_size)
        elif self.piece_type == 'Shogi_Knight':
            return self._get_shogi_knight_moves(pos, board_size)
        elif self.piece_type == 'Lance':
            return self._get_lance_moves(pos, board_size)
        elif self.piece_type == 'Shogi_Pawn':
            return self._get_shogi_pawn_moves(pos, board_size)
        elif self.piece_type == 'Dragon':
            return self._get_dragon_moves(pos, board_size)
        elif self.piece_type == 'Horse':
            return self._get_horse_moves(pos, board_size)
        return set()

    def _is_valid_position(self, pos: Tuple[int, int], board_size: int) -> bool:
        """Check if a position is valid on the board."""
        row, col = pos
        return 0 <= row < board_size and 0 <= col < board_size

    def _get_pawn_moves(self, pos, board_size):
        moves = []
        row, col = pos
        
        # White pawns start at row board_size-2 and move up (decreasing row)
        # Black pawns start at row 1 and move down (increasing row)
        if self.color == 'White':
            # White pawn moves
            # One square forward (up)
            if row > 0:  # Can't move up if at top
                moves.append((row - 1, col))
                # Two squares forward from starting position
                if row == board_size - 2:  # Starting position
                    moves.append((row - 2, col))
            # Diagonal captures
            if row > 0:  # Can't capture if at top
                if col > 0:  # Can capture left
                    moves.append((row - 1, col - 1))
                if col < board_size - 1:  # Can capture right
                    moves.append((row - 1, col + 1))
        else:
            # Black pawn moves
            # One square forward (down)
            if row < board_size - 1:  # Can't move down if at bottom
                moves.append((row + 1, col))
                # Two squares forward from starting position
                if row == 1:  # Starting position
                    moves.append((row + 2, col))
            # Diagonal captures
            if row < board_size - 1:  # Can't capture if at bottom
                if col > 0:  # Can capture left
                    moves.append((row + 1, col - 1))
                if col < board_size - 1:  # Can capture right
                    moves.append((row + 1, col + 1))
        
        return moves

    def _get_knight_moves(self, pos: Tuple[int, int], board_size: int) -> Set[Tuple[int, int]]:
        """Get all legal moves for a knight from the given position."""
        moves = set()
        row, col = pos
        
        # All possible knight moves (8 directions)
        possible_moves = [
            (row - 2, col - 1),  # Up-left
            (row - 2, col + 1),  # Up-right
            (row + 2, col - 1),  # Down-left
            (row + 2, col + 1),  # Down-right
            (row - 1, col - 2),  # Left-up
            (row - 1, col + 2),  # Right-up
            (row + 1, col - 2),  # Left-down
            (row + 1, col + 2)   # Right-down
        ]
        
        # Add only valid moves
        for move in possible_moves:
            if self._is_valid_position(move, board_size):
                moves.add(move)
        
        return moves

    def _get_bishop_moves(self, pos: Tuple[int, int], board_size: int) -> Set[Tuple[int, int]]:
        """Get all legal moves for a bishop from the given position."""
        moves = set()
        row, col = pos
        
        # Bishops move diagonally
        directions = [
            (-1, -1), (-1, 1),  # Up
            (1, -1), (1, 1)     # Down
        ]
        
        for row_dir, col_dir in directions:
            current_row, current_col = row + row_dir, col + col_dir
            while self._is_valid_position((current_row, current_col), board_size):
                moves.add((current_row, current_col))
                current_row += row_dir
                current_col += col_dir
        
        return moves

    def _get_rook_moves(self, pos: Tuple[int, int], board_size: int) -> Set[Tuple[int, int]]:
        """Get all legal moves for a rook from the given position."""
        moves = set()
        row, col = pos
        
        # All possible rook directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for row_dir, col_dir in directions:
            current_row, current_col = row + row_dir, col + col_dir
            while self._is_valid_position((current_row, current_col), board_size):
                moves.add((current_row, current_col))
                current_row += row_dir
                current_col += col_dir
        
        return moves

    def _get_queen_moves(self, pos: Tuple[int, int], board_size: int) -> Set[Tuple[int, int]]:
        """Get all legal moves for a queen from the given position."""
        # Queen moves are a combination of bishop and rook moves
        return self._get_bishop_moves(pos, board_size) | self._get_rook_moves(pos, board_size)

    def _get_king_moves(self, pos: Tuple[int, int], board_size: int) -> Set[Tuple[int, int]]:
        """Get all legal moves for a king from the given position."""
        moves = set()
        row, col = pos
        
        # All possible king moves
        king_moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for row_offset, col_offset in king_moves:
            new_row, new_col = row + row_offset, col + col_offset
            if self._is_valid_position((new_row, new_col), board_size):
                moves.add((new_row, new_col))
        
        return moves

    def _get_lance_moves(self, pos: Tuple[int, int], board_size: int) -> Set[Tuple[int, int]]:
        """Get all legal moves for a lance from the given position."""
        moves = set()
        row, col = pos
        
        # Lance can only move forward (up for White, down for Black)
        direction = -1 if self.color == 'White' else 1
        current_row = row + direction
        
        while self._is_valid_position((current_row, col), board_size):
            moves.add((current_row, col))
            current_row += direction
        
        return moves

    def _get_shogi_knight_moves(self, pos: Tuple[int, int], board_size: int) -> Set[Tuple[int, int]]:
        """Get all legal moves for a Shogi knight from the given position."""
        moves = set()
        row, col = pos
        
        # Shogi knight moves in an L-shape but only forward
        if self.color == 'White':
            # White knight moves up and to the sides
            moves = {
                (row - 2, col - 1),
                (row - 2, col + 1)
            }
        else:
            # Black knight moves down and to the sides
            moves = {
                (row + 2, col - 1),
                (row + 2, col + 1)
            }
        
        # Filter out invalid positions
        return {move for move in moves if self._is_valid_position(move, board_size)}

    def _get_silver_moves(self, pos: Tuple[int, int], board_size: int) -> Set[Tuple[int, int]]:
        """Get all legal moves for a silver general from the given position."""
        moves = set()
        row, col = pos
        
        # Silver general moves diagonally and one square forward
        if self.color == 'White':
            # White silver moves
            moves = {
                (row - 1, col - 1),  # Forward left
                (row - 1, col),      # Forward
                (row - 1, col + 1),  # Forward right
                (row + 1, col - 1),  # Backward left
                (row + 1, col + 1)   # Backward right
            }
        else:
            # Black silver moves
            moves = {
                (row + 1, col - 1),  # Forward left
                (row + 1, col),      # Forward
                (row + 1, col + 1),  # Forward right
                (row - 1, col - 1),  # Backward left
                (row - 1, col + 1)   # Backward right
            }
        
        # Filter out invalid positions
        return {move for move in moves if self._is_valid_position(move, board_size)}

    def _get_gold_moves(self, pos: Tuple[int, int], board_size: int) -> Set[Tuple[int, int]]:
        """Get all legal moves for a gold general from the given position."""
        moves = set()
        row, col = pos
        
        # Gold general moves like a king but cannot move diagonally backward
        if self.color == 'White':
            # White gold moves
            moves = {
                (row - 1, col - 1),  # Forward left
                (row - 1, col),      # Forward
                (row - 1, col + 1),  # Forward right
                (row, col - 1),      # Left
                (row, col + 1),      # Right
                (row + 1, col)       # Backward
            }
        else:
            # Black gold moves
            moves = {
                (row + 1, col - 1),  # Forward left
                (row + 1, col),      # Forward
                (row + 1, col + 1),  # Forward right
                (row, col - 1),      # Left
                (row, col + 1),      # Right
                (row - 1, col)       # Backward
            }
        
        # Filter out invalid positions
        return {move for move in moves if self._is_valid_position(move, board_size)}

# Factory function to create pieces
def create_piece(piece_type: str, color: str) -> Piece:
    """Create a new piece of the given type and color."""
    return Piece(piece_type, color)

# Dictionary of all available pieces
AVAILABLE_PIECES = {
    'White_Pawn':           (PieceType.PAWN, PieceColor.WHITE),
    'White_Knight':         (PieceType.KNIGHT, PieceColor.WHITE),
    'White_Bishop':         (PieceType.BISHOP, PieceColor.WHITE),
    'White_Rook':           (PieceType.ROOK, PieceColor.WHITE),
    'White_Queen':          (PieceType.QUEEN, PieceColor.WHITE),
    'White_King':           (PieceType.KING, PieceColor.WHITE),
    'White_Gold':           (PieceType.GOLD_GENERAL, PieceColor.WHITE),
    'White_Silver':         (PieceType.SILVER_GENERAL, PieceColor.WHITE),
    'White_Shogi_Knight':   (PieceType.SHOGI_KNIGHT, PieceColor.WHITE),
    'White_Lance':          (PieceType.LANCE, PieceColor.WHITE),
    'White_Shogi_Pawn':     (PieceType.SHOGI_PAWN, PieceColor.WHITE),
    'White_Dragon':         (PieceType.DRAGON, PieceColor.WHITE),
    'White_Horse':          (PieceType.HORSE, PieceColor.WHITE),
    'Black_Pawn':           (PieceType.PAWN, PieceColor.BLACK),
    'Black_Knight':         (PieceType.KNIGHT, PieceColor.BLACK),
    'Black_Bishop':         (PieceType.BISHOP, PieceColor.BLACK),
    'Black_Rook':           (PieceType.ROOK, PieceColor.BLACK),
    'Black_Queen':          (PieceType.QUEEN, PieceColor.BLACK),
    'Black_King':           (PieceType.KING, PieceColor.BLACK),
    'Black_Gold':           (PieceType.GOLD_GENERAL, PieceColor.BLACK),
    'Black_Silver':         (PieceType.SILVER_GENERAL, PieceColor.BLACK),
    'Black_Shogi_Knight':   (PieceType.SHOGI_KNIGHT, PieceColor.BLACK),
    'Black_Lance':          (PieceType.LANCE, PieceColor.BLACK),
    'Black_Shogi_Pawn':     (PieceType.SHOGI_PAWN, PieceColor.BLACK),
    'Black_Dragon':         (PieceType.DRAGON, PieceColor.BLACK),
    'Black_Horse':          (PieceType.HORSE, PieceColor.BLACK),
}   