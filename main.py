import pygame
from constants import WIDTH, HEIGHT, WHITE, BACKGROUND_COLOR, initial_player_positions, goals, scal
from player import Player, draw_players
from ball import Ball, draw_ball, draw_textured_ball
from utils import handle_input, handle_collision, update_positions, check_goal, check_game_over, draw_board, display_game_over_message, reset_ball_and_players, draw_arrow

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple 2D Soccer")

original_texture = pygame.image.load("ball_texture.jpg").convert_alpha()
scaled_texture = pygame.transform.scale(original_texture, (original_texture.get_width() * scal, original_texture.get_height() * scal))

players = [Player(x, y, 0) for x, y in initial_player_positions()]

ball = Ball(WIDTH // 2, HEIGHT // 2, scaled_texture)

turn = 0  # 0 for team 1, 1 for team 2
goals = [0, 0]

# Game loop
running = True
selected_player = None
mouse_pos = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            # Handle input only when the player is not moving
            for player in players:
                if player.velocity == [0, 0]:
                    handle_input([player], 0, event)

    arrow_start = (player.x, player.y)
    arrow_end = (2 * player.x, 2 * player.y)

    

    # Apply friction to the player
    handle_collision(players, ball)
    update_positions(players, ball)
    # Clear screen
    screen.fill(BACKGROUND_COLOR)

    goal_scored, team = check_goal(ball)
    if goal_scored:
        goals[team] += 1
        reset_ball_and_players(ball, players)
        turn = (turn + 1) % 2

    game_over, winning_team = check_game_over(goals)
    if game_over:
        display_game_over_message(screen, winning_team)
        pygame.display.update()
        pygame.time.delay(3000)
        running = False
    # Draw player
    for player in players:
        if player.selected:
            arrow_start = (player.x, player.y)
            arrow_end = (2 * player.x - player.mouse_pos[0], 2 * player.y - player.mouse_pos[1])
            draw_arrow(screen, arrow_start, arrow_end, (0, 255, 0), (255, 0, 0))
    draw_board(screen, goals)
    draw_textured_ball(screen, ball)
    draw_players(screen, players)

    # Update display
    pygame.display.flip()
    pygame.time.delay(10)

pygame.quit()