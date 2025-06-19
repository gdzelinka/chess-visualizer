import pygame
import os
from pieces import create_piece, AVAILABLE_PIECES, ROYAL_PIECES, HOOK_MOVERS, JUMP_MOVERS
from presets import get_preset
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
        self.screen = pygame.display.set_mode((WINDOW_SIZE + PANEL_WIDTH,
                                               WINDOW_SIZE + SETTINGS_BAR_HEIGHT))
        pygame.display.set_caption("Chess Move Visualizer")
        self.piece_images = self.load_piece_images()
        self.settings_bar = SettingsBar(self.board_size)
        self.piece_panel = PiecePanel(self.piece_images, self.square_size)
        self.preset_menu = PresetMenu(WINDOW_SIZE + PANEL_WIDTH,
                                      WINDOW_SIZE + SETTINGS_BAR_HEIGHT)
        self.selected_square = None
        self.board = {}  # Dictionary to store piece positions
        self.dragging_piece = None
        self.drag_start_pos = None
        self.is_white_turn = True  # Track whose turn it is
        self.en_passant_target = None  # Track the square that can be captured en passant

        # Initialize board with tuples
        preset_pieces = get_preset('standard', self.board_size)['pieces']
        self.board = {}
        for pos, piece_key in preset_pieces.items():
            rank = self._get_piece_rank(piece_key)
            self.board[pos] = (piece_key, rank)

    def load_piece_images(self):
        pieces = {}

        # First load all images at their original size
        original_images = {}
        for file_name, value in AVAILABLE_PIECES.items():
            image_path = os.path.join("pieces", f"{file_name}.png")
            if os.path.exists(image_path):
                original_images[file_name] = pygame.image.load(image_path)

        # Then scale them to the board size
        for piece_key, image in original_images.items():
            pieces[piece_key] = pygame.transform.smoothscale(image,
                                                             (self.square_size,
                                                              self.square_size))

        return pieces

    def draw_board(self):
        # Fill the entire board area with panel color first
        pygame.draw.rect(self.screen,
                         PANEL_COLOR,
                         (0,
                          SETTINGS_BAR_HEIGHT,
                          WINDOW_SIZE,
                          WINDOW_SIZE))

        # Draw only the squares within the actual board size
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = col * self.square_size
                y = row * self.square_size + SETTINGS_BAR_HEIGHT
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(self.screen,
                                 color,
                                 (x,
                                  y,
                                  self.square_size,
                                  self.square_size))

    def draw_pieces(self):
        for pos, board_entry in self.board.items():
            row, col = pos
            # Handle tuple format (piece_key, rank)
            piece_key, _ = board_entry
                
            if piece_key in self.piece_images:
                x = col * self.square_size
                y = row * self.square_size + SETTINGS_BAR_HEIGHT
                self.screen.blit(self.piece_images[piece_key],
                                 (x, y))

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
            s = pygame.Surface((self.square_size,
                                self.square_size),
                               pygame.SRCALPHA)
            pygame.draw.rect(s, color, s.get_rect())
            self.screen.blit(s, (x, y))

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

    def _is_path_clear_for_royal_piece(self, start, end, piece_rank):
        """Check if the path between two squares is clear for Royal pieces, allowing jumps over pieces ranked below."""
        start_row, start_col = start
        end_row, end_col = end

        # Determine direction of movement
        row_dir = 0 if start_row == end_row else (1 if end_row > start_row else -1)
        col_dir = 0 if start_col == end_col else (1 if end_col > start_col else -1)

        # Check each square along the path
        current_row, current_col = start_row + row_dir, start_col + col_dir
        while (current_row, current_col) != (end_row, end_col):
            if (current_row, current_col) in self.board:
                # Get the rank of the piece in the way
                blocking_piece = self.board[(current_row, current_col)]
                blocking_piece_key, blocking_rank = blocking_piece
                
                # Rook_General can jump over pieces of rank 8 or below
                if blocking_rank >= piece_rank:
                    return False  # Cannot jump over this piece
            current_row += row_dir
            current_col += col_dir
        return True

    def get_legal_moves(self, square):
        board_result = self.board.get(square)
        if not board_result:
            return []
        start_row, start_col = square

        # Handle tuple format (piece_key, rank)
        piece_key, rank = board_result
        # Extract color and piece type from the key (format: "White_Knight")
        color, piece_type = piece_key.split('_', 1)

        # Create piece and get all possible moves with jump information
        piece = create_piece(piece_type, color, int(rank))
        moves_with_info = piece.get_legal_moves_with_info(square, self.board_size)

        # Filter moves based on piece blocking and capture opportunities
        ORIGIN_DIRECTION = {}
        filtered_moves = []
        if piece_type in JUMP_MOVERS:
            for move, can_jump in moves_with_info:
                if can_jump[0] == 'origin':
                    target_board_result = self.board.get(move)
                    if target_board_result:
                        target_piece_key, _ = target_board_result
                        target_color = target_piece_key.split('_')[0]
                    if target_board_result is None:
                        ORIGIN_DIRECTION[can_jump[1]] = move
                        filtered_moves.append((move, HIGHLIGHT_COLOR))
                    elif target_color != color:
                        filtered_moves.append((move, CAPTURE_COLOR))
            for move, can_jump in moves_with_info:
                if can_jump[0] == 'direction':
                    end_row, end_col = move
                    if can_jump[1] in ORIGIN_DIRECTION.keys():
                        move = (ORIGIN_DIRECTION[can_jump[1]][0] + end_row - start_row, ORIGIN_DIRECTION[can_jump[1]][1] + end_col - start_col)
                        target_board_result = self.board.get(move)
                        if target_board_result:
                            target_piece_key, _ = target_board_result
                            target_color = target_piece_key.split('_')[0]
                        else:
                            target_color = None
                        if target_board_result is None:
                            filtered_moves.append((move, HIGHLIGHT_COLOR))
                        elif target_color != color:
                            filtered_moves.append((move, CAPTURE_COLOR))
                else:
                    if target_board_result is None:
                        # Empty square, check if path is clear or if piece can jump
                        if can_jump == True or self._is_path_clear(square, move):
                            filtered_moves.append((move, HIGHLIGHT_COLOR))

                    elif target_color != color:  # Different color piece
                        if can_jump == True or self._is_path_clear(square, move):
                            filtered_moves.append((move, CAPTURE_COLOR))

        else: # Non-jump movers
            for move, can_jump in moves_with_info:
                target_board_result = self.board.get(move)
                if target_board_result:
                    target_piece_key, _ = target_board_result
                    target_color = target_piece_key.split('_')[0]
                else:
                    target_color = None

                # For pawns, handle forward and diagonal moves differently
                if piece_type == 'Pawn':
                    # Get the direction of movement
                    start_row, start_col = square
                    end_row, end_col = move
                    is_diagonal = start_col != end_col

                    if is_diagonal:
                        # Diagonal moves are only valid for captures
                        if target_board_result and target_color != color:
                            filtered_moves.append((move, CAPTURE_COLOR))
                        # Check for en passant
                        elif self.en_passant_target == move:
                            filtered_moves.append((move, CAPTURE_COLOR))
                    else:
                        # Forward moves are only valid for empty squares
                        if target_board_result is None:
                            # For two-square moves, check if the middle square is empty
                            if abs(end_row - start_row) == 2:
                                intermediate_row = (start_row + end_row) // 2
                                if (intermediate_row, start_col) not in self.board:
                                    filtered_moves.append((move, HIGHLIGHT_COLOR))
                            else:
                                filtered_moves.append((move, HIGHLIGHT_COLOR))
                elif piece_type in ROYAL_PIECES:
                    if self._is_path_clear_for_royal_piece(square, move, rank):
                        if target_board_result is None:
                            filtered_moves.append((move, HIGHLIGHT_COLOR))
                        else:
                            filtered_moves.append((move, CAPTURE_COLOR))
                elif piece_type in HOOK_MOVERS:
                    if target_board_result is None:
                        if self._is_path_clear(square, move):
                            filtered_moves.append((move, HIGHLIGHT_COLOR))
                        if can_jump:
                            self._highlight_turned_squares(square, move, color)
                    elif target_color != color:
                        if self._is_path_clear(square, move):
                            filtered_moves.append((move, CAPTURE_COLOR))
                else:
                    # For normal pieces, use standard move filtering
                    if target_board_result is None:
                        # Empty square, check if path is clear or if piece can jump
                        if can_jump or self._is_path_clear(square, move):
                            filtered_moves.append((move, HIGHLIGHT_COLOR))

                    elif target_color != color:  # Different color piece
                        if can_jump or self._is_path_clear(square, move):
                            filtered_moves.append((move, CAPTURE_COLOR))

        return filtered_moves

    def resize_board(self, new_size):
        if MIN_BOARD_SIZE <= new_size <= MAX_BOARD_SIZE:
            self.board_size = new_size
            self.square_size = WINDOW_SIZE // self.board_size
            self.settings_bar.update_size_text(self.board_size)
            self.piece_images = self.load_piece_images()
            self.piece_panel = PiecePanel(self.piece_images, self.square_size)
            # Initialize board with tuples
            preset_pieces = get_preset('standard', self.board_size)['pieces']
            self.board = {}
            for pos, piece_key in preset_pieces.items():
                rank = self._get_piece_rank(piece_key)
                self.board[pos] = (piece_key, rank)
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
            self.board = {}  # Clear the board
            self.selected_square = None
            self.dragging_piece = None
            self.en_passant_target = None

            # Initialize board with tuples
            preset_pieces = preset['pieces']
            for pos, piece_key in preset_pieces.items():
                rank = self._get_piece_rank(piece_key)
                self.board[pos] = (piece_key, rank)

            self.is_white_turn = True
            self.settings_bar.update_turn_text(self.is_white_turn)

    def _get_piece_color(self, board_entry):
        """Extract piece color from board entry (tuple format)."""
        piece_key, _ = board_entry
        return piece_key.split('_')[0]
    
    def _get_piece_type(self, board_entry):
        """Extract piece type from board entry (tuple format)."""
        piece_key, _ = board_entry
        return piece_key.split('_')[1]

    def _get_piece_rank(self, piece_key):
        """Get the rank for a piece key from AVAILABLE_PIECES."""
        if piece_key in AVAILABLE_PIECES:
            piece_info = AVAILABLE_PIECES[piece_key]
            # Convert PieceRank enum to numerical rank
            rank_enum = piece_info[2]
            if rank_enum.value == 1:  # KING
                return 10
            elif rank_enum.value == 2:  # GREAT_GENERAL
                return 9
            elif rank_enum.value == 3:  # VICE_GENERAL
                return 8
            elif rank_enum.value == 4:  # GENERAL
                return 7
            else:  # OTHER
                return 1
        return 1  # Default rank

    def _is_valid_position(self, pos):
        row, col = pos
        return 0 <= row < self.board_size and 0 <= col < self.board_size

    def _highlight_turned_squares(self, start, end, color):
        start_row, start_col = start
        end_row, end_col = end
        
        x_delta = end_col - start_col
        y_delta = end_row - start_row
        
        if x_delta == 0 and y_delta != 0: # Moving up or down
            #Highlight the squares to the left and right of the end square
            move = (end_row, end_col - 1)
            target_board_result = self.board.get(move) if self._is_valid_position(move) else None
            while self._is_valid_position(move) and target_board_result is None:
                self.highlight_square(move, HIGHLIGHT_COLOR)
                move = (move[0], move[1] - 1)
                target_board_result = self.board.get(move) if self._is_valid_position(move) else None
            if self._is_valid_position(move) and target_board_result is not None:
                target_piece_key, _ = target_board_result
                target_color = target_piece_key.split('_')[0]
                if target_color != color:
                    self.highlight_square(move, CAPTURE_COLOR)
            move = (end_row, end_col + 1)
            target_board_result = self.board.get(move) if self._is_valid_position(move) else None
            while self._is_valid_position(move) and target_board_result is None:
                self.highlight_square(move, HIGHLIGHT_COLOR)
                move = (move[0], move[1] + 1)
                target_board_result = self.board.get(move) if self._is_valid_position(move) else None
            if self._is_valid_position(move) and target_board_result is not None:
                target_piece_key, _ = target_board_result
                target_color = target_piece_key.split('_')[0]
                if target_color != color:
                    self.highlight_square(move, CAPTURE_COLOR)
        elif x_delta != 0 and y_delta == 0: # Moving right or left
            move = (end_row - 1, end_col)
            target_board_result = self.board.get(move) if self._is_valid_position(move) else None
            while self._is_valid_position(move) and target_board_result is None:
                self.highlight_square(move, HIGHLIGHT_COLOR)
                move = (move[0] - 1, move[1])
                target_board_result = self.board.get(move) if self._is_valid_position(move) else None
            if self._is_valid_position(move) and target_board_result is not None:
                target_piece_key, _ = target_board_result
                target_color = target_piece_key.split('_')[0]
                if target_color != color:
                    self.highlight_square(move, CAPTURE_COLOR)
            move = (end_row + 1, end_col)
            target_board_result = self.board.get(move) if self._is_valid_position(move) else None
            while self._is_valid_position(move) and target_board_result is None:
                self.highlight_square(move, HIGHLIGHT_COLOR)
                move = (move[0] + 1, move[1])
                target_board_result = self.board.get(move) if self._is_valid_position(move) else None
            if self._is_valid_position(move) and target_board_result is not None:
                target_piece_key, _ = target_board_result
                target_color = target_piece_key.split('_')[0]
                if target_color != color:
                    self.highlight_square(move, CAPTURE_COLOR)
        elif (x_delta < 0 and y_delta < 0) or (x_delta > 0 and y_delta > 0): # Moving diagonally
            move = (end_row - 1, end_col + 1)
            target_board_result = self.board.get(move) if self._is_valid_position(move) else None
            while self._is_valid_position(move) and target_board_result is None:
                self.highlight_square(move, HIGHLIGHT_COLOR)
                move = (move[0] - 1, move[1] + 1)
                target_board_result = self.board.get(move) if self._is_valid_position(move) else None
            if self._is_valid_position(move) and target_board_result is not None:
                target_piece_key, _ = target_board_result
                target_color = target_piece_key.split('_')[0]
                if target_color != color:
                    self.highlight_square(move, CAPTURE_COLOR)
            move = (end_row + 1, end_col - 1)
            target_board_result = self.board.get(move) if self._is_valid_position(move) else None
            while self._is_valid_position(move) and target_board_result is None:
                self.highlight_square(move, HIGHLIGHT_COLOR)
                move = (move[0] + 1, move[1] - 1)
                target_board_result = self.board.get(move) if self._is_valid_position(move) else None
            if self._is_valid_position(move) and target_board_result is not None:
                target_piece_key, _ = target_board_result
                target_color = target_piece_key.split('_')[0]
                if target_color != color:
                    self.highlight_square(move, CAPTURE_COLOR)
        elif (x_delta < 0 and y_delta > 0) or (x_delta > 0 and y_delta < 0): # Moving diagonally
            move = (end_row + 1, end_col + 1)
            target_board_result = self.board.get(move) if self._is_valid_position(move) else None
            while self._is_valid_position(move) and target_board_result is None:
                self.highlight_square(move, HIGHLIGHT_COLOR)
                move = (move[0] + 1, move[1] + 1)
                target_board_result = self.board.get(move) if self._is_valid_position(move) else None
            if self._is_valid_position(move) and target_board_result is not None:
                target_piece_key, _ = target_board_result
                target_color = target_piece_key.split('_')[0]
                if target_color != color:
                    self.highlight_square(move, CAPTURE_COLOR)
            move = (end_row - 1, end_col - 1)
            target_board_result = self.board.get(move) if self._is_valid_position(move) else None
            while self._is_valid_position(move) and target_board_result is None:
                self.highlight_square(move, HIGHLIGHT_COLOR)
                move = (move[0] - 1, move[1] - 1)
                target_board_result = self.board.get(move) if self._is_valid_position(move) else None
            if self._is_valid_position(move) and target_board_result is not None:
                target_piece_key, _ = target_board_result
                target_color = target_piece_key.split('_')[0]
                if target_color != color:
                    self.highlight_square(move, CAPTURE_COLOR)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Reset to standard preset with tuples
                        preset_pieces = get_preset('standard', self.board_size)['pieces']
                        self.board = {}
                        for pos, piece_key in preset_pieces.items():
                            rank = self._get_piece_rank(piece_key)
                            self.board[pos] = (piece_key, rank)
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
                            if self.selected_square == square:
                                self.selected_square = None
                            continue

                        if self.dragging_piece:
                            # Place the dragged piece on the board with rank
                            rank = self._get_piece_rank(self.dragging_piece)
                            self.board[square] = (self.dragging_piece, rank)
                            self.dragging_piece = None
                            self.en_passant_target = None  # Clear en passant target on piece placement
                        else:
                            # Chess logic
                            if self.selected_square is None:
                                if square in self.board:
                                    # Only select pieces of the current turn's color
                                    piece_color = self._get_piece_color(self.board[square])
                                    if piece_color == ('White' if self.is_white_turn else 'Black'):
                                        self.selected_square = square
                            else:
                                # If clicking the same square or a square with a piece of the same color, just deselect
                                if square == self.selected_square or (
                                    square in self.board and
                                    self._get_piece_color(self.board[square]) ==
                                    self._get_piece_color(self.board[self.selected_square])
                                ):
                                    self.selected_square = None
                                else:
                                    # Check if there's still a piece at the selected square
                                    if self.selected_square not in self.board:
                                        self.selected_square = None
                                        continue
                                    
                                    # Move piece to new position
                                    piece = self.board.pop(self.selected_square)
                                    start_row, start_col = self.selected_square
                                    end_row, end_col = square

                                    # Check if this was a two-square pawn move
                                    piece_type = self._get_piece_type(piece)
                                    if piece_type == 'Pawn' and abs(end_row - start_row) == 2:
                                        # Set the en passant target square
                                        self.en_passant_target = ((start_row + end_row) // 2, start_col)
                                    else:
                                        self.en_passant_target = None

                                    # Handle en passant capture
                                    if piece_type == 'Pawn' and square == self.en_passant_target:
                                        # Remove the captured pawn
                                        piece_color = self._get_piece_color(piece)
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
                            # store the piece key with rank
                            rank = self._get_piece_rank(self.dragging_piece)
                            self.board[square] = (self.dragging_piece, rank)
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
