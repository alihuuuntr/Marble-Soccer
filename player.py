import pygame
import math
from constants import player_radius, ball_radius, TEAM_1_COLOR, TEAM_2_COLOR, BALL_COLOR, WIDTH, HEIGHT, default_friction, minimal_speed

class Player:
    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team
        self.radius = player_radius
        self.velocity = [0, 0]
        self.selected = False
        self.mouse_pos = None

    def move(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def bounce_off_wall(self):
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.velocity[0] = -self.velocity[0]

        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.velocity[1] = -self.velocity[1]

    def collide_with(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < self.radius + other.radius:
            # Calculate the unit vector along the collision axis
            ux = dx / distance
            uy = dy / distance

            # Calculate the velocities along the collision axis
            v1 = self.velocity[0] * ux + self.velocity[1] * uy
            v2 = other.velocity[0] * ux + other.velocity[1] * uy

            # Calculate the final velocities along the collision axis after an elastic collision
            new_v1 = v2
            new_v2 = v1

            # Update the object velocities
            self.velocity[0] += (new_v1 - v1) * ux
            self.velocity[1] += (new_v1 - v1) * uy
            other.velocity[0] += (new_v2 - v2) * ux
            other.velocity[1] += (new_v2 - v2) * uy

            # Move the objects to prevent overlapping
            overlap = (self.radius + other.radius) - distance + 1
            self.x -= overlap * ux / 2
            self.y -= overlap * uy / 2
            other.x += overlap * ux / 2
            other.y += overlap * uy / 2

    def collides_with_point(self, pos):
        dx = self.x - pos[0]
        dy = self.y - pos[1]
        return math.sqrt(dx ** 2 + dy ** 2) <= self.radius
    
    def apply_friction(self, friction=default_friction):
        self.velocity[0] *= friction
        self.velocity[1] *= friction

        # Stop the player completely if the velocity is very low
        if abs(self.velocity[0]) < minimal_speed:
            self.velocity[0] = 0
        if abs(self.velocity[1]) < minimal_speed:
            self.velocity[1] = 0

    def shoot(self, dx, dy):
        self.velocity = [dx / 10, dy / 10]

def draw_players(screen, players):
    for i, player in enumerate(players):
        color = TEAM_1_COLOR if i < len(players) // 2 else TEAM_2_COLOR
        pygame.draw.circle(screen, color, (player.x, player.y), player.radius)


