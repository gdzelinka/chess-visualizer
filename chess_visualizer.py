import pygame
import chess
import os
from pieces import Piece, create_piece, AVAILABLE_PIECES, PieceKey
from presets import get_preset, get_all_presets
from menus import SettingsBar, PiecePanel, PresetMenu, WINDOW_SIZE, PANEL_WIDTH, SETTINGS_BAR_HEIGHT

# Initialize Pygame
pygame.init()

# Constants
DEFAULT_BOARD_SIZE = 8
MIN_BOARD_SIZE = 4
MAX_BOARD_SIZE = 300
WHITE = (255, 255, 255)
BLACK = (128, 128, 128)
HIGHLIGHT_COLOR = (124, 252, 0, 128)  # Light green with alpha
SELECTED_COLOR = (255, 255, 0, 128)    # Yellow with alpha
CAPTURE_COLOR = (255, 0, 0, 128)       # Red with alpha for capture squares
PANEL_COLOR = (180, 180, 180)

class ChessVisualizer:
    def __init__(self):
        self.board_size = DEFAULT_BOARD_SIZE
        self.square_size = WINDOW_SIZE // self.board_size
        self.screen = pygame.display.set_mode((WINDOW_SIZE + PANEL_WIDTH, WINDOW_SIZE + SETTINGS_BAR_HEIGHT))
        pygame.display.set_caption("Chess Move Visualizer")
        self.piece_images = self.load_piece_images()
        self.settings_bar = SettingsBar(self.board_size)
        self.piece_panel = PiecePanel(self.piece_images, self.square_size)
        self.preset_menu = PresetMenu(WINDOW_SIZE + PANEL_WIDTH, WINDOW_SIZE + SETTINGS_BAR_HEIGHT)
        self.selected_square = None
        self.board = {}  # Dictionary to store piece positions
        self.dragging_piece = None
        self.drag_start_pos = None
        self.is_white_turn = True  # Track whose turn it is
        self.en_passant_target = None  # Track the square that can be captured en passant
        

        self.board = get_preset('standard', self.board_size)['pieces'].copy()

    def load_piece_images(self):
        pieces = {}
        # Define the piece types we need
        piece_types = ['Pawn', 'Knight', 'Bishop', 'Rook', 'Queen', 'King', 'Gold', 'Silver', 'Shogi_Knight', 'Lance', 'Shogi_Pawn', 'Dragon', 'Horse']
        colors = ['White', 'Black']
        
        # First load all images at their original size
        original_images = {}
        for color in colors:
            for piece_type in piece_types:
                piece_key = color + '_' + piece_type
                image_path = os.path.join("pieces", f"{piece_key}.png")
                if os.path.exists(image_path):
                    original_images[piece_key] = pygame.image.load(image_path)
        
        # Then scale them to the board size
        for piece_key, image in original_images.items():
            pieces[piece_key] = pygame.transform.smoothscale(image, (self.square_size, self.square_size))
            
        return pieces

    def draw_board(self):
        # Calculate the actual board dimensions
        actual_width = self.board_size * self.square_size
        actual_height = self.board_size * self.square_size
        
        # Fill the entire board area with panel color first
        pygame.draw.rect(self.screen, PANEL_COLOR, 
                        (0, SETTINGS_BAR_HEIGHT, WINDOW_SIZE, WINDOW_SIZE))
        
        # Draw only the squares within the actual board size
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = col * self.square_size
                y = row * self.square_size + SETTINGS_BAR_HEIGHT
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(self.screen, color, (x, y, self.square_size, self.square_size))

    def draw_pieces(self):
            for pos, piece_key in self.board.items():
                row, col = pos
                if piece_key in self.piece_images:
                    x = col * self.square_size
                    y = row * self.square_size + SETTINGS_BAR_HEIGHT
                    self.screen.blit(self.piece_images[piece_key], (x, y))

    def get_square_from_pos(self, pos):
        x, y = pos
        if y < SETTINGS_BAR_HEIGHT or x >= WINDOW_SIZE:
            return None
        y -= SETTINGS_BAR_HEIGHT
        col = x // self.square_size
        row = y // self.square_size
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            return (row, col)
        return None

    def highlight_square(self, square, color):
        if square is not None:
            row, col = square
            x = col * self.square_size
            y = row * self.square_size + SETTINGS_BAR_HEIGHT
            s = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            pygame.draw.rect(s, color, s.get_rect())
            self.screen.blit(s, (x, y))

    def get_legal_moves(self, square):
        piece_key = self.board.get(square)
        if not piece_key:
            return []
        
        # Extract color and piece type from the key (format: "White_Knight" or "Black_Pawn")
        color, piece_type = piece_key.split('_', 1)
        
        # Create piece and get all possible moves
        piece = create_piece(piece_type, color)
        moves = piece.get_legal_moves(square, self.board_size)
        
        # Filter moves based on piece blocking and capture opportunities
        filtered_moves = []
        for move in moves:
            target_piece = self.board.get(move)
            target_color = target_piece.split('_')[0] if target_piece else None

            # For pawns, handle forward and diagonal moves differently
            if piece_type == 'Pawn':
                # Get the direction of movement
                start_row, start_col = square
                end_row, end_col = move
                is_diagonal = start_col != end_col
                
                if is_diagonal:
                    # Diagonal moves are only valid for captures
                    if target_piece and target_color != color:
                        filtered_moves.append((move, CAPTURE_COLOR))
                    # Check for en passant
                    elif self.en_passant_target == move:
                        filtered_moves.append((move, CAPTURE_COLOR))
                else:
                    # Forward moves are only valid for empty squares
                    if target_piece is None:
                        # For two-square moves, check if the intermediate square is empty
                        if abs(end_row - start_row) == 2:
                            intermediate_row = (start_row + end_row) // 2
                            if (intermediate_row, start_col) not in self.board:
                                filtered_moves.append((move, HIGHLIGHT_COLOR))
                        else:
                            filtered_moves.append((move, HIGHLIGHT_COLOR))
            else:
                # For non-pawn pieces, use standard move filtering
                if target_piece is None:
                    # Empty square, check if path is clear
                    if piece_type in ['Knight', 'Shogi_Knight'] or self._is_path_clear(square, move):
                        filtered_moves.append((move, HIGHLIGHT_COLOR))
                elif target_color != color:  # Different color piece
                    # Can capture, check if path is clear
                    if piece_type in ['Knight', 'Shogi_Knight'] or self._is_path_clear(square, move):
                        filtered_moves.append((move, CAPTURE_COLOR))
        
        return filtered_moves

    def _is_path_clear(self, start, end):
        """Check if the path between two squares is clear of pieces."""
        start_row, start_col = start
        end_row, end_col = end
        
        # Determine direction of movement
        row_dir = 0 if start_row == end_row else (1 if end_row > start_row else -1)
        col_dir = 0 if start_col == end_col else (1 if end_col > start_col else -1)
        
        # Check each square along the path
        current_row, current_col = start_row + row_dir, start_col + col_dir
        while (current_row, current_col) != (end_row, end_col):
            if (current_row, current_col) in self.board:
                return False
            current_row += row_dir
            current_col += col_dir
        return True

    def resize_board(self, new_size):
        if MIN_BOARD_SIZE <= new_size <= MAX_BOARD_SIZE:
            self.board_size = new_size
            self.square_size = WINDOW_SIZE // self.board_size
            self.settings_bar.update_size_text(self.board_size)
            self.piece_images = self.load_piece_images()
            self.piece_panel = PiecePanel(self.piece_images, self.square_size)
            self.board = get_preset('standard', self.board_size)['pieces'].copy()
            # Clear selected square when resizing
            self.selected_square = None
            self.dragging_piece = None

    def apply_preset(self, preset_name):
        preset = get_preset(preset_name, self.board_size)
        if preset:
            self.board_size = preset['size']
            self.square_size = WINDOW_SIZE // self.board_size
            self.settings_bar.update_size_text(self.board_size)
            self.piece_images = self.load_piece_images()
            self.piece_panel = PiecePanel(self.piece_images, self.square_size)
            self.board = preset['pieces'].copy()
            
            self.is_white_turn = True
            self.settings_bar.update_turn_text(self.is_white_turn)
            self.selected_square = None
            self.dragging_piece = None
            self.en_passant_target = None

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.board = get_preset('standard', self.board_size)['pieces'].copy()
                        self.selected_square = None
                        self.dragging_piece = None
                        self.is_white_turn = True
                        self.settings_bar.update_turn_text(self.is_white_turn)
                        self.en_passant_target = None
                    elif event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_ESCAPE:
                        self.preset_menu.visible = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    # Check if click is in settings bar
                    if pos[1] < SETTINGS_BAR_HEIGHT:
                        action = self.settings_bar.handle_click(pos)
                        if action == "decrease":
                            self.resize_board(self.board_size - 1)
                        elif action == "increase":
                            self.resize_board(self.board_size + 1)
                        elif action == "toggle_turn":
                            self.is_white_turn = not self.is_white_turn
                            self.settings_bar.update_turn_text(self.is_white_turn)
                            self.en_passant_target = None  # Clear en passant target on turn change
                        elif action == "show_presets":
                            self.preset_menu.visible = True
                        continue
                    
                    # Check if click is in preset menu
                    if self.preset_menu.visible:
                        preset_name = self.preset_menu.handle_click(pos)
                        if preset_name:
                            self.apply_preset(preset_name)
                            self.preset_menu.visible = False
                        continue
                    
                    # Check if click is in piece panel
                    if pos[0] >= WINDOW_SIZE:
                        piece_key = self.piece_panel.handle_click(pos)
                        if piece_key:
                            self.dragging_piece = piece_key
                            self.drag_start_pos = pos
                        continue
                    
                    # Handle board clicks
                    square = self.get_square_from_pos(pos)
                    if square is not None:
                        # Handle right-click to remove pieces
                        if event.button == 3:  # Right mouse button
                            self.board.pop(square, None)
                            continue
                            
                        if self.dragging_piece:
                            # Place the dragged piece on the board
                            self.board[square] = self.dragging_piece
                            self.dragging_piece = None
                            self.en_passant_target = None  # Clear en passant target on piece placement
                        else:
                            # Chess logic
                            if self.selected_square is None:
                                if square in self.board:
                                    # Only select pieces of the current turn's color
                                    piece_color = self.board[square].split('_')[0]
                                    if piece_color == ('White' if self.is_white_turn else 'Black'):
                                        self.selected_square = square
                            else:
                                # If clicking the same square or a square with a piece of the same color, just deselect
                                if square == self.selected_square or (
                                    square in self.board and 
                                    self.board[square].split('_')[0] == 
                                    self.board[self.selected_square].split('_')[0]
                                ):
                                    self.selected_square = None
                                else:
                                    # Move piece to new position
                                    piece = self.board.pop(self.selected_square)
                                    start_row, start_col = self.selected_square
                                    end_row, end_col = square
                                    
                                    # Check if this was a two-square pawn move
                                    piece_type = piece.split('_')[1]
                                    if piece_type == 'Pawn' and abs(end_row - start_row) == 2:
                                        # Set the en passant target square
                                        self.en_passant_target = ((start_row + end_row) // 2, start_col)
                                    else:
                                        self.en_passant_target = None
                                    
                                    # Handle en passant capture
                                    if piece_type == 'Pawn' and square == self.en_passant_target:
                                        # Remove the captured pawn
                                        piece_color = piece.split('_')[0]
                                        captured_row = start_row if piece_color == 'White' else end_row
                                        self.board.pop((captured_row, end_col), None)
                                    
                                    self.board[square] = piece
                                    self.selected_square = None
                                    self.is_white_turn = not self.is_white_turn
                                    self.settings_bar.update_turn_text(self.is_white_turn)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.dragging_piece:
                        pos = pygame.mouse.get_pos()
                        square = self.get_square_from_pos(pos)
                        if square is not None:
                            # store the piece key
                            self.board[square] = self.dragging_piece
                        self.dragging_piece = None

            # Draw everything
            self.draw_board()
            
            if self.selected_square is not None:
                self.highlight_square(self.selected_square, SELECTED_COLOR)
                legal_moves = self.get_legal_moves(self.selected_square)
                for move, color in legal_moves:
                    self.highlight_square(move, color)
            
            self.draw_pieces()
            self.settings_bar.draw(self.screen)
            self.piece_panel.draw(self.screen)
            self.preset_menu.draw(self.screen)
            
            # Draw the dragging piece if any
            if self.dragging_piece:
                mouse_pos = pygame.mouse.get_pos()
                self.screen.blit(self.piece_images[self.dragging_piece], 
                               (mouse_pos[0] - self.square_size//2, 
                                mouse_pos[1] - self.square_size//2))
            
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    visualizer = ChessVisualizer()
    visualizer.run() 