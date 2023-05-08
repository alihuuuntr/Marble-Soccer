import pygame
import pygame.mask
import pygame.surfarray as surfarray
import numpy as np
import math
from player import Player
from constants import WIDTH, HEIGHT, GOAL_COLOR, TEXT_COLOR,WHITE, goals, initial_player_positions


def handle_input(players, team, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = event.pos
        for player in players:
            if player.team == team:
                if player.collides_with_point(event.pos):
                    player.selected = True
                    player.mouse_pos = (mouse_x, mouse_y)
    elif event.type == pygame.MOUSEMOTION:
        for player in players:
            if player.selected:
                player.mouse_pos = event.pos
    elif event.type == pygame.MOUSEBUTTONUP:
        for player in players:
            if player.selected:
                player.selected = False
                dx = player.x - event.pos[0]
                dy = player.y - event.pos[1] 
                player.shoot(dx, dy)

def draw_arrow(screen, start, end, min_color, max_color):
    pygame.draw.line(screen, interpolate_color(start, end, min_color, max_color), start, end, 2)

    # Arrowhead
    arrowhead_length = 10
    angle = math.atan2(end[1] - start[1], end[0] - start[0]) + math.pi

    arrowhead_angle1 = angle - math.radians(45)
    arrowhead_angle2 = angle + math.radians(45)

    arrowhead_x1 = end[0] + arrowhead_length * math.cos(arrowhead_angle1)
    arrowhead_y1 = end[1] + arrowhead_length * math.sin(arrowhead_angle1)

    arrowhead_x2 = end[0] + arrowhead_length * math.cos(arrowhead_angle2)
    arrowhead_y2 = end[1] + arrowhead_length * math.sin(arrowhead_angle2)

    pygame.draw.line(screen, interpolate_color(start, end, min_color, max_color), end, (arrowhead_x1, arrowhead_y1), 2)
    pygame.draw.line(screen, interpolate_color(start, end, min_color, max_color), end, (arrowhead_x2, arrowhead_y2), 2)

def interpolate_color(start, end, min_color, max_color):
    arrow_length = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
    max_arrow_length = 200  # Adjust this value according to the desired maximum arrow length

    normalized_length = min(arrow_length / max_arrow_length, 1)

    color_r = int(min_color[0] * (1 - normalized_length) + max_color[0] * normalized_length)
    color_g = int(min_color[1] * (1 - normalized_length) + max_color[1] * normalized_length)
    color_b = int(min_color[2] * (1 - normalized_length) + max_color[2] * normalized_length)

    return (color_r, color_g, color_b)

                
# def handle_input(player, event, ball):
#     if event.type == pygame.MOUSEBUTTONDOWN:
#         if player.collides_with_point(event.pos):
#             player.selected = True

#     if event.type == pygame.MOUSEBUTTONUP:
#         if player.selected:
#             player.selected = False
#             dx = event.pos[0] - player.x
#             dy = event.pos[1] - player.y
#             player.shoot_ball(ball, dx, dy)

#     if event.type == pygame.MOUSEMOTION and player.selected:
#         player.update_aim(event.pos)

def player_ball_collision(player, ball):
    dx = player.x - ball.x
    dy = player.y - ball.y
    distance = math.sqrt(dx ** 2 + dy ** 2)

    if distance < ball.radius + player.radius:
        # Calculate the unit vector along the collision axis
        ux = dx / distance
        uy = dy / distance

        # Calculate the velocities along the collision axis
        v1 = ball.velocity[0] * ux + ball.velocity[1] * uy
        v2 = player.velocity[0] * ux + player.velocity[1] * uy

        # Calculate the final velocities along the collision axis after an elastic collision
        new_v1 = v2
        new_v2 = v1

        # Update the object velocities
        ball.velocity[0] += (new_v1 - v1) * ux
        ball.velocity[1] += (new_v1 - v1) * uy
        player.velocity[0] += (new_v2 - v2) * ux
        player.velocity[1] += (new_v2 - v2) * uy

        # Move the objects to prevent overlapping
        overlap = (ball.radius + player.radius) - distance + 1
        ball.x -= overlap * ux / 2
        ball.y -= overlap * uy / 2
        player.x += overlap * ux / 2
        player.y += overlap * uy / 2

def update_positions(players, ball):
    for player in players:
        player.apply_friction()
        player.move()
    ball.apply_friction()
    ball.move()

def handle_collision(players, ball):
    for i, player in enumerate(players):
        player.bounce_off_wall()  # Handle wall collisions for players
        player_ball_collision(player, ball)  # Handle player-ball collisions

        for other_player in players[i + 1:]:
            player.collide_with(other_player)  # Handle player-player collisions

    ball.bounce_off_wall()  # Handle wall collisions for the ball

def check_goal(ball, goal_width=50, goal_height=150):
    if (ball.y >= (HEIGHT - goal_height) // 2) and (ball.y <= (HEIGHT + goal_height) // 2):
        if ball.x <= goal_width:  # Team 2 scores
            return True, 1
        elif ball.x >= WIDTH - goal_width:  # Team 1 scores
            return True, 0

    return False, None  # No goal scored

def draw_board(screen, goals):
    # Draw the game board, including goals and any markings
    goal_width = 100
    pygame.draw.rect(screen, GOAL_COLOR, (0, (HEIGHT - goal_width) // 2, 5, goal_width))
    pygame.draw.rect(screen, GOAL_COLOR, (WIDTH - 5, (HEIGHT - goal_width) // 2, 5, goal_width))

    # Display goals on the screen
    font = pygame.font.Font(None, 36)
    text = font.render(f"Team 1: {goals[0]} | Team 2: {goals[1]}", True, TEXT_COLOR)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 10))

def reset_ball_and_players(ball, players):
    ball.x = WIDTH // 2
    ball.y = HEIGHT // 2
    ball.velocity = [0, 0]

    # Reset players to their initial positions
    initial_positions = initial_player_positions()
    for i, player in enumerate(players):
        player.x, player.y = initial_positions[i]
        player.velocity = [0, 0]

def check_game_over(goals, target_goals=3):
    for i, goal_count in enumerate(goals):
        if goal_count >= target_goals:
            return True, i
    return False, None

def display_game_over_message(screen, winning_team):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Game Over! Team {winning_team + 1} wins!", True, TEXT_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

def fisheye(surface):
    width, height = surface.get_size()
    fisheye_surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    fisheye_surface = fisheye_surface.convert_alpha()

    arr = surfarray.array3d(surface)

    # Create empty output array
    out_arr = np.zeros((width, height, 3), dtype=np.uint8)

    r = min(height, width) // 2

    for x in range(width):
        for y in range(height):
            dx = x - r
            dy = y - r
            
            
            angle = math.atan2(dy, dx)

            # Move the point twice as close to the intersection of the circle
            ex = int(r + r * math.cos(angle))
            ey = int(r + r * math.sin(angle))
            fisheye_x = int(x * 0.75 + ex * 0.25)
            fisheye_y = int(y * 0.75 + ey * 0.25)

            if 0 <= fisheye_x < width and 0 <= fisheye_y < height:
                out_arr[x, y] = arr[fisheye_x, fisheye_y]

    surfarray.blit_array(fisheye_surface, out_arr)
    return fisheye_surface

def create_circular_texture(texture, ball):
    # Apply fisheye transformation to the texture
    fisheye_texture = fisheye(texture)

    circular_texture = pygame.Surface((ball.radius * 2, ball.radius * 2), pygame.SRCALPHA, 32)
    circular_texture = circular_texture.convert_alpha()

    width = (int)(fisheye_texture.get_width() / 6.33333)
    height = (int)(fisheye_texture.get_height()  / 4)
    texture_x = 3 *width - (ball.x % width)
    texture_y = 2 * height - (ball.y % height)

    circular_texture.blit(fisheye_texture, (0, 0), (texture_x, texture_y, ball.radius * 2, ball.radius * 2))

    mask_surface = pygame.Surface((ball.radius * 2, ball.radius * 2), pygame.SRCALPHA, 32)
    pygame.draw.circle(mask_surface, (255, 255, 255), (ball.radius, ball.radius), ball.radius)

    circular_texture.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    return circular_texture

# def create_circular_texture(texture, ball):
#     circular_texture = pygame.Surface((ball.radius * 2, ball.radius * 2), pygame.SRCALPHA, 32)
#     circular_texture = circular_texture.convert_alpha()

#     width = (int)(texture.get_width() / 6.33333)
#     height = (int)(texture.get_height()  / 4)
#     texture_x = 3 *width - (ball.x % width)
#     texture_y = 2 * height - (ball.y % height)

#     circular_texture.blit(texture, (0, 0), (texture_x, texture_y, ball.radius * 2, ball.radius * 2))

#     mask_surface = pygame.Surface((ball.radius * 2, ball.radius * 2), pygame.SRCALPHA, 32)
#     pygame.draw.circle(mask_surface, (255, 255, 255), (ball.radius, ball.radius), ball.radius)

#     circular_texture.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

#     return circular_texture
