import random
import sys
from typing import List

import pygame


class Ball(pygame.Rect):
    def __init__(self, start_x: int, start_y: int, width: int, height: int) -> None:
        self.start_x: int = start_x
        self.start_y: int = start_y
        super().__init__(self.start_x, self.start_y, width, height)

        self.speed_x: float = 7
        self.speed_y: float = 7

    def move_logic(self, screen_width: int, screen_height: int) -> None:
        """
        The ball will constantly move at a specific rate, reversing the axis that hits the wall.
        ie ball hits the top wall, reverse the y axis.
        """
        self.move_ip(self.speed_x, self.speed_y)

        # If the ball touches the top or bottom of the screen, reverse it's y movement by multiplying it by -1
        if self.top <= 0 or self.bottom >= screen_height:
            self.speed_y *= -1  # Reverse y axis direction

        # If the ball touches the left or right side of the screen, reverse it's x movement by multiplying it by -1
        if self.left <= 0:
            self.reset_position()
            self.randomize_direction()

        if self.right >= screen_width:
            self.reset_position()
            self.randomize_direction()

    def reset_position(self) -> None:
        self.center = (self.start_x, self.start_y)

    def randomize_direction(self) -> None:
        self.speed_x *= random.choice([1, -1])
        self.speed_y *= random.choice([1, -1])

    def paddle_interaction_logic(self, rects: List[pygame.Rect]) -> None:
        """
        Define the Player/Opponent paddle interaction with the ball.
        Might change when abilities are added.
        """
        for rect in rects:
            if self.colliderect(rect):
                self.speed_x *= -1  # Reverse x axis direction.


# Not sure if there's a difference between the PC and NPC yet
class Npc(pygame.Rect):
    def __init__(self, start_x: int, start_y: int, width: int, height: int) -> None:
        super().__init__(start_x, start_y, width, height)

        self.speed: int = 7

    def move_logic(self, screen_width: int, screen_height: int) -> None:
        # Prevent paddle from leaving screen
        if self.top <= 0:
            self.top = 0
        if self.bottom >= screen_height:
            self.bottom = screen_height

    def ball_tracking(self, ball: Ball, screen_width: int) -> None:
        # Opponent Logic
        if ball.x < screen_width // 2:  # Prevent opponent from reacting to the ball before it's in its court
            if self.top < ball.y:
                self.top += self.speed
            if self.bottom > ball.y:
                self.bottom -= self.speed


# Not sure if there's a difference between the PC and NPC yet
class Pc(pygame.Rect):
    def __init__(self, start_x: int, start_y: int, width: int, height: int) -> None:
        super().__init__(start_x, start_y, width, height)

        self.speed: int = 0

    def move_logic(self, screen_width: int, screen_height: int) -> None:
        # Prevent paddle from leaving screen
        if self.top <= 0:
            self.top = 0
        if self.bottom >= screen_height:
            self.bottom = screen_height

        # Paddle Movement/Animation
        self.y += self.speed


def main() -> None:
    # General setup
    pygame.init()
    clock = pygame.time.Clock()

    # Setup main window
    screen_width = 1280
    screen_height = 960
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pong")

    ball = Ball(start_x=screen_width // 2 - 15, start_y=screen_height // 2 - 15, width=30, height=30)
    player = Pc(start_x=screen_width - 20, start_y=screen_height // 2 - 70, width=10, height=140)
    opponent = Npc(start_x=10, start_y=screen_height // 2 - 70, width=10, height=140)

    bg_color_grey12 = pygame.Color("grey12")
    light_grey = (200, 200, 200)

    while True:
        # Handling input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player.speed += 7
                if event.key == pygame.K_UP:
                    player.speed -= 7

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.speed -= 7
                if event.key == pygame.K_UP:
                    player.speed += 7

        ball.move_logic(screen_width=screen_width, screen_height=screen_height)
        ball.paddle_interaction_logic(rects=[player, opponent])

        player.move_logic(screen_width=screen_width, screen_height=screen_height)

        opponent.move_logic(screen_width=screen_width, screen_height=screen_height)
        opponent.ball_tracking(ball=ball, screen_width=screen_width)

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


if __name__ == "__main__":
    main()
