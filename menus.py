import pygame
import os
from presets import get_preset, get_all_presets

# Constants
WINDOW_SIZE = 800
PANEL_WIDTH = 200
SETTINGS_BAR_HEIGHT = 50
SETTINGS_BAR_COLOR = (200, 200, 200)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)
TEXT_COLOR = (0, 0, 0)
PANEL_COLOR = (180, 180, 180)

class SettingsBar:
    def __init__(self, board_size):
        self.height = SETTINGS_BAR_HEIGHT
        self.width = WINDOW_SIZE + PANEL_WIDTH
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.font = pygame.font.Font(None, 24)
        
        # Create buttons
        button_width = 100
        button_height = 30
        button_y = (self.height - button_height) // 2
        
        # Decrease size button
        self.decrease_btn = pygame.Rect(10, button_y, button_width, button_height)
        self.decrease_text = self.font.render("- Board", True, TEXT_COLOR)
        
        # Increase size button
        self.increase_btn = pygame.Rect(120, button_y, button_width, button_height)
        self.increase_text = self.font.render("+ Board", True, TEXT_COLOR)
        
        # Turn toggle button
        self.turn_btn = pygame.Rect(self.width - button_width - 10, button_y, button_width, button_height)
        self.turn_text = self.font.render("White's Turn", True, TEXT_COLOR)
        
        # Preset button
        self.preset_btn = pygame.Rect(self.width - 2 * button_width - 20, button_y, button_width, button_height)
        self.preset_text = self.font.render("Presets", True, TEXT_COLOR)
        
        # Size text
        self.size_text = self.font.render(f"Board Size: {board_size}x{board_size}", True, TEXT_COLOR)
        self.size_text_rect = self.size_text.get_rect(centerx=self.width//2, centery=self.height//2)

    def draw(self, screen):
        # Draw settings bar background
        pygame.draw.rect(screen, SETTINGS_BAR_COLOR, self.rect)
        
        # Draw buttons
        pygame.draw.rect(screen, BUTTON_COLOR, self.decrease_btn)
        pygame.draw.rect(screen, BUTTON_COLOR, self.increase_btn)
        pygame.draw.rect(screen, BUTTON_COLOR, self.turn_btn)
        pygame.draw.rect(screen, BUTTON_COLOR, self.preset_btn)
        
        # Draw button text
        screen.blit(self.decrease_text, (self.decrease_btn.centerx - self.decrease_text.get_width()//2,
                                       self.decrease_btn.centery - self.decrease_text.get_height()//2))
        screen.blit(self.increase_text, (self.increase_btn.centerx - self.increase_text.get_width()//2,
                                       self.increase_btn.centery - self.increase_text.get_height()//2))
        screen.blit(self.turn_text, (self.turn_btn.centerx - self.turn_text.get_width()//2,
                                   self.turn_btn.centery - self.turn_text.get_height()//2))
        screen.blit(self.preset_text, (self.preset_btn.centerx - self.preset_text.get_width()//2,
                                     self.preset_btn.centery - self.preset_text.get_height()//2))
        
        # Draw size text
        screen.blit(self.size_text, self.size_text_rect)

    def handle_click(self, pos):
        if self.decrease_btn.collidepoint(pos):
            return "decrease"
        elif self.increase_btn.collidepoint(pos):
            return "increase"
        elif self.turn_btn.collidepoint(pos):
            return "toggle_turn"
        elif self.preset_btn.collidepoint(pos):
            return "show_presets"
        return None

    def update_size_text(self, board_size):
        self.size_text = self.font.render(f"Board Size: {board_size}x{board_size}", True, TEXT_COLOR)
        self.size_text_rect = self.size_text.get_rect(centerx=self.width//2, centery=self.height//2)

    def update_turn_text(self, is_white_turn):
        self.turn_text = self.font.render("White's Turn" if is_white_turn else "Black's Turn", True, TEXT_COLOR)

class PiecePanel:
    def __init__(self, piece_images, square_size):
        self.piece_images = piece_images
        self.square_size = square_size
        self.pieces_per_page = 7  # Number of piece pairs to show at once
        self.current_page = 0
        
        # Group pieces by type (without color)
        self.piece_pairs = []
        piece_types = set()
        for piece_key in piece_images.keys():
            color, piece_type = piece_key.split('_', 1)
            piece_types.add(piece_type)
        
        # Create pairs of white and black pieces
        for piece_type in sorted(piece_types):
            white_key = f"White_{piece_type}"
            black_key = f"Black_{piece_type}"
            if white_key in piece_images and black_key in piece_images:
                self.piece_pairs.append((white_key, black_key))
        
        self.total_pages = (len(self.piece_pairs) + self.pieces_per_page - 1) // self.pieces_per_page
        
        # Calculate panel dimensions
        self.width = PANEL_WIDTH
        self.height = WINDOW_SIZE
        self.x = WINDOW_SIZE
        self.y = SETTINGS_BAR_HEIGHT
        
        # Button dimensions
        self.button_height = 30
        self.button_width = 60
        self.button_margin = 10
        
        # Calculate the area for pieces
        self.pieces_area_height = self.height - (2 * (self.button_height + self.button_margin))
        self.piece_spacing = self.pieces_area_height // self.pieces_per_page
        
        # Calculate piece positions
        self.white_x = self.x + (self.width // 4) - (self.square_size // 2)
        self.black_x = self.x + (3 * self.width // 4) - (self.square_size // 2)

    def draw(self, screen):
        # Draw panel background
        pygame.draw.rect(screen, PANEL_COLOR, (self.x, self.y, self.width, self.height))
        
        # Draw navigation buttons
        prev_button_rect = pygame.Rect(
            self.x + self.button_margin,
            self.y + self.button_margin,
            self.button_width,
            self.button_height
        )
        next_button_rect = pygame.Rect(
            self.x + self.width - self.button_width - self.button_margin,
            self.y + self.button_margin,
            self.button_width,
            self.button_height
        )
        
        # Draw buttons
        pygame.draw.rect(screen, (200, 200, 200), prev_button_rect)
        pygame.draw.rect(screen, (200, 200, 200), next_button_rect)
        
        # Draw button text
        font = pygame.font.Font(None, 24)
        prev_text = font.render("Prev", True, (0, 0, 0))
        next_text = font.render("Next", True, (0, 0, 0))
        page_text = font.render(f"Page {self.current_page + 1}/{self.total_pages}", True, (0, 0, 0))
        
        screen.blit(prev_text, (prev_button_rect.centerx - prev_text.get_width()//2,
                               prev_button_rect.centery - prev_text.get_height()//2))
        screen.blit(next_text, (next_button_rect.centerx - next_text.get_width()//2,
                               next_button_rect.centery - next_text.get_height()//2))
        screen.blit(page_text, (self.x + self.width//2 - page_text.get_width()//2,
                               self.y + self.button_margin + self.button_height//2 - page_text.get_height()//2))
        
        # Draw column headers
        white_header = font.render("White", True, (0, 0, 0))
        black_header = font.render("Black", True, (0, 0, 0))
        header_y = self.y + 2 * (self.button_height + self.button_margin)
        
        screen.blit(white_header, (self.white_x + (self.square_size - white_header.get_width())//2, header_y))
        screen.blit(black_header, (self.black_x + (self.square_size - black_header.get_width())//2, header_y))
        
        # Draw pieces for current page
        start_idx = self.current_page * self.pieces_per_page
        end_idx = min(start_idx + self.pieces_per_page, len(self.piece_pairs))
        
        for i, (white_key, black_key) in enumerate(self.piece_pairs[start_idx:end_idx]):
            piece_y = header_y + 30 + (i * self.piece_spacing)
            
            # Draw white piece
            screen.blit(self.piece_images[white_key], (self.white_x, piece_y))
            # Draw black piece
            screen.blit(self.piece_images[black_key], (self.black_x, piece_y))

    def handle_click(self, pos):
        x, y = pos
        
        # Check if click is in panel
        if not (self.x <= x < self.x + self.width and self.y <= y < self.y + self.height):
            return None
            
        # Check navigation buttons
        button_y = self.y + self.button_margin
        prev_button_rect = pygame.Rect(
            self.x + self.button_margin,
            button_y,
            self.button_width,
            self.button_height
        )
        next_button_rect = pygame.Rect(
            self.x + self.width - self.button_width - self.button_margin,
            button_y,
            self.button_width,
            self.button_height
        )
        
        if prev_button_rect.collidepoint(x, y):
            self.current_page = (self.current_page - 1) % self.total_pages
            return None
        elif next_button_rect.collidepoint(x, y):
            self.current_page = (self.current_page + 1) % self.total_pages
            return None
            
        # Check piece clicks
        start_idx = self.current_page * self.pieces_per_page
        end_idx = min(start_idx + self.pieces_per_page, len(self.piece_pairs))
        header_y = self.y + 2 * (self.button_height + self.button_margin)
        
        for i, (white_key, black_key) in enumerate(self.piece_pairs[start_idx:end_idx]):
            piece_y = header_y + 30 + (i * self.piece_spacing)
            
            # Check white piece
            white_rect = pygame.Rect(self.white_x, piece_y, self.square_size, self.square_size)
            if white_rect.collidepoint(x, y):
                return white_key
                
            # Check black piece
            black_rect = pygame.Rect(self.black_x, piece_y, self.square_size, self.square_size)
            if black_rect.collidepoint(x, y):
                return black_key
                
        return None

class PresetMenu:
    def __init__(self, screen_width, screen_height):
        self.width = 300
        self.height = 400
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 32)
        self.visible = False
        self.presets = get_all_presets()
        self.buttons = []
        self.close_button = pygame.Rect(self.x + self.width - 30, self.y + 10, 20, 20)
        self.update_buttons()

    def update_buttons(self):
        self.buttons = []
        y_offset = self.y + 50
        for preset_name, preset in self.presets.items():
            text = self.font.render(preset['name'], True, TEXT_COLOR)
            button_rect = pygame.Rect(self.x + 10, y_offset, self.width - 20, 30)
            self.buttons.append((button_rect, preset_name, text))
            y_offset += 40

    def draw(self, screen):
        if not self.visible:
            return

        # Draw semi-transparent background
        s = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        screen.blit(s, (0, 0))

        # Draw menu background
        pygame.draw.rect(screen, SETTINGS_BAR_COLOR, self.rect)
        pygame.draw.rect(screen, TEXT_COLOR, self.rect, 2)

        # Draw title
        title = self.title_font.render("Select Preset", True, TEXT_COLOR)
        screen.blit(title, (self.x + (self.width - title.get_width()) // 2, self.y + 10))

        # Draw close button
        pygame.draw.rect(screen, BUTTON_COLOR, self.close_button)
        close_text = self.font.render("X", True, TEXT_COLOR)
        screen.blit(close_text, (self.close_button.centerx - close_text.get_width() // 2,
                                self.close_button.centery - close_text.get_height() // 2))

        # Draw buttons
        for button_rect, _, text in self.buttons:
            pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
            screen.blit(text, (button_rect.centerx - text.get_width() // 2,
                             button_rect.centery - text.get_height() // 2))

    def handle_click(self, pos):
        if not self.visible:
            return None

        # Check close button first
        if self.close_button.collidepoint(pos):
            self.visible = False
            return None

        for button_rect, preset_name, _ in self.buttons:
            if button_rect.collidepoint(pos):
                return preset_name
        return None 