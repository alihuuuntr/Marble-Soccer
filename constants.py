# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0) # Black
TEAM_1_COLOR = (255, 100, 100)  # Reddish
TEAM_2_COLOR = (100, 100, 255) # Greenish
BALL_COLOR = (100, 100, 255)  # Blueish
TEXT_COLOR = (200, 200, 200)  # Light gray
GOAL_COLOR = (255, 255, 255) # White
BACKGROUND_COLOR = (0, 180, 0) 

# Game variables
player_radius = 20
ball_radius = 30
max_speed = 8
goals = [0, 0]
default_friction = 0.99
minimal_speed = 0.06
scal = ball_radius / 60

def initial_player_positions():
    team_1_positions = [
        (100, HEIGHT // 2),
        (200, HEIGHT // 4),
        (200, HEIGHT * 3 // 4),
        (300, HEIGHT // 6),
        (300, HEIGHT * 5 // 6),
    ]
    team_2_positions = [
        (WIDTH - 100, HEIGHT // 2),
        (WIDTH - 200, HEIGHT // 4),
        (WIDTH - 200, HEIGHT * 3 // 4),
        (WIDTH - 300, HEIGHT // 6),
        (WIDTH - 300, HEIGHT * 5 // 6),
    ]
    return team_1_positions + team_2_positions