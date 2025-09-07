"""
Configuration file for the Street Fighter-style 2D Fighting Game
"""

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Stage dimensions
STAGE_WIDTH = 1000
STAGE_HEIGHT = 600
STAGE_FLOOR = SCREEN_HEIGHT - 150
STAGE_LEFT = (SCREEN_WIDTH - STAGE_WIDTH) // 2
STAGE_RIGHT = STAGE_LEFT + STAGE_WIDTH

# Fighter properties
FIGHTER_WIDTH = 60
FIGHTER_HEIGHT = 120
FIGHTER_SPEED = 4
JUMP_STRENGTH = 16
GRAVITY = 0.8
MAX_FALL_SPEED = 12

# Combat properties
MAX_HEALTH = 100
PUNCH_DAMAGE = 5
KICK_DAMAGE = 9
PUNCH_RANGE = 50
KICK_RANGE = 90
ATTACK_DURATION = 15  # frames
ATTACK_COOLDOWN = 10  # frames after attack
ATTACK_TO_BLOCK_DELAY = 15  # frames after attack before can block
BLOCK_TO_ATTACK_DELAY = 10  # frames after block before can attack
MINIMUM_BLOCK_DURATION = 30  # frames (0.5 seconds at 60 FPS)
BLOCK_REDUCTION = 0.25  # damage taken when blocking (25% of full damage)
PUNCH_KNOCKBACK = 0  # no knockback for punches
KICK_KNOCKBACK = 6   # horizontal knockback for kicks
KICK_UPWARD_FORCE = 8  # upward velocity when kicked
KNOCKBACK_DURATION = 20  # frames of knockback state

# Projectile settings
PROJECTILE_CHARGE_TIME = 40  # frames (~0.67 seconds at 60 FPS)
PROJECTILE_SPEED = FIGHTER_SPEED * 3  # 3x character move speed
PROJECTILE_COOLDOWN = 60  # frames (1 second cooldown)
PROJECTILE_MIN_DAMAGE = 10  # Uncharged damage
PROJECTILE_MAX_DAMAGE = 25  # Fully charged damage (kick level)
PROJECTILE_SIZE = 12  # Radius of projectile

# Visual feedback
HIT_EFFECT_DURATION = 15  # frames to show hit effect
BLOCK_EFFECT_DURATION = 20  # frames to show block effect

# Character collision
PUSH_FORCE = 2  # How much to push when characters collide
PUSH_DISTANCE_THRESHOLD = 5  # Minimum distance from stage edge to allow push

# Audio settings
MASTER_VOLUME = 0.7  # Overall volume (0.0 to 1.0)
SFX_VOLUME = 0.8     # Sound effects volume
MUSIC_VOLUME = 0.5   # Background music volume

# Game timer settings
ROUND_TIME_SECONDS = 60  # 60 seconds per round
ROUND_TIME_FRAMES = ROUND_TIME_SECONDS * FPS  # Convert to frames

# Debug settings
TRAINING_MODE = False  # Disable debug outputs during training

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
DARK_RED = (150, 0, 0)
DARK_BLUE = (0, 0, 150)
LIGHT_GRAY = (200, 200, 200)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# Player 1 controls (WASD + JKL + I)
PLAYER1_CONTROLS = {
    'left': 'a',
    'right': 'd',
    'jump': 'w',
    'punch': 'j',
    'kick': 'k',
    'block': 'l',
    'projectile': 'i'
}

# Player 2 controls (Arrow keys + numpad)
PLAYER2_CONTROLS = {
    'left': 'left',
    'right': 'right',
    'jump': 'up',
    'punch': 'kp1',
    'kick': 'kp2',
    'block': 'kp0',
    'projectile': 'kp3'
}

# Fighter states
class FighterState:
    IDLE = "idle"
    WALKING = "walking"
    JUMPING = "jumping"
    PUNCHING = "punching"
    KICKING = "kicking"
    BLOCKING = "blocking"
    CHARGING = "charging"
    HIT = "hit"
    KNOCKBACK = "knockback"
    KNOCKED_DOWN = "knocked_down"

# Game states
class GameState:
    MENU = "menu"
    FIGHTING = "fighting"
    PAUSED = "paused"
    GAME_OVER = "game_over"

# AI behavior constants
AI_DECISION_INTERVAL = 30  # frames between AI decisions
AI_ATTACK_CHANCE = 0.6  # Increased from 0.3 to make AI more aggressive
AI_BLOCK_CHANCE = 0.2
AI_JUMP_CHANCE = 0.1

# AI behavior modes
class AIBehavior:
    DEFAULT = 1  # Normal AI behavior
    IDLE = 2     # Stand still and do nothing
    BLOCK = 3    # Constantly block
