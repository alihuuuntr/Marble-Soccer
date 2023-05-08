import pygame
from constants import ball_radius, BALL_COLOR, WIDTH, HEIGHT, default_friction, minimal_speed
from utils import create_circular_texture

class Ball:
    def __init__(self, x, y, texture):
        self.x = x
        self.y = y
        self.radius = ball_radius
        self.velocity = [0, 0]
        self.original_texture = texture
        self.update_circular_texture()

    def update_circular_texture(self):
        self.texture = create_circular_texture(self.original_texture, self)

    def move(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.update_circular_texture()

    def apply_friction(self, friction=default_friction):
        self.velocity[0] *= friction
        self.velocity[1] *= friction

        if abs(self.velocity[0]) < minimal_speed:
            self.velocity[0] = 0
        if abs(self.velocity[1]) < minimal_speed:
            self.velocity[1] = 0
        
    def bounce_off_wall(self):
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.velocity[0] = -self.velocity[0]

        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.velocity[1] = -self.velocity[1]


def draw_ball(screen, ball):
    pygame.draw.circle(screen, BALL_COLOR, (ball.x, ball.y), ball.radius)



def draw_textured_ball(screen, ball):
    screen.blit(ball.texture, (ball.x - ball.radius, ball.y - ball.radius))

# def draw_textured_ball(screen, ball):
#     # ball_rect = ball.texture.get_rect()
#     # ball_rect.center = (ball.x, ball.y)
#     # screen.blit(ball.texture, ball_rect)