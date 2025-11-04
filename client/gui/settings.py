import pygame
import sys
from enum import Enum, auto
from typing import Dict, List, Tuple, Any

# --- Game & Engine Settings ---
SCREEN_WIDTH: int = 1000
SCREEN_HEIGHT: int = 600
DEFAULT_COOLDOWN: int = 50
FPS: int = 60

# --- Slab/Platform Design Constants ---
BASE_COLOR: Tuple[int, int, int] = (60, 60, 60)  # Dark gray base stone color
HIGHLIGHT_COLOR: Tuple[int, int, int] = (80, 80, 80)  # Slightly lighter top highlight
BORDER_COLOR: Tuple[int, int, int] = (30, 30, 30)  # Border outline color
CRACK_COLOR: Tuple[int, int, int] = (45, 45, 45)  # "Crack" or joint line color
HIGHLIGHT_HEIGHT: int = 5  # Height of the top highlight band (px)
BORDER_WIDTH: int = 2  # Thickness of outer border (px)
LINE_WIDTH: int = 2  # Width of crack/joint lines (px)
MIN_VERTICAL_STEP: int = 50  # Minimum spacing between vertical lines (px)
HORIZONTAL_DIVISIONS: int = 2  # Number of horizontal layers in the slab look

# --- Projectile & Effect Constants ---
EXPLOSION_COOLDOWN: int = 40
FIREBALL_SPEED: int = 15
FIREBALL_LIFETIME: int = 30
FIREBALL_GRAVITY: float = 1.0
FIREBALL_RIGHT_OFFSET_EXPLOSION: int = 10
FIREBALL_FRAME_COUNT: int = 59
EXPLOSION_FRAME_COUNT: int = 5
EXPLOSION_SIZE: int = 100

# --- Player Configuration ---
WIZARD: Dict[str, Any] = {
    "width": 60,
    "height": 135,
    "offset": [112, 75],
    "scale": 1.5,
    "gravity": 2,
    "speed": 10,
    "jump_power": -35,
    "frame_size": 250,
    "staff_x_offset": 40,
    "staff_y_offset": 60,
    "initial_fireball_vel_y": -18,
    "attack_cooldown": 20,
    "animation_rows": {
        "idle": (0, 8),
        "run": (1, 8),
        "jump": (2, 1),
        "attack1": (3, 8),
        "attack2": (4, 8),
        "hurt": (5, 3),
        "death": (6, 7),
    }
}


# ==============================
# ENUMS
# ==============================

class GameLayers(Enum):
    """Defines the rendering order for sprites."""
    BACKGROUND = auto()
    MAP = auto()
    SHADOWS = auto()
    BOTS = auto()
    OBJECTS = auto()
    UI = auto()
