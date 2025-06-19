from enum import Enum
from typing import Tuple, List


class MovementPattern:
    """Base class for movement patterns that can be combined to create piece movements."""

    @staticmethod
    def _is_valid_position(pos: Tuple[int, int], board_size: int) -> bool:
        """Check if a position is valid on the board."""
        row, col = pos
        return 0 <= row < board_size and 0 <= col < board_size

    @staticmethod
    def get_moves(pos: Tuple[int, int], patterns: List[Tuple[int, int]], board_size: int, direction: int, max_steps: int = None) -> List[Tuple[int, int]]:
        moves = []
        row, col = pos
        for row_dir, col_dir in patterns:
            dr = row_dir * direction
            dc = col_dir
            current_row, current_col = row + dr, col + dc
            steps = 0
            while (max_steps is None or steps < max_steps) and MovementPattern._is_valid_position((current_row, current_col), board_size):
                moves.append((current_row, current_col))
                current_row += dr
                current_col += dc
                steps += 1
        return moves

# Define common movement patterns
MOVEMENT_PATTERNS = {
    'ORTHOGONAL': [(-1, 0), (1, 0), (0, -1), (0, 1)],  # Up, down, left, right
    'DIAGONAL': [(-1, -1), (-1, 1), (1, -1), (1, 1)],  # All diagonals
    'KING': [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)],  # King moves
    'KNIGHT': [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)],  # L-shape
    'SHOGI_KNIGHT': [(-2, -1), (-2, 1)],  # L-shape Forward
    'FORWARD': [(-1, 0)],  # Forward only
    'FORWARD_AND_BACKWARD': [(-1, 0), (1, 0)],  # Forward and backward
    'FORWARD_DIAGONAL': [(-1, -1), (-1, 1)],  # Forward diagonals
    'FORWARD_LEFT_DIAGONAL': [(-1, -1)],  # Forward left diagonal
    'FORWARD_RIGHT_DIAGONAL': [(-1, 1)],  # Forward right diagonal
    'BACKWARD': [(1, 0)],  # Backward only
    'BACKWARD_DIAGONAL': [(1, -1), (1, 1)],  # Backward diagonals
    'BACKWARD_LEFT_DIAGONAL': [(1, -1)],  # Backward left diagonal
    'BACKWARD_RIGHT_DIAGONAL': [(1, 1)],  # Backward right diagonal
    'SIDE': [(0, -1), (0, 1)],  # Left and right only
    'LEFT_SIDE': [(0, -1)],  # Left side only
    'RIGHT_SIDE': [(0, 1)],  # Right side only
    'FORWARD_AND_SIDE': [(-1, 0), (0, -1), (0, 1)],  # Forward and sides
    'BACKWARD_AND_SIDE': [(1, 0), (0, -1), (0, 1)],  # Backward and sides
    'FORWARD_AND_DIAGONAL': [(-1, 0), (-1, -1), (-1, 1)],  # Forward and forward diagonals
    'BACKWARD_AND_DIAGONAL': [(1, 0), (1, -1), (1, 1)],  # Backward and backward diagonals

    'ROARING_DOG': [(-3, -3), (-3, 0), (-3, 3), (-3, 0), (0, -3), (3, 0)],  # Roaring Dog moves
    'FLYING_CAT': [(0, -3), (-3, -3), (-3, 0), (-3, 3), (0, 3)],  # Flying Cat moves
    'FLYING_DRAGON': [(-2, -2), (-2, 2), (2, 2), (2, -2)],  # Flying Dragon moves
    'FREE_EAGLE': [(-2, -2), (-3, -3), (-4, -4),
                   (-2, 0), (-3, 0),
                   (-2, 2), (-3, 3), (-4, 4),
                   (0, 2), (0, 3),
                   (2, 2), (3, 3),
                   (2, 0), (3, 0),
                   (2, -2), (3, -3),
                   (0, -2), (0, -3)],  # Free Eagle moves
    'GREAT_MASTER': [(-3, -3), (-3, 0), (-3, 3)],  # Great Master moves
    'GREAT_STAG': [(-2, -2), (-2, 2)],  # Great Stag moves
    'GREAT_TURTLE': [(-3, 0), (3, 0)],  # Great Turtle moves
    'HORNED_FALCON': [(-2, 0)],  # Horned Falcon moves
    'RUNNING_HORSE': [(2, -2), (2, 2)],  # Running Horse moves
    'KIRIN': [(0, -2), (0, 2)],  # Kirin moves
    'LION_DOG': [(-3, -3), (-3, 0), (-3, 3), (0, 3), (3, 3), (3, 0), (3, -3), (0, -3)],  # Lion Dog moves
    'LEFT_MOUNTAIN_EAGLE': [(-2, -2), (2, -2)],  # Left Mountain Eagle moves
    'RIGHT_MOUNTAIN_EAGLE': [(-2, 2), (2, 2)],  # Right Mountain Eagle moves
    'CENTAUR_MASTER': [(-2, -2), (-2, 0), (-2, 2), (2, 0)],  # Centaur Master moves
    'PHOENIX_MASTER': [(-3, -3), (-3, 3)],  # Phoenix Master moves
    'WOODEN_DOVE': [(-3, -3), (-4, -4), (-5, -5),
                    (-3, 3), (-4, 4), (-5, 5),
                    (3, -3), (4, -4), (5, -5),
                    (3, 3), (4, 4), (5, 5)],  # Wooden Dove moves
    'VICE_GENERAL': [(-2, 0), (2, 0), (-2, 0), (2, 0)],  # Vice General moves
}

class PieceColor(Enum):
    WHITE = 'White'
    BLACK = 'Black'

class PieceRank(Enum):
    KING = 1
    GREAT_GENERAL = 2
    VICE_GENERAL = 3
    GENERAL = 4
    OTHER = 5

class PieceType(Enum):
    PAWN = 'Pawn'
    KNIGHT = 'Knight'
    BISHOP = 'Bishop'
    ROOK = 'Rook'
    QUEEN = 'Queen'
    KING = 'King'
    GOLD_GENERAL = 'Gold_General'
    SILVER_GENERAL = 'Silver_General'
    SHOGI_KNIGHT = 'Shogi_Knight'
    LANCE = 'Lance'
    SHOGI_PAWN = 'Shogi_Pawn'
    DRAGON = 'Dragon'
    HORSE = 'Horse'
    ANGRY_BOAR = 'Angry_Boar'
    RUNNING_BEAR = 'Running_Bear'
    BLIND_BEAR = 'Blind_Bear'
    BEAST_CADET = 'Beast_Cadet'
    BUDDHIST_DEVIL = 'Buddhist_Devil'
    BEAR_SOLDIER = 'Bear_Soldier'
    BISHOP_GENERAL = 'Bishop_General'
    BLIND_DOG = 'Blind_Dog'
    BLUE_DRAGON = 'Blue_Dragon'
    BLIND_MONKEY = 'Blind_Monkey'
    BURNING_SOLDIER = 'Burning_Soldier'
    BEAST_OFFICER = 'Beast_Officer'
    BOAR_SOLDIER = 'Boar_Soldier'
    BLIND_TIGER = 'Blind_Tiger'
    COPPER_GENERAL = 'Copper_General'
    CAPRICORN = 'Capricorn'
    CHINESE_ROOSTER = 'Chinese_Rooster'
    CERAMIC_DOVE = 'Ceramic_Dove'
    CLOUD_EAGLE = 'Cloud_Eagle'
    CHICKEN_GENERAL = 'Chicken_General'
    CHARIOT_SOLDIER = 'Chariot_Soldier'
    STONE_CHARIOT = 'Stone_Chariot'
    FLYING_ROOSTER = 'Flying_Rooster'
    CLOUD_DRAGON = 'Cloud_Dragon'
    CLIMBING_MONKEY = 'Climbing_Monkey'
    CENTER_STANDARD = 'Center_Standard'
    CAPTIVE_OFFICER = 'Captive_Officer'
    PRINCE = 'Prince'
    COPPER_CHARIOT = 'Copper_Chariot'
    CAT_SWORD = 'Cat_Sword'
    CAPTIVE_CADET = 'Captive_Cadet'
    DOG = 'Dog'
    DRUNKEN_ELEPHANT = 'Drunken_Elephant'
    ROARING_DOG = 'Roaring_Dog'
    DRAGON_HORSE = 'Dragon_Horse'
    DRAGON_KING = 'Dragon_King'
    DONKEY = 'Donkey'
    FIRE_DEMON = 'Fire_Demon'
    DARK_SPIRIT = 'Dark_Spirit'
    DEVA = 'Deva'
    EARTH_GENERAL = 'Earth_General'
    ENCHANTED_BADGER = 'Enchanted_Badger'
    EARTH_CHARIOT = 'Earth_Chariot'
    EARTH_DRAGON = 'Earth_Dragon'
    FIERCE_EAGLE = 'Fierce_Eagle'
    SOARING_EAGLE = 'Soaring_Eagle'
    EASTERN_BARBARIAN = 'Eastern_Barbarian'
    EVIL_WOLF = 'Evil_Wolf'
    FIRE_GENERAL = 'Fire_General'
    FLYING_CAT = 'Flying_Cat'
    FLYING_DRAGON = 'Flying_Dragon'
    FREE_EAGLE = 'Free_Eagle'
    FRAGRANT_ELEPHANT = 'Fragrant_Elephant'
    FLYING_HORSE = 'Flying_Horse'
    FIRE_DRAGON = 'Fire_Dragon'
    FEROCIOUS_LEOPARD = 'Ferocious_Leopard'
    FOREST_DEMON = 'Forest_Demon'
    FREE_PUP = 'Free_Pup'
    FREE_DEMON = 'Free_Demon'
    FLYING_SWALLOW = 'Flying_Swallow'
    FREE_DREAM_EATER = 'Free_Dream_Eater'
    FLYING_GOOSE = 'Flying_Goose'
    GO_BETWEEN = 'Go_Between'
    GOLD_CHARIOT = 'Gold_Chariot'
    GREAT_DRAGON = 'Great_Dragon'
    GREAT_STANDARD = 'Great_Standard'
    GREAT_GENERAL = 'Great_General'
    GOLDEN_DEER = 'Golden_Deer'
    GREAT_MASTER = 'Great_Master'
    WOOD_GENERAL = 'Wood_General'
    GOLDEN_BIRD = 'Golden_Bird'
    GREAT_DOVE = 'Great_Dove'
    GREAT_STAG = 'Great_Stag'
    GREAT_TURTLE = 'Great_Turtle'
    GUARDIAN_OF_THE_GODS = 'Guardian_Of_The_Gods'
    HORSE_GENERAL = 'Horse_General'
    HOWLING_DOG = 'Howling_Dog'
    RAMS_HEAD_SOLDIER = 'Rams_Head_Soldier'
    HORNFED_FALCON = 'Horned_Falcon'
    HOOK_MOVER = 'Hook_Mover'
    HORSEMAN = 'Horseman'
    RUNNING_HORSE = 'Running_Horse'
    HORSE_SOLDIER = 'Horse_Soldier'
    IRON_GENERAL = 'Iron_General'
    SHOGI_KING = 'Sogi_King'
    KIRIN_MASTER = 'Kirin_Master'
    KIRIN = 'Kirin'
    LONGBOW_SOLDIER = 'Longbow_Soldier'
    LEFT_CHARIOT = 'Left_Chariot'
    LION_DOG = 'Lion_Dog'
    LEFT_DRAGON = 'Left_Dragon'
    LEFT_GENERAL = 'Left_General'
    LIBERATED_HORSE = 'Liberated_Horse'
    LION_HAWK = 'Lion_Hawk'
    LITTLE_TURTLE = 'Little_Turtle'
    LION = 'Lion'
    LONG_NOSED_GOBLIN = 'Long_Nosed_Goblin'
    LEOPARD_SOLDIER = 'Leopard_Soldier'
    LITTLE_STANDARD = 'Little_Standard'
    LEFT_TIGER = 'Left_Tiger'
    MOUNTAIN_GENERAL = 'Mountain_General'
    MOUNTAIN_FALCON = 'Mountain_Falcon'
    SIDE_MONKEY = 'Side_Monkey'
    LEFT_MOUNTAIN_EAGLE = 'Left_Mountain_Eagle'
    RIGHT_MOUNTAIN_EAGLE = 'Right_Mountain_Eagle'
    MOUNTAIN_STAG = 'Mountain_Stag'
    CENTAUR_MASTER = 'Centaur_Master'
    NORTHERN_BARBARIAN = 'Northern_Barbarian'
    NEIGHBORING_KING = 'Neighboring_King'
    VIOLENT_WOLF = 'Violent_Wolf'
    OX_GENERAL = 'Ox_General'
    OXCART = 'Oxcart'
    OLD_KITE = 'Old_Kite'
    OLD_MONKEY = 'Old_Monkey'
    OLD_RAT = 'Old_Rat'
    OX_SOLDIER = 'Ox_Soldier'
    SWOOPING_OWL = 'Swooping_Owl'
    FLYING_OX = 'Flying_Ox'
    PEACOCK = 'Peacock'
    PUP_GENERAL = 'Pup_General'
    PHOENIX = 'Phoenix'
    PIG_GENERAL = 'Pig_General'
    PHOENIX_MASTER = 'Phoenix_Master'
    PRANCING_STAG = 'Prancing_Stag'
    POISONOUS_SNAKE = 'Poisonous_Snake'
    RAIN_DRAGON = 'Rain_Dragon'
    RUSHING_BIRD = 'Rushing_Bird'
    RIGHT_CHARIOT = 'Right_Chariot'
    RECLINING_DRAGON = 'Reclining_Dragon'
    RIVER_GENERAL = 'River_General'
    RIGHT_GENERAL = 'Right_General'
    RUNNING_CHARIOT = 'Running_Chariot'
    RIGHT_DRAGON = 'Right_Dragon'
    ROC_MASTER = 'Roc_Master'
    RUNNING_STAG = 'Running_Stag'
    ROOK_GENERAL = 'Rook_General'
    RUNNING_PUP = 'Running_Pup'
    RUNNING_RABBIT = 'Running_Rabbit'
    REAR_STANDARD = 'Rear_Standard'
    RUNNING_TIGER = 'Running_Tiger'
    RUNNING_SERPENT = 'Running_Serpent'
    REVERSE_CHARIOT = 'Reverse_Chariot'
    RUNNING_WOLF = 'Running_Wolf'
    SIDE_BOAR = 'Side_Boar'
    CROSSBOW_SOLDIER = 'Crossbow_Soldier'
    FRONT_STANDARD = 'Front_Standard'
    SWORD_SOLDIER = 'Sword_Soldier'
    SIDE_FLYER = 'Side_Flyer'
    STONE_GENERAL = 'Stone_General'
    SIDE_DRAGON = 'Side_Dragon'
    SIDE_SOLDIER = 'Side_Soldier'
    SIDE_MOVER = 'Side_Mover'
    COILED_SERPENT = 'Coiled_Serpent'
    SOLDIER = 'Soldier'
    SPEAR_SOLDIER = 'Spear_Soldier'
    SQUARE_MOVER = 'Square_Mover'
    SILVER_RABBIT = 'Silver_Rabbit'
    SIDE_SERPENT = 'Side_Serpent'
    STRUTTING_CROW = 'Strutting_Crow'
    SOUTHERN_BARBARIAN = 'Southern_Barbarian'
    SILVER_CHARIOT = 'Silver_Chariot'
    SWALLOWS_WINGS = 'Swallows_Wings'
    SIDE_OX = 'Side_Ox'
    TILE_GENERAL = 'Tile_General'
    TILE_CHARIOT = 'Tile_Chariot'
    TURTLE_DOVE = 'Turtle_Dove'
    TREACHEROUS_FOX = 'Treacherous_Fox'
    SAVAGE_TIGER = 'Savage_Tiger'
    TURTLE_SNAKE = 'Turtle_Snake'
    RIGHT_TIGER = 'Right_Tiger'
    VIOLENT_BEAR = 'Violent_Bear'
    VIOLENT_DRAGON = 'Violent_Dragon'
    VERTICAL_BEAR = 'Vertical_Bear'
    VICE_GENERAL = 'Vice_General'
    VERTICAL_HORSE = 'Vertical_Horse'
    VERMILION_SPARROW = 'Vermilion_Sparrow'
    VERTICAL_LEOPARD = 'Vertical_Leopard'
    VERTICAL_MOVER = 'Vertical_Mover'
    VIOLENT_OX = 'Violent_Ox'
    VERTICAL_PUP = 'Vertical_Pup'
    VERTICAL_SOLDIER = 'Vertical_Soldier'
    VIOLENT_STAG = 'Violent_Stag'
    VERTICAL_TIGER = 'Vertical_Tiger'
    VERTICAL_WOLF = 'Vertical_Wolf'
    WHALE = 'Whale'
    WATER_DRAGON = 'Water_Dragon'
    WATER_BUFFALO = 'Water_Buffalo'
    WOOD_CHARIOT = 'Wood_Chariot'
    WIND_DRAGON = 'Wind_Dragon'
    WHITE_ELEPHANT = 'White_Elephant'
    SIDE_WOLF = 'Side_Wolf'
    WATER_GENERAL = 'Water_General'
    WHITE_HORSE = 'White_Horse'
    WOODLAND_DEMON = 'Woodland_Demon'
    WIND_GENERAL = 'Wind_General'
    WOODEN_DOVE = 'Wooden_Dove'
    WRESTLER = 'Wrestler'
    WESTERN_BARBARIAN = 'Western_Barbarian'
    WHITE_TIGER = 'White_Tiger'
    YAKSHA = 'Yaksha'

class PieceKey:
    def __init__(self, color, piece_type, rank):
        self.color = color  # 'White' or 'Black'
        self.piece_type = piece_type  # 'Pawn', 'Knight', etc
        self.rank = rank  # 'King', 'Great_General', etc

    @classmethod
    def from_string(cls, key_str):
        # For backward compatibility, assume rank 1 if not specified
        parts = key_str.split('_', 2)
        if len(parts) >= 3:
            return cls(parts[0], parts[1], int(parts[2]))
        else:
            return cls(parts[0], parts[1], 1)

    def __str__(self):
        return f"{self.color}{self.piece_type}{self.rank}"


class Piece:
    def __init__(self, piece_type: str, color: str, rank: int = 1):
        self.piece_type = piece_type
        self.color = color
        self.rank = rank  # Numerical rank (1-10, 1=lowest, 10=highest)
        self.symbol = color + '_' + piece_type  # Keep image filename without rank
        self.direction = -1 if color == 'White' else 1

    def get_legal_moves_with_info(self, pos: Tuple[int, int], board_size: int) -> List[Tuple[Tuple[int, int], bool]]:
        """Get all legal moves for this piece from the given position with jump information.
        Returns a list of tuples: (position, can_jump_over_pieces)"""
        # Map piece types to their movement patterns with jump info
        movement_patterns = {
            # Standard chess pieces
            'Pawn': lambda p, b: [(move, False) for move in self._get_pawn_moves(p, b)],
            'Knight': lambda p, b: [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['KNIGHT'], b, self.direction, max_steps=1)],
            'Bishop': lambda p, b: (    
                [(move, ('origin', 1)) for move in MovementPattern.get_moves(p, [(-3, -3)], b, self.direction, max_steps=1)] +
                [(move, ('origin', 2)) for move in MovementPattern.get_moves(p, [(-3, 3)], b, self.direction, max_steps=1)] +
                [(move, ('direction', 1)) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_LEFT_DIAGONAL'], b, self.direction)] +
                [(move, ('direction', 2)) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_RIGHT_DIAGONAL'], b, self.direction)]
            ),
            'Rook': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction)],
            'Queen': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['KING'], b, self.direction)],
            'King': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['KING'], b, self.direction, max_steps=1)],
            
            # Shogi pieces
            'Gold_General': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL']+MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction, max_steps=1)],
            'Silver_General': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction, max_steps=1)],
            'Shogi_Knight': lambda p, b: [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SHOGI_KNIGHT'], b, self.direction, max_steps=1)],
            'Lance': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction)],
            'Shogi_Pawn': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction,  max_steps=1)],
            'Dragon_General': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction,  max_steps=1)],
            'Horse_General': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction,  max_steps=1)],
            
            # Taikyoku pieces
            'Angry_Boar': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_SIDE'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=2)]
            ),
            'Running_Bear': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction)]
            ),
            'Blind_Bear': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'] + MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Beast_Cadet': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_SIDE']+MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction,  max_steps=2)]
            ),
            'Buddhist_Devil': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_AND_SIDE'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=3)]
            ),
            'Bear_Soldier': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction)]
            ),
            'Bishop_General': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction)],
            'Blind_Dog': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_AND_SIDE']+MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=1)],
            'Blue_Dragon': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'] + MOVEMENT_PATTERNS['BACKWARD']+MOVEMENT_PATTERNS['FORWARD_RIGHT_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=2)]
            ),
            'Blind_Monkey': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE']+MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction,  max_steps=1)],
            'Burning_Soldier': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=3)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=5)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction,  max_steps=7)]
            ),
            'Beast_Officer': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL'], b, self.direction,  max_steps=3)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=2)]
            ),
            'Boar_Soldier': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL'], b, self.direction)]
            ),
            'Blind_Tiger': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD']+MOVEMENT_PATTERNS['SIDE']+MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction,  max_steps=1)],
            'Copper_General': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)],
            'Capricorn': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction,  max_steps=1)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction)]
             ),
            'Chinese_Rooster': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_AND_SIDE']+MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=1)],
            'Ceramic_Dove': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction)]
            ),
            'Cloud_Eagle': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=3)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=1)]
            ),
            'Chicken_General': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKEARD_DIAGONAL'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction,  max_steps=4)]
            ),
            'Chariot_Soldier': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD']+MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=2)]
            ),
            'Stone_Chariot': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Flying_Rooster': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=1)],
            'Cloud_Dragon': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'] + MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=1)]
            ),
            'Climbing_Monkey': lambda p, b: MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1),
            'Center_Standard': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction,  max_steps=3)]
            ),
            'Captive_Officer': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_SIDE'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction,  max_steps=3)]
            ),
            'Prince': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['KING'], b, self.direction,  max_steps=1)],
            'Copper_Chariot': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=3)]
            ),
            'Cat_Sword': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction,  max_steps=1)],
            'Captive_Cadet': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_SIDE']+MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction,  max_steps=3)],
            'Dog': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL'], b, self.direction,  max_steps=1)],
            'Drunken_Elephant': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_SIDE']+MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction,  max_steps=1)],
            'Roaring_Dog': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'] + MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction,  max_steps=3)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ROARING_DOG'], b, self.direction)]
                ),
            'Dragon_Horse': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Dragon_King': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Donkey': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction,  max_steps=2)],
            'Fire_Demon': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL']+MOVEMENT_PATTERNS['SIDE'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=2)]
            ),
            'Dark_Spirit': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL']+MOVEMENT_PATTERNS['BACKWARD_DIAGONAL']+MOVEMENT_PATTERNS['FORWARD_RIGHT_DIAGONAL'], b, self.direction,  max_steps=1)],
            'Deva': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL']+MOVEMENT_PATTERNS['BACKWARD_DIAGONAL']+MOVEMENT_PATTERNS['FORWARD_LEFT_DIAGONAL'], b, self.direction,  max_steps=1)],
            'Earth_General': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)],
            'Enchanted_Badger': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction,  max_steps=2)],
            'Earth_Chariot': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=1)]
            ),
            'Earth_Dragon': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction)]
            ), #This piece is different in Japanese
            'Fierce_Eagle': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_SIDE'], b, self.direction,  max_steps=1)]
            ),
            'Soaring_Eagle': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['KING'], b, self.direction)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=2)]
            ),
            'Eastern_Barbarian': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE']+MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Evil_Wolf': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_SIDE']+MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=1)],
            'Fire_General': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=3)]
            ),
            'Flying_Cat': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL'], b, self.direction,  max_steps=1)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FLYING_CAT'], b, self.direction,  max_steps=1)]
            ),
            'Flying_Dragon': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['KING'], b, self.direction,  max_steps=1)]
            ),
            'Free_Eagle': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['KING'], b, self.direction)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FREE_EAGLE'], b, self.direction,  max_steps=1)]
            ),
            'Fragrant_Elephant': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['KING'], b, self.direction,  max_steps=2)],
            'Flying_Horse': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction,  max_steps=2)],
            'Fire_Dragon': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=4)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction,  max_steps=2)]
            ),
            'Ferocious_Leopard': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_AND_DIAGONAL'], b, self.direction,  max_steps=1)],
            'Forest_Demon': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_SIDE'], b, self.direction,  max_steps=3)]
            ),
            'Free_Pup': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL'] + MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Free_Demon': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL']+ MOVEMENT_PATTERNS['RIGHT_SIDE'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=5)]
            ), # Free Demon is different in Japanese
            'Flying_Swallow': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['Backward'], b, self.direction,  max_steps=1)]
            ),
            'Free_Dream_Eater': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL']+MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=5)]
            ),
            'Flying_Goose': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)],
            'Go_Between': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)],
            'Gold_Chariot': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Great_Dragon': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=3)]
            ),
            'Great_Standard': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL']+MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction,  max_steps=3)]
            ),
            'Great_General': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['KING'], b, self.direction)],
            'Golden_Deer': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction,  max_steps=2)]
            ),
            'Great_Master': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE']+MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction,  max_steps=5)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['GREAT_MASTER'], b, self.direction,  max_steps=1)]
            ),
            'Wood_General': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=2)],
            'Golden_Bird': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL'], b, self.direction)], #Golden Bird requires fixing jumping
            'Great_Dove': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction,  max_steps=3)]
            ),
            'Great_Stag': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction,  max_steps=2)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['GREAT_STAG'], b, self.direction,  max_steps=1)]
            ),
            'Great_Turtle': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL']+MOVEMENT_PATTERNS['FORWARD_AND_BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=3)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['GREAT_TURTLE'], b, self.direction,  max_steps=1)]
            ),
            'Guardian_Of_The_Gods': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction,  max_steps=3)],
            'Horse_General': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction,  max_steps=3)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)]
            ),
            'Howling_Dog': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)],
            ),
            'Rams_Head_Soldier': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)],
            ),
            'Horned_Falcon': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['KING'], b, self.direction)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['HORNED_FALCON'], b, self.direction,  max_steps=1)]
            ),
            'Hook_Mover': lambda p, b: [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction)],
            'Horseman': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=2)],
            ),
            'Running_Horse': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['RUNNING_HORSE'], b, self.direction,  max_steps=1)]
            ),
            'Horse_Soldier': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=3)],
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)],
            ),
            'Iron_General': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL'], b, self.direction,  max_steps=1)],
            'Shogi_King': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['KING'], b, self.direction,  max_steps=2)],
            'Kirin_Master': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL']+MOVEMENT_PATTERNS['FORWARD_AND_BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=3)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['GREAT_TURTLE'], b, self.direction,  max_steps=1)]
            ),
            'Kirin': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction,  max_steps=1)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['KIRIN'], b, self.direction,  max_steps=1)]
            ),
            'Longbow_Soldier': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=3)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=2)]
            ),
            'Left_Chariot': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['FORWARD_LEFT_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_RIGHT_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['LEFT_SIDE'], b, self.direction,  max_steps=1)],
            ),
            'Lion_Dog': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['KING'], b, self.direction)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['LION_DOG'], b, self.direction,  max_steps=1)]
            ),
            'Left_Dragon': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['RIGHT_SIDE'] + MOVEMENT_PATTERNS['FORWARD_RIGHT_DIAGONAL']+ MOVEMENT_PATTERNS['BACKWARD_RIGHT_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['LEFT_SIDE'], b, self.direction,  max_steps=2)]
            ),
            'Left_General': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['KING'], b, self.direction,  max_steps=1)],
            'Liberated_Horse': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=1)]
            ),
            'Lion_Hawk': lambda p, b: (
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['KING'], b, self.direction,  max_steps=2)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['KNIGHT'], b, self.direction,  max_steps=1)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FLYING_DRAGON'], b, self.direction,  max_steps=1)]
            ),
            'Little_Turtle': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL']+MOVEMENT_PATTERNS['FORWARD_AND_BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=2)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['KIRIN'], b, self.direction,  max_steps=1)]
            ),
            'Lion': lambda p, b: (
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['KING'], b, self.direction,  max_steps=2)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['KNIGHT'], b, self.direction,  max_steps=1)]
            ),
            'Long_Nosed_Goblin': lambda p, b: [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction)],
            'Leopard_Soldier': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=2)]
            ),
            'Little_Standard': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Left_Tiger': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['RIGHT_SIDE']+MOVEMENT_PATTERNS['FORWARD_RIGHT_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_RIGHT_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_LEFT_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_LEFT_DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Mountain_General': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=3)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)]
            ),
            'Mountain_Falcon': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD']+MOVEMENT_PATTERNS['SIDE'], b, self.direction)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['HORNED_FALCON'], b, self.direction,  max_steps=1)]
            ),
            'Side_Monkey': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)]
            ),
            'Left_Mountain_Eagle': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL']+MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_LEFT_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_RIGHT_DIAGONAL'], b, self.direction,  max_steps=2)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['LEFT_MOUNTAIN_EAGLE'], b, self.direction,  max_steps=1)]
            ),
            'Right_Mountain_Eagle': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL']+MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_RIGHT_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_LEFT_DIAGONAL'], b, self.direction,  max_steps=2)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['RIGHT_MOUNTAIN_EAGLE'], b, self.direction,  max_steps=1)]
            ),
            'Mountain_Stag': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=3)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=4)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=2)]
            ),
            'Centaur_Master': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE']+MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction,  max_steps=3)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['CENTAUR_MASTER'], b, self.direction,  max_steps=1)]
            ),
            'Northern_Barbarian': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=2)]
            ),
            'Neighboring_King': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL']+MOVEMENT_PATTERNS['FORWARD_AND_SIDE'], b, self.direction,  max_steps=1)],
            'Violent_Wolf': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD']+MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=1)],
            'Ox_General': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction,  max_steps=3)]
            ),
            'Oxcart': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction)],
            'Old_Kite': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=1)]
            ),
            'Old_Monkey': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_AND_DIAGONAL'], b, self.direction,  max_steps=1)],
            'Old_Rat': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD_AND_DIAGONAL'], b, self.direction,  max_steps=1)],
            'Ox_Soldier': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=3)]
            ),
            'Swooping_Owl': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction,  max_steps=1)],
            'Flying_Ox': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_AND_DIAGONAL'], b, self.direction)],
            'Peacock': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction,  max_steps = 2)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction)]
            ),
            'Pup_General': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction,  max_steps=4)]
            ),
            'Phoenix': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction,  max_steps=1)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FLYING_DRAGON'], b, self.direction,  max_steps=1)]
            ),
            'Pig_General': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=4)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=2)]
            ),
            'Phoenix_Master': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL']+MOVEMENT_PATTERNS['FORWARD_AND_BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=3)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['PHOENIX_MASTER'], b, self.direction,  max_steps=1)]
            ),
            'Prancing_Stag': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=2)]
            ),
            'Poisonous_Snake': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_SIDE'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)]
            ),
            'Rain_Dragon': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE']+MOVEMENT_PATTERNS['BACKWARD_AND_DIAGONAL'], b, self.direction)]
            ),
            'Rushing_Bird': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL']+MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=1)]
            ),
            'Right_Chariot': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['FORWARD_RIGHT_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_LEFT_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['RIGHT_SIDE'], b, self.direction,  max_steps=1)]
            ),
            'Reclining_Dragon': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction,  max_steps=1)],
            'River_General': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction,  max_steps=3)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)]
            ),
            'Right_General': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['KING'], b, self.direction,  max_steps=1)],
            'Running_Chariot': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction)],
            'Right_Dragon': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_LEFT_DIAGONAL'] + MOVEMENT_PATTERNS['LEFT_SIDE']+MOVEMENT_PATTERNS['BACKWARD_LEFT_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['RIGHT_SIDE'], b, self.direction,  max_steps=2)]
            ),
            'Roc_Master': lambda p, b: (
                # For White
                ([
                    # Jump to (-3, -3)
                    ((p[0] - 3, p[1] - 3), True)
                ] if MovementPattern._is_valid_position((p[0] - 3, p[1] - 3), b, self.direction) else set()
                ) +
                ([
                    # Jump to (-3, 3)
                    ((p[0] - 3, p[1] + 3), True)
                ] if MovementPattern._is_valid_position((p[0] - 3, p[1] + 3), b, self.direction) else set()
                ) +
                # From each jump destination, continue along the same diagonal
                set().union(*[[
                    ((jump_pos[0] + step * d[0], jump_pos[1] + step * d[1]), False)
                    for step in range(1, b, self.direction)
                    if MovementPattern._is_valid_position((jump_pos[0] + step * d[0], jump_pos[1] + step * d[1]), b, self.direction)
                ]
                for d, jump_pos in [
                    ((-1, -1), (p[0] - 3, p[1] - 3)),
                    ((-1, 1), (p[0] - 3, p[1] + 3))
                ]
                if MovementPattern._is_valid_position(jump_pos, b, self.direction)
            ]))
            if self.color == 'White' else (
                # For Black
                ([
                    # Jump to (3, -3)
                    ((p[0] + 3, p[1] - 3), True)
                ] if MovementPattern._is_valid_position((p[0] + 3, p[1] - 3), b, self.direction) else set()
                ) +
                ([
                    # Jump to (3, 3)
                    ((p[0] + 3, p[1] + 3), True)
                ] if MovementPattern._is_valid_position((p[0] + 3, p[1] + 3), b, self.direction) else set()
                ) +
                set().union(*[[
                    ((jump_pos[0] + step * d[0], jump_pos[1] + step * d[1]), False)
                    for step in range(1, b, self.direction)
                    if MovementPattern._is_valid_position((jump_pos[0] + step * d[0], jump_pos[1] + step * d[1]), b, self.direction)
                ]
                for d, jump_pos in [
                    ((1, -1), (p[0] + 3, p[1] - 3)),
                    ((1, 1), (p[0] + 3, p[1] + 3))
                ]
                if MovementPattern._is_valid_position(jump_pos, b, self.direction)
            ]) +
            [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_BACKWARD'], b, self.direction)] +
            [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_DIAGONAL']+MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=6)]
            ),
            'Running_Stag': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=2)]
            ),
            'Rook_General': lambda p, b: [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction)],
            'Running_Pup': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=1)]
            ),
            'Running_Rabbit': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_AND_DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Rear_Standard': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction,  max_steps=2)]
            ),
            'Running_Tiger': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=2)]
            ),
            'Running_Serpent': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=1)]
            ),
            'Reverse_Chariot': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)],
            'Running_Wolf': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction,  max_steps=1)]
            ),
            'Side_Boar': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Crossbow_Soldier': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction,  max_steps=5)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=3)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)]
            ),
            'Front_Standard': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction,  max_steps=3)]
            ),
            'Sword_Soldier': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)],
            'Side_Flyer': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Stone_General': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=1)],
            'Side_Dragon': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'] + MOVEMENT_PATTERNS['SIDE'], b, self.direction)],
            'Side_Soldier': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)]
            ),
            'Side_Mover': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)]
            ),
            'Coiled_Serpent': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD_AND_DIAGONAL'], b, self.direction)],
            'Soldier': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction)],
            'Spear_Soldier': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)]
            ),
            'Square_Mover': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction)],
            'Silver_Rabbit': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction)]
            ),
            'Side_Serpent': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction,  max_steps=3)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)]
            ),
            'Strutting_Crow': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction,  max_steps=1)],
            'Southern_Barbarian': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=2)]
            ),
            'Silver_Chariot': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Swallows_Wings': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)]
            ),
            'Side_Ox': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_RIGHT_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_LEFT_DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Tile_General': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)],
            'Tile_Chariot': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_RIGHT_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_LEFT_DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Turtle_Dove': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=5)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_AND_SIDE'], b, self.direction,  max_steps=1)]
            ),
            'Treacherous_Fox': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_AND_DIAGONAL'], b, self.direction)],
            'Savage_Tiger': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction)],
            'Turtle_Snake': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_RIGHT_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_LEFT_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['FORWARD_LEFT_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD']+MOVEMENT_PATTERNS['BACKWARD_RIGHT_DIAGONAL']+MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=1)]
            ),
            'Right_Tiger': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_LEFT_DIAGONAL']+MOVEMENT_PATTERNS['LEFT_SIDE']+MOVEMENT_PATTERNS['BACKWARD_LEFT_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_RIGHT_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_RIGHT_DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Violent_Bear': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_SIDE'], b, self.direction,  max_steps=1)]
            ),
            'Violent_Dragon': lambda p, b: (
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction,  max_steps=2)]
            ),
            'Vertical_Bear': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=2)]
            ),
            'Vice_General': lambda p, b: (
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['VICE_GENERAL'], b, self.direction,  max_steps=1)]
            ),
            'Vertical_Horse': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD']+MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Vermilion_Sparrow': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_LEFT_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_RIGHT_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL']+MOVEMENT_PATTERNS['FORWARD_RIGHT_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_LEFT_DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Vertical_Leopard': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD']+MOVEMENT_PATTERNS['SIDE']+MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Vertical_Mover': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=1)]
            ),
            'Violent_Ox': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD']+MOVEMENT_PATTERNS['FORWARD'], b, self.direction,  max_steps=1)]
            ),
            'Vertical_Pup': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_AND_DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Vertical_Soldier': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=2)]
            ),
            'Violent_Stag': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction)],
            'Vertical_Tiger': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=2)]
            ),
            'Vertical_Wolf': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=3)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=1)]
            ),
            'Whale': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD_AND_DIAGONAL'], b, self.direction)],
            'Water_Dragon': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_DIAGONAL'], b, self.direction,  max_steps=4)]
            ),
            'Water_Buffalo': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL']+MOVEMENT_PATTERNS['SIDE'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=2)]
            ),
            'Wood_Chariot': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_LEFT_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_RIGHT_DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Wind_Dragon': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'] + MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_RIGHT_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD_LEFT_DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'White_Elephant': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['KING'], b, self.direction,  max_steps=2)],
            'Side_Wolf': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_LEFT_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD_RIGHT_DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Water_General': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=3)]
            ),
            'White_Horse': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)],
            'Woodland_Demon': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_AND_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=2)]
            ),
            'Wind_General': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD'], b, self.direction,  max_steps=3)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['BACKWARD']+MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'Wooden_Dove': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['ORTHOGONAL'], b, self.direction,  max_steps=2)] +
                [(move, True) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['WOODEN_DOVE'], b, self.direction,  max_steps=1)]
            ),
            'Wrestler': lambda p, b: [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['DIAGONAL'], b, self.direction,  max_steps=3)],
            'Western_Barbarian': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=2)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE']+MOVEMENT_PATTERNS['FORWARD_DIAGONAL'], b, self.direction,  max_steps=1)]
            ),
            'White_Tiger': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE']+MOVEMENT_PATTERNS['FORWARD_LEFT_DIAGONAL'], b, self.direction)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=2)]
            ),
            'Yaksha': lambda p, b: (
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['SIDE'], b, self.direction,  max_steps=3)] +
                [(move, False) for move in MovementPattern.get_moves(p, MOVEMENT_PATTERNS['FORWARD_DIAGONAL']+MOVEMENT_PATTERNS['BACKWARD'], b, self.direction,  max_steps=1)]
            ),
        }
        
        # Get the movement function for this piece type
        movement_function = movement_patterns.get(self.piece_type)
        if movement_function:
            return movement_function(pos, board_size)
        return list()

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


# Factory function to create pieces
def create_piece(piece_type: str, color: str, rank: int = 1) -> Piece:
    """Create a new piece of the given type and color."""
    return Piece(piece_type, color, rank)


# Dictionary of all available pieces
AVAILABLE_PIECES = {
    'White_Pawn':           (PieceType.PAWN, PieceColor.WHITE, PieceRank.OTHER),
    'White_Knight':         (PieceType.KNIGHT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Bishop':         (PieceType.BISHOP, PieceColor.WHITE, PieceRank.OTHER),
    'White_Rook':           (PieceType.ROOK, PieceColor.WHITE, PieceRank.OTHER),
    'White_Queen':          (PieceType.QUEEN, PieceColor.WHITE, PieceRank.OTHER),
    'White_King':           (PieceType.KING, PieceColor.WHITE, PieceRank.KING),
    'White_Gold_General':   (PieceType.GOLD_GENERAL, PieceColor.WHITE, PieceRank.OTHER),
    'White_Silver_General': (PieceType.SILVER_GENERAL, PieceColor.WHITE, PieceRank.OTHER),
    'White_Shogi_Knight':   (PieceType.SHOGI_KNIGHT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Lance':          (PieceType.LANCE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Shogi_Pawn':     (PieceType.SHOGI_PAWN, PieceColor.WHITE, PieceRank.OTHER),
    'White_Dragon':         (PieceType.DRAGON, PieceColor.WHITE, PieceRank.OTHER),
    'White_Horse':  (PieceType.HORSE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Angry_Boar':     (PieceType.ANGRY_BOAR, PieceColor.WHITE, PieceRank.OTHER),
    'White_Running_Bear':   (PieceType.RUNNING_BEAR, PieceColor.WHITE, PieceRank.OTHER),
    'White_Blind_Bear':     (PieceType.BLIND_BEAR, PieceColor.WHITE, PieceRank.OTHER),
    'White_Beast_Cadet':    (PieceType.BEAST_CADET, PieceColor.WHITE, PieceRank.OTHER),
    'White_Buddhist_Devil': (PieceType.BUDDHIST_DEVIL, PieceColor.WHITE, PieceRank.OTHER),
    'White_Bear_Soldier':   (PieceType.BEAR_SOLDIER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Bishop_General': (PieceType.BISHOP_GENERAL, PieceColor.WHITE, PieceRank.GENERAL),
    'White_Blind_Dog':      (PieceType.BLIND_DOG, PieceColor.WHITE, PieceRank.OTHER),
    'White_Blue_Dragon':    (PieceType.BLUE_DRAGON, PieceColor.WHITE, PieceRank.OTHER),
    'White_Blind_Monkey':   (PieceType.BLIND_MONKEY, PieceColor.WHITE, PieceRank.OTHER),
    'White_Burning_Soldier': (PieceType.BURNING_SOLDIER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Beast_Officer':  (PieceType.BEAST_OFFICER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Boar_Soldier':   (PieceType.BOAR_SOLDIER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Blind_Tiger':    (PieceType.BLIND_TIGER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Copper_General': (PieceType.COPPER_GENERAL, PieceColor.WHITE, PieceRank.OTHER),
    'White_Capricorn':      (PieceType.CAPRICORN, PieceColor.WHITE, PieceRank.OTHER),
    'White_Chinese_Rooster': (PieceType.CHINESE_ROOSTER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Ceramic_Dove':   (PieceType.CERAMIC_DOVE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Cloud_Eagle':    (PieceType.CLOUD_EAGLE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Chicken_General': (PieceType.CHICKEN_GENERAL, PieceColor.WHITE, PieceRank.OTHER),
    'White_Chariot_Soldier': (PieceType.CHARIOT_SOLDIER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Stone_Chariot':  (PieceType.STONE_CHARIOT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Flying_Rooster': (PieceType.FLYING_ROOSTER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Cloud_Dragon':   (PieceType.CLOUD_DRAGON, PieceColor.WHITE, PieceRank.OTHER),
    'White_Climbing_Monkey': (PieceType.CLIMBING_MONKEY, PieceColor.WHITE, PieceRank.OTHER),
    'White_Center_Standard': (PieceType.CENTER_STANDARD, PieceColor.WHITE, PieceRank.OTHER),
    'White_Captive_Officer': (PieceType.CAPTIVE_OFFICER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Prince':         (PieceType.PRINCE, PieceColor.WHITE, PieceRank.KING),
    'White_Copper_Chariot': (PieceType.COPPER_CHARIOT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Cat_Sword':      (PieceType.CAT_SWORD, PieceColor.WHITE, PieceRank.OTHER),
    'White_Captive_Cadet':  (PieceType.CAPTIVE_CADET, PieceColor.WHITE, PieceRank.OTHER),
    'White_Dog':            (PieceType.DOG, PieceColor.WHITE, PieceRank.OTHER),
    'White_Drunken_Elephant': (PieceType.DRUNKEN_ELEPHANT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Roaring_Dog':    (PieceType.ROARING_DOG, PieceColor.WHITE, PieceRank.OTHER),
    'White_Dragon_Horse':   (PieceType.DRAGON_HORSE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Dragon_King':    (PieceType.DRAGON_KING, PieceColor.WHITE, PieceRank.OTHER),
    'White_Donkey':         (PieceType.DONKEY, PieceColor.WHITE, PieceRank.OTHER),
    'White_Fire_Demon':     (PieceType.FIRE_DEMON, PieceColor.WHITE, PieceRank.OTHER),
    'White_Dark_Spirit':    (PieceType.DARK_SPIRIT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Deva':           (PieceType.DEVA, PieceColor.WHITE, PieceRank.OTHER),
    'White_Earth_General':  (PieceType.EARTH_GENERAL, PieceColor.WHITE, PieceRank.OTHER),
    'White_Enchanted_Badger': (PieceType.ENCHANTED_BADGER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Earth_Chariot':  (PieceType.EARTH_CHARIOT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Earth_Dragon':   (PieceType.EARTH_DRAGON, PieceColor.WHITE, PieceRank.OTHER),
    'White_Fierce_Eagle':   (PieceType.FIERCE_EAGLE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Soaring_Eagle':  (PieceType.SOARING_EAGLE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Eastern_Barbarian': (PieceType.EASTERN_BARBARIAN, PieceColor.WHITE, PieceRank.OTHER),
    'White_Evil_Wolf':      (PieceType.EVIL_WOLF, PieceColor.WHITE, PieceRank.OTHER),
    'White_Fire_General':   (PieceType.FIRE_GENERAL, PieceColor.WHITE, PieceRank.OTHER),
    'White_Flying_Cat':     (PieceType.FLYING_CAT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Flying_Dragon':  (PieceType.FLYING_DRAGON, PieceColor.WHITE, PieceRank.OTHER),
    'White_Free_Eagle':     (PieceType.FREE_EAGLE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Fragrant_Elephant': (PieceType.FRAGRANT_ELEPHANT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Flying_Horse':    (PieceType.FLYING_HORSE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Fire_Dragon':     (PieceType.FIRE_DRAGON, PieceColor.WHITE, PieceRank.OTHER),
    'White_Ferocious_Leopard': (PieceType.FEROCIOUS_LEOPARD, PieceColor.WHITE, PieceRank.OTHER),
    'White_Forest_Demon':   (PieceType.FOREST_DEMON, PieceColor.WHITE, PieceRank.OTHER),
    'White_Free_Pup':       (PieceType.FREE_PUP, PieceColor.WHITE, PieceRank.OTHER),
    'White_Free_Demon':     (PieceType.FREE_DEMON, PieceColor.WHITE, PieceRank.OTHER),
    'White_Flying_Swallow': (PieceType.FLYING_SWALLOW, PieceColor.WHITE, PieceRank.OTHER),
    'White_Free_Dream_Eater': (PieceType.FREE_DREAM_EATER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Flying_Goose':    (PieceType.FLYING_GOOSE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Go_Between':      (PieceType.GO_BETWEEN, PieceColor.WHITE, PieceRank.OTHER),
    'White_Gold_Chariot':   (PieceType.GOLD_CHARIOT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Great_Dragon':   (PieceType.GREAT_DRAGON, PieceColor.WHITE, PieceRank.OTHER),
    'White_Great_Standard':  (PieceType.GREAT_STANDARD, PieceColor.WHITE, PieceRank.OTHER),
    'White_Great_General':   (PieceType.GREAT_GENERAL, PieceColor.WHITE, PieceRank.GREAT_GENERAL),
    'White_Golden_Deer':    (PieceType.GOLDEN_DEER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Great_Master':   (PieceType.GREAT_MASTER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Wood_General':   (PieceType.WOOD_GENERAL, PieceColor.WHITE, PieceRank.OTHER),
    'White_Golden_Bird':    (PieceType.GOLDEN_BIRD, PieceColor.WHITE, PieceRank.OTHER),
    'White_Great_Dove':     (PieceType.GREAT_DOVE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Great_Stag':     (PieceType.GREAT_STAG, PieceColor.WHITE, PieceRank.OTHER),
    'White_Great_Turtle':   (PieceType.GREAT_TURTLE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Guardian_Of_The_Gods': (PieceType.GUARDIAN_OF_THE_GODS, PieceColor.WHITE, PieceRank.OTHER),
    'White_Horse_General':  (PieceType.HORSE_GENERAL, PieceColor.WHITE, PieceRank.OTHER),
    'White_Howling_Dog':    (PieceType.HOWLING_DOG, PieceColor.WHITE, PieceRank.OTHER),
    'White_Rams_Head_Soldier': (PieceType.RAMS_HEAD_SOLDIER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Horned_Falcon':  (PieceType.HORNFED_FALCON, PieceColor.WHITE, PieceRank.OTHER),
    'White_Hook_Mover':     (PieceType.HOOK_MOVER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Horseman':       (PieceType.HORSEMAN, PieceColor.WHITE, PieceRank.OTHER),
    'White_Running_Horse':  (PieceType.RUNNING_HORSE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Horse_Soldier':  (PieceType.HORSE_SOLDIER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Iron_General':   (PieceType.IRON_GENERAL, PieceColor.WHITE, PieceRank.OTHER),
    'White_Shogi_King':     (PieceType.SHOGI_KING, PieceColor.WHITE, PieceRank.OTHER),
    'White_Kirin_Master':   (PieceType.KIRIN_MASTER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Kirin':          (PieceType.KIRIN, PieceColor.WHITE, PieceRank.OTHER),
    'White_Longbow_Soldier': (PieceType.LONGBOW_SOLDIER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Left_Chariot':   (PieceType.LEFT_CHARIOT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Lion_Dog':       (PieceType.LION_DOG, PieceColor.WHITE, PieceRank.OTHER),
    'White_Left_Dragon':    (PieceType.LEFT_DRAGON, PieceColor.WHITE, PieceRank.OTHER),
    'White_Left_General':   (PieceType.LEFT_GENERAL, PieceColor.WHITE, PieceRank.OTHER),
    'White_Liberated_Horse': (PieceType.LIBERATED_HORSE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Lion_Hawk':      (PieceType.LION_HAWK, PieceColor.WHITE, PieceRank.OTHER),
    'White_Little_Turtle':  (PieceType.LITTLE_TURTLE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Lion':           (PieceType.LION, PieceColor.WHITE, PieceRank.OTHER),
    'White_Long_Nosed_Goblin': (PieceType.LONG_NOSED_GOBLIN, PieceColor.WHITE, PieceRank.OTHER),
    'White_Leopard_Soldier': (PieceType.LEOPARD_SOLDIER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Little_Standard': (PieceType.LITTLE_STANDARD, PieceColor.WHITE, PieceRank.OTHER),
    'White_Left_Tiger':     (PieceType.LEFT_TIGER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Mountain_General': (PieceType.MOUNTAIN_GENERAL, PieceColor.WHITE, PieceRank.OTHER),
    'White_Mountain_Falcon': (PieceType.MOUNTAIN_FALCON, PieceColor.WHITE, PieceRank.OTHER),
    'White_Side_Monkey':    (PieceType.SIDE_MONKEY, PieceColor.WHITE, PieceRank.OTHER),
    'White_Left_Mountain_Eagle': (PieceType.LEFT_MOUNTAIN_EAGLE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Right_Mountain_Eagle': (PieceType.RIGHT_MOUNTAIN_EAGLE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Mountain_Stag':  (PieceType.MOUNTAIN_STAG, PieceColor.WHITE, PieceRank.OTHER),
    'White_Centaur_Master': (PieceType.CENTAUR_MASTER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Northern_Barbarian': (PieceType.NORTHERN_BARBARIAN, PieceColor.WHITE, PieceRank.OTHER),
    'White_Neighboring_King': (PieceType.NEIGHBORING_KING, PieceColor.WHITE, PieceRank.OTHER),
    'White_Violent_Wolf': (PieceType.VIOLENT_WOLF, PieceColor.WHITE, PieceRank.OTHER),
    'White_Ox_General': (PieceType.OX_GENERAL, PieceColor.WHITE, PieceRank.OTHER),
    'White_Oxcart': (PieceType.OXCART, PieceColor.WHITE, PieceRank.OTHER),
    'White_Old_Kite': (PieceType.OLD_KITE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Old_Monkey': (PieceType.OLD_MONKEY, PieceColor.WHITE, PieceRank.OTHER),
    'White_Old_Rat': (PieceType.OLD_RAT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Ox_Soldier': (PieceType.OX_SOLDIER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Swooping_Owl': (PieceType.SWOOPING_OWL, PieceColor.WHITE, PieceRank.OTHER),
    'White_Flying_Ox': (PieceType.FLYING_OX, PieceColor.WHITE, PieceRank.OTHER),
    'White_Peacock': (PieceType.PEACOCK, PieceColor.WHITE, PieceRank.OTHER),
    'White_Pup_General': (PieceType.PUP_GENERAL, PieceColor.WHITE, PieceRank.OTHER),
    'White_Phoenix': (PieceType.PHOENIX, PieceColor.WHITE, PieceRank.OTHER),
    'White_Pig_General': (PieceType.PIG_GENERAL, PieceColor.WHITE, PieceRank.OTHER),
    'White_Phoenix_Master': (PieceType.PHOENIX_MASTER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Prancing_Stag': (PieceType.PRANCING_STAG, PieceColor.WHITE, PieceRank.OTHER),
    'White_Poisonous_Snake': (PieceType.POISONOUS_SNAKE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Rain_Dragon': (PieceType.RAIN_DRAGON, PieceColor.WHITE, PieceRank.OTHER),
    'White_Rushing_Bird': (PieceType.RUSHING_BIRD, PieceColor.WHITE, PieceRank.OTHER),
    'White_Right_Chariot': (PieceType.RIGHT_CHARIOT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Reclining_Dragon': (PieceType.RECLINING_DRAGON, PieceColor.WHITE, PieceRank.OTHER),
    'White_River_General': (PieceType.RIVER_GENERAL, PieceColor.WHITE, PieceRank.OTHER),
    'White_Right_General': (PieceType.RIGHT_GENERAL, PieceColor.WHITE, PieceRank.OTHER),
    'White_Running_Chariot': (PieceType.RUNNING_CHARIOT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Right_Dragon': (PieceType.RIGHT_DRAGON, PieceColor.WHITE, PieceRank.OTHER),
    'White_Roc_Master': (PieceType.ROC_MASTER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Running_Stag': (PieceType.RUNNING_STAG, PieceColor.WHITE, PieceRank.OTHER),
    'White_Rook_General': (PieceType.ROOK_GENERAL, PieceColor.WHITE, PieceRank.GENERAL),
    'White_Running_Pup': (PieceType.RUNNING_PUP, PieceColor.WHITE, PieceRank.OTHER),
    'White_Running_Rabbit': (PieceType.RUNNING_RABBIT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Rear_Standard': (PieceType.REAR_STANDARD, PieceColor.WHITE, PieceRank.OTHER),
    'White_Running_Tiger': (PieceType.RUNNING_TIGER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Running_Serpent': (PieceType.RUNNING_SERPENT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Reverse_Chariot': (PieceType.REVERSE_CHARIOT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Running_Wolf': (PieceType.RUNNING_WOLF, PieceColor.WHITE, PieceRank.OTHER),
    'White_Side_Boar': (PieceType.SIDE_BOAR, PieceColor.WHITE, PieceRank.OTHER),
    'White_Crossbow_Soldier': (PieceType.CROSSBOW_SOLDIER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Front_Standard': (PieceType.FRONT_STANDARD, PieceColor.WHITE, PieceRank.OTHER),
    'White_Sword_Soldier': (PieceType.SWORD_SOLDIER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Side_Flyer': (PieceType.SIDE_FLYER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Stone_General': (PieceType.STONE_GENERAL, PieceColor.WHITE, PieceRank.OTHER),
    'White_Side_Dragon': (PieceType.SIDE_DRAGON, PieceColor.WHITE, PieceRank.OTHER),
    'White_Side_Soldier': (PieceType.SIDE_SOLDIER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Side_Mover': (PieceType.SIDE_MOVER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Coiled_Serpent': (PieceType.COILED_SERPENT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Soldier': (PieceType.SOLDIER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Spear_Soldier': (PieceType.SPEAR_SOLDIER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Square_Mover': (PieceType.SQUARE_MOVER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Silver_Rabbit': (PieceType.SILVER_RABBIT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Side_Serpent': (PieceType.SIDE_SERPENT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Strutting_Crow': (PieceType.STRUTTING_CROW, PieceColor.WHITE, PieceRank.OTHER),
    'White_Southern_Barbarian': (PieceType.SOUTHERN_BARBARIAN, PieceColor.WHITE, PieceRank.OTHER),
    'White_Silver_Chariot': (PieceType.SILVER_CHARIOT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Swallows_Wings': (PieceType.SWALLOWS_WINGS, PieceColor.WHITE, PieceRank.OTHER),
    'White_Side_Ox': (PieceType.SIDE_OX, PieceColor.WHITE, PieceRank.OTHER),
    'White_Tile_General': (PieceType.TILE_GENERAL, PieceColor.WHITE, PieceRank.OTHER),
    'White_Tile_Chariot': (PieceType.TILE_CHARIOT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Turtle_Dove': (PieceType.TURTLE_DOVE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Treacherous_Fox': (PieceType.TREACHEROUS_FOX, PieceColor.WHITE, PieceRank.OTHER),
    'White_Savage_Tiger': (PieceType.SAVAGE_TIGER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Turtle_Snake': (PieceType.TURTLE_SNAKE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Right_Tiger': (PieceType.RIGHT_TIGER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Violent_Bear': (PieceType.VIOLENT_BEAR, PieceColor.WHITE, PieceRank.OTHER),
    'White_Violent_Dragon': (PieceType.VIOLENT_DRAGON, PieceColor.WHITE, PieceRank.GENERAL),
    'White_Vertical_Bear': (PieceType.VERTICAL_BEAR, PieceColor.WHITE, PieceRank.OTHER),
    'White_Vice_General': (PieceType.VICE_GENERAL, PieceColor.WHITE, PieceRank.VICE_GENERAL),
    'White_Vertical_Horse': (PieceType.VERTICAL_HORSE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Vermilion_Sparrow': (PieceType.VERMILION_SPARROW, PieceColor.WHITE, PieceRank.OTHER),
    'White_Vertical_Leopard': (PieceType.VERTICAL_LEOPARD, PieceColor.WHITE, PieceRank.OTHER),
    'White_Vertical_Mover': (PieceType.VERTICAL_MOVER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Violent_Ox': (PieceType.VIOLENT_OX, PieceColor.WHITE, PieceRank.OTHER),
    'White_Vertical_Pup': (PieceType.VERTICAL_PUP, PieceColor.WHITE, PieceRank.OTHER),
    'White_Vertical_Soldier': (PieceType.VERTICAL_SOLDIER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Violent_Stag': (PieceType.VIOLENT_STAG, PieceColor.WHITE, PieceRank.OTHER),
    'White_Vertical_Tiger': (PieceType.VERTICAL_TIGER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Vertical_Wolf': (PieceType.VERTICAL_WOLF, PieceColor.WHITE, PieceRank.OTHER),
    'White_Whale': (PieceType.WHALE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Water_Dragon': (PieceType.WATER_DRAGON, PieceColor.WHITE, PieceRank.OTHER),
    'White_Water_Buffalo': (PieceType.WATER_BUFFALO, PieceColor.WHITE, PieceRank.OTHER),
    'White_Wood_Chariot': (PieceType.WOOD_CHARIOT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Wind_Dragon': (PieceType.WIND_DRAGON, PieceColor.WHITE, PieceRank.OTHER),
    'White_White_Elephant': (PieceType.WHITE_ELEPHANT, PieceColor.WHITE, PieceRank.OTHER),
    'White_Side_Wolf': (PieceType.SIDE_WOLF, PieceColor.WHITE, PieceRank.OTHER),
    'White_Water_General': (PieceType.WATER_GENERAL, PieceColor.WHITE, PieceRank.OTHER),
    'White_White_Horse': (PieceType.WHITE_HORSE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Woodland_Demon': (PieceType.WOODLAND_DEMON, PieceColor.WHITE, PieceRank.OTHER),
    'White_Wind_General': (PieceType.WIND_GENERAL, PieceColor.WHITE, PieceRank.OTHER),
    'White_Wooden_Dove': (PieceType.WOODEN_DOVE, PieceColor.WHITE, PieceRank.OTHER),
    'White_Wrestler': (PieceType.WRESTLER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Western_Barbarian': (PieceType.WESTERN_BARBARIAN, PieceColor.WHITE, PieceRank.OTHER),
    'White_White_Tiger': (PieceType.WHITE_TIGER, PieceColor.WHITE, PieceRank.OTHER),
    'White_Yaksha': (PieceType.YAKSHA, PieceColor.WHITE, PieceRank.OTHER),
    
    'Black_Pawn':           (PieceType.PAWN, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Knight':         (PieceType.KNIGHT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Bishop':         (PieceType.BISHOP, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Rook':           (PieceType.ROOK, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Queen':          (PieceType.QUEEN, PieceColor.BLACK, PieceRank.OTHER),
    'Black_King':           (PieceType.KING, PieceColor.BLACK, PieceRank.KING),
    'Black_Gold_General':   (PieceType.GOLD_GENERAL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Silver_General': (PieceType.SILVER_GENERAL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Shogi_Knight':   (PieceType.SHOGI_KNIGHT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Lance':          (PieceType.LANCE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Shogi_Pawn':     (PieceType.SHOGI_PAWN, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Dragon':         (PieceType.DRAGON, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Horse':          (PieceType.HORSE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Angry_Boar':     (PieceType.ANGRY_BOAR, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Running_Bear':   (PieceType.RUNNING_BEAR, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Blind_Bear':     (PieceType.BLIND_BEAR, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Beast_Cadet':    (PieceType.BEAST_CADET, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Buddhist_Devil': (PieceType.BUDDHIST_DEVIL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Bear_Soldier':   (PieceType.BEAR_SOLDIER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Bishop_General': (PieceType.BISHOP_GENERAL, PieceColor.BLACK, PieceRank.GENERAL),
    'Black_Blind_Dog':      (PieceType.BLIND_DOG, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Blue_Dragon':    (PieceType.BLUE_DRAGON, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Blind_Monkey':   (PieceType.BLIND_MONKEY, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Burning_Soldier': (PieceType.BURNING_SOLDIER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Beast_Officer':  (PieceType.BEAST_OFFICER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Boar_Soldier':   (PieceType.BOAR_SOLDIER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Blind_Tiger':    (PieceType.BLIND_TIGER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Copper_General': (PieceType.COPPER_GENERAL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Capricorn':      (PieceType.CAPRICORN, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Chinese_Rooster': (PieceType.CHINESE_ROOSTER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Ceramic_Dove':   (PieceType.CERAMIC_DOVE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Cloud_Eagle':    (PieceType.CLOUD_EAGLE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Chicken_General': (PieceType.CHICKEN_GENERAL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Chariot_Soldier': (PieceType.CHARIOT_SOLDIER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Stone_Chariot':  (PieceType.STONE_CHARIOT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Flying_Rooster': (PieceType.FLYING_ROOSTER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Cloud_Dragon':   (PieceType.CLOUD_DRAGON, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Climbing_Monkey': (PieceType.CLIMBING_MONKEY, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Center_Standard': (PieceType.CENTER_STANDARD, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Captive_Officer': (PieceType.CAPTIVE_OFFICER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Prince':         (PieceType.PRINCE, PieceColor.BLACK, PieceRank.KING),
    'Black_Copper_Chariot': (PieceType.COPPER_CHARIOT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Cat_Sword':      (PieceType.CAT_SWORD, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Captive_Cadet':  (PieceType.CAPTIVE_CADET, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Dog':            (PieceType.DOG, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Drunken_Elephant': (PieceType.DRUNKEN_ELEPHANT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Roaring_Dog':    (PieceType.ROARING_DOG, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Dragon_Horse':   (PieceType.DRAGON_HORSE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Dragon_King':    (PieceType.DRAGON_KING, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Donkey':         (PieceType.DONKEY, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Fire_Demon':     (PieceType.FIRE_DEMON, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Dark_Spirit':    (PieceType.DARK_SPIRIT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Deva':           (PieceType.DEVA, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Earth_General':  (PieceType.EARTH_GENERAL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Enchanted_Badger': (PieceType.ENCHANTED_BADGER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Earth_Chariot':  (PieceType.EARTH_CHARIOT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Earth_Dragon':   (PieceType.EARTH_DRAGON, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Fierce_Eagle':   (PieceType.FIERCE_EAGLE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Soaring_Eagle':  (PieceType.SOARING_EAGLE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Eastern_Barbarian': (PieceType.EASTERN_BARBARIAN, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Evil_Wolf':      (PieceType.EVIL_WOLF, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Fire_General':   (PieceType.FIRE_GENERAL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Flying_Cat':     (PieceType.FLYING_CAT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Flying_Dragon':  (PieceType.FLYING_DRAGON, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Free_Eagle':     (PieceType.FREE_EAGLE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Fragrant_Elephant': (PieceType.FRAGRANT_ELEPHANT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Flying_Horse':    (PieceType.FLYING_HORSE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Fire_Dragon':     (PieceType.FIRE_DRAGON, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Ferocious_Leopard': (PieceType.FEROCIOUS_LEOPARD, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Forest_Demon':   (PieceType.FOREST_DEMON, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Free_Pup':       (PieceType.FREE_PUP, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Free_Demon':     (PieceType.FREE_DEMON, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Flying_Swallow': (PieceType.FLYING_SWALLOW, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Free_Dream_Eater': (PieceType.FREE_DREAM_EATER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Flying_Goose':    (PieceType.FLYING_GOOSE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Go_Between':      (PieceType.GO_BETWEEN, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Gold_Chariot':   (PieceType.GOLD_CHARIOT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Great_Dragon':   (PieceType.GREAT_DRAGON, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Great_Standard':  (PieceType.GREAT_STANDARD, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Great_General':   (PieceType.GREAT_GENERAL, PieceColor.BLACK, PieceRank.GREAT_GENERAL),
    'Black_Golden_Deer':    (PieceType.GOLDEN_DEER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Great_Master':   (PieceType.GREAT_MASTER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Wood_General':   (PieceType.WOOD_GENERAL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Golden_Bird':    (PieceType.GOLDEN_BIRD, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Great_Dove':     (PieceType.GREAT_DOVE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Great_Stag':     (PieceType.GREAT_STAG, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Great_Turtle':   (PieceType.GREAT_TURTLE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Guardian_Of_The_Gods': (PieceType.GUARDIAN_OF_THE_GODS, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Horse_General':  (PieceType.HORSE_GENERAL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Howling_Dog':    (PieceType.HOWLING_DOG, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Rams_Head_Soldier': (PieceType.RAMS_HEAD_SOLDIER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Horned_Falcon':  (PieceType.HORNFED_FALCON, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Hook_Mover':     (PieceType.HOOK_MOVER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Horseman':       (PieceType.HORSEMAN, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Running_Horse':  (PieceType.RUNNING_HORSE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Horse_Soldier':  (PieceType.HORSE_SOLDIER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Iron_General':   (PieceType.IRON_GENERAL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Shogi_King':     (PieceType.SHOGI_KING, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Kirin_Master':   (PieceType.KIRIN_MASTER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Kirin':          (PieceType.KIRIN, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Longbow_Soldier': (PieceType.LONGBOW_SOLDIER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Left_Chariot':   (PieceType.LEFT_CHARIOT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Lion_Dog':       (PieceType.LION_DOG, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Left_Dragon':    (PieceType.LEFT_DRAGON, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Left_General':   (PieceType.LEFT_GENERAL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Liberated_Horse': (PieceType.LIBERATED_HORSE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Lion_Hawk':      (PieceType.LION_HAWK, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Little_Turtle':  (PieceType.LITTLE_TURTLE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Lion':           (PieceType.LION, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Long_Nosed_Goblin': (PieceType.LONG_NOSED_GOBLIN, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Leopard_Soldier': (PieceType.LEOPARD_SOLDIER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Little_Standard': (PieceType.LITTLE_STANDARD, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Left_Tiger':     (PieceType.LEFT_TIGER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Mountain_General': (PieceType.MOUNTAIN_GENERAL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Mountain_Falcon': (PieceType.MOUNTAIN_FALCON, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Side_Monkey':    (PieceType.SIDE_MONKEY, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Left_Mountain_Eagle': (PieceType.LEFT_MOUNTAIN_EAGLE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Right_Mountain_Eagle': (PieceType.RIGHT_MOUNTAIN_EAGLE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Mountain_Stag':  (PieceType.MOUNTAIN_STAG, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Centaur_Master': (PieceType.CENTAUR_MASTER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Northern_Barbarian': (PieceType.NORTHERN_BARBARIAN, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Neighboring_King': (PieceType.NEIGHBORING_KING, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Violent_Wolf': (PieceType.VIOLENT_WOLF, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Ox_General': (PieceType.OX_GENERAL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Oxcart': (PieceType.OXCART, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Old_Kite': (PieceType.OLD_KITE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Old_Monkey': (PieceType.OLD_MONKEY, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Old_Rat': (PieceType.OLD_RAT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Ox_Soldier': (PieceType.OX_SOLDIER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Swooping_Owl': (PieceType.SWOOPING_OWL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Flying_Ox': (PieceType.FLYING_OX, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Peacock': (PieceType.PEACOCK, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Pup_General': (PieceType.PUP_GENERAL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Phoenix': (PieceType.PHOENIX, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Pig_General': (PieceType.PIG_GENERAL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Phoenix_Master': (PieceType.PHOENIX_MASTER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Prancing_Stag': (PieceType.PRANCING_STAG, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Poisonous_Snake': (PieceType.POISONOUS_SNAKE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Rain_Dragon': (PieceType.RAIN_DRAGON, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Rushing_Bird': (PieceType.RUSHING_BIRD, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Right_Chariot': (PieceType.RIGHT_CHARIOT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Reclining_Dragon': (PieceType.RECLINING_DRAGON, PieceColor.BLACK, PieceRank.OTHER),
    'Black_River_General': (PieceType.RIVER_GENERAL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Right_General': (PieceType.RIGHT_GENERAL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Running_Chariot': (PieceType.RUNNING_CHARIOT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Right_Dragon': (PieceType.RIGHT_DRAGON, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Roc_Master': (PieceType.ROC_MASTER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Running_Stag': (PieceType.RUNNING_STAG, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Rook_General': (PieceType.ROOK_GENERAL, PieceColor.BLACK, PieceRank.GENERAL),
    'Black_Running_Pup': (PieceType.RUNNING_PUP, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Running_Rabbit': (PieceType.RUNNING_RABBIT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Rear_Standard': (PieceType.REAR_STANDARD, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Running_Tiger': (PieceType.RUNNING_TIGER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Running_Serpent': (PieceType.RUNNING_SERPENT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Reverse_Chariot': (PieceType.REVERSE_CHARIOT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Running_Wolf': (PieceType.RUNNING_WOLF, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Side_Boar': (PieceType.SIDE_BOAR, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Crossbow_Soldier': (PieceType.CROSSBOW_SOLDIER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Front_Standard': (PieceType.FRONT_STANDARD, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Sword_Soldier': (PieceType.SWORD_SOLDIER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Side_Flyer': (PieceType.SIDE_FLYER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Stone_General': (PieceType.STONE_GENERAL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Side_Dragon': (PieceType.SIDE_DRAGON, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Side_Soldier': (PieceType.SIDE_SOLDIER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Side_Mover': (PieceType.SIDE_MOVER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Coiled_Serpent': (PieceType.COILED_SERPENT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Soldier': (PieceType.SOLDIER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Spear_Soldier': (PieceType.SPEAR_SOLDIER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Square_Mover': (PieceType.SQUARE_MOVER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Silver_Rabbit': (PieceType.SILVER_RABBIT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Side_Serpent': (PieceType.SIDE_SERPENT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Strutting_Crow': (PieceType.STRUTTING_CROW, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Southern_Barbarian': (PieceType.SOUTHERN_BARBARIAN, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Silver_Chariot': (PieceType.SILVER_CHARIOT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Swallows_Wings': (PieceType.SWALLOWS_WINGS, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Side_Ox': (PieceType.SIDE_OX, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Tile_General': (PieceType.TILE_GENERAL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Tile_Chariot': (PieceType.TILE_CHARIOT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Turtle_Dove': (PieceType.TURTLE_DOVE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Treacherous_Fox': (PieceType.TREACHEROUS_FOX, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Savage_Tiger': (PieceType.SAVAGE_TIGER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Turtle_Snake': (PieceType.TURTLE_SNAKE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Right_Tiger': (PieceType.RIGHT_TIGER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Violent_Bear': (PieceType.VIOLENT_BEAR, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Violent_Dragon': (PieceType.VIOLENT_DRAGON, PieceColor.BLACK, PieceRank.GENERAL),
    'Black_Vertical_Bear': (PieceType.VERTICAL_BEAR, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Vice_General': (PieceType.VICE_GENERAL, PieceColor.BLACK, PieceRank.VICE_GENERAL),
    'Black_Vertical_Horse': (PieceType.VERTICAL_HORSE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Vermillion_Sparrow': (PieceType.VERMILION_SPARROW, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Vertical_Leopard': (PieceType.VERTICAL_LEOPARD, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Vertical_Mover': (PieceType.VERTICAL_MOVER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Violent_Ox': (PieceType.VIOLENT_OX, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Vertical_Pup': (PieceType.VERTICAL_PUP, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Vertical_Soldier': (PieceType.VERTICAL_SOLDIER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Violent_Stag': (PieceType.VIOLENT_STAG, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Vertical_Tiger': (PieceType.VERTICAL_TIGER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Vertical_Wolf': (PieceType.VERTICAL_WOLF, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Whale': (PieceType.WHALE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Water_Dragon': (PieceType.WATER_DRAGON, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Water_Buffalo': (PieceType.WATER_BUFFALO, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Wood_Chariot': (PieceType.WOOD_CHARIOT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Wind_Dragon': (PieceType.WIND_DRAGON, PieceColor.BLACK, PieceRank.OTHER),
    'Black_White_Elephant': (PieceType.WHITE_ELEPHANT, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Side_Wolf': (PieceType.SIDE_WOLF, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Water_General': (PieceType.WATER_GENERAL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_White_Horse': (PieceType.WHITE_HORSE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Woodland_Demon': (PieceType.WOODLAND_DEMON, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Wind_General': (PieceType.WIND_GENERAL, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Wooden_Dove': (PieceType.WOODEN_DOVE, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Wrestler': (PieceType.WRESTLER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Western_Barbarian': (PieceType.WESTERN_BARBARIAN, PieceColor.BLACK, PieceRank.OTHER),
    'Black_White_Tiger': (PieceType.WHITE_TIGER, PieceColor.BLACK, PieceRank.OTHER),
    'Black_Yaksha': (PieceType.YAKSHA, PieceColor.BLACK, PieceRank.OTHER),
}

ROYAL_PIECES = ['Rook_General', 'Bishop_General', 'Violent_Dragon', 'Flying_Crocodile', 'Vice_General', 'Great_General']
HOOK_MOVERS = ['Hook_Mover', 'Capricorn', 'Long_Nosed_Goblin', 'Peacock']
JUMP_MOVERS = ['Roc_Master']