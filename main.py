import sys

import pygame
from lib import sprites
from lib import colors

# import pygame.locals for easier access to key coordinates
from pygame.locals import *


def main():
    # General setup
    pygame.init()
    clock = pygame.time.Clock()

    # Setup main window
    screen_width = 1280
    screen_height = 960
    screen: pygame.Surface = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Pong')

    ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
    player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
    opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

    bg_color_grey12 = pygame.Color('grey12')
    light_grey = (200, 200, 200)

    ball_speed_x = 7
    ball_speed_y = 7
    player_speed = 0
    opponent_speed = 7

    while True:
        # Handling input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_DOWN:
                    player_speed += 7
                if event.key == pygame.K_UP:
                    player_speed -= 7

            if event.type == pygame.KEYUP:
                if event.key == K_DOWN:
                    player_speed -= 7
                if event.key == pygame.K_UP:
                    player_speed += 7

        # Movement/Animations
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Ball Logic
        # If the ball touches the top or bottom of the screen, reverse it's y movement by multiplying it by -1
        if ball.top <= 0 or ball.bottom >= screen_height:
            ball_speed_y *= -1
        # If the ball touches the left or right side of the screen, reverse it's x movement by multiplying it by -1
        if ball.left <= 0 or ball.right >= screen_width:
            ball_speed_x *= -1

        # Player Logic
        if ball.colliderect(player) or ball.colliderect(opponent):
            ball_speed_x *= -1

        # Prevent player from leaving screen
        if player.top <= 0:
            player.top = 0
        if player.bottom >= screen_height:
            player.bottom = screen_height

        # Player Movement/Animation
        player.y += player_speed

        # Opponent Logic
        if ball.x < screen_width // 2:  # Prevent opponent from reacting to the ball before it's in it's court
            if opponent.top < ball.y:
                opponent.top += opponent_speed
            if opponent.bottom > ball.y:
                opponent.bottom -= opponent_speed

        # Prevent Opponent from leaving screen
        if opponent.top <= 0:
            opponent.top = 0
        if opponent.bottom >= screen_height:
            opponent.bottom = screen_height

        # Visualize
        screen.fill(color=bg_color_grey12)
        pygame.draw.rect(surface=screen, color=light_grey, rect=player)
        pygame.draw.rect(surface=screen, color=light_grey, rect=opponent)
        pygame.draw.ellipse(surface=screen, color=light_grey, rect=ball)
        pygame.draw.aaline(
            surface=screen, color=light_grey, start_pos=(screen_width / 2, 0), end_pos=(screen_width / 2, screen_height)
        )

        # Update the window
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
