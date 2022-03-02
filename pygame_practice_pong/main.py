import random
import sys
import time
from typing import List

import pygame


class Ball(pygame.Rect):
    def __init__(self, start_x: int, start_y: int, width: int, height: int) -> None:
        self.start_x: int = start_x
        self.start_y: int = start_y
        super().__init__(self.start_x, self.start_y, width, height)

        self.speed_x: float = 7
        self.speed_y: float = 7

    def move_logic(self, screen_width: int, screen_height: int, player: "Pc", opponent: "Npc") -> None:
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
            self.reset_position(screen_height=screen_height)
            self.randomize_direction()
            player.update_score()

        if self.right >= screen_width:
            self.reset_position(screen_height=screen_height)
            self.randomize_direction()
            opponent.update_score()

    def reset_position(self, screen_height: int) -> None:
        # 1, and screen_height - 1, are to keep the ball from bouncing between the walls and the outside boundary.
        self.center = (self.start_x, random.randrange(1, screen_height - 1))

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
        self.score: str = "0"

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
                self.top += self.speed - 7
            if self.bottom > ball.y:
                self.bottom -= self.speed - 7

    def reset_score(self) -> None:
        self.score = "0"

    def update_score(self, points: int = 1) -> None:
        self.score = str(int(self.score) + points)


# Not sure if there's a difference between the PC and NPC yet
class Pc(pygame.Rect):
    def __init__(self, start_x: int, start_y: int, width: int, height: int) -> None:
        super().__init__(start_x, start_y, width, height)

        self.speed: int = 0
        self.score: str = "0"

    def move_logic(self, screen_width: int, screen_height: int) -> None:
        # Prevent paddle from leaving screen
        if self.top <= 0:
            self.top = 0
        if self.bottom >= screen_height:
            self.bottom = screen_height

        # Paddle Movement/Animation
        self.y += self.speed

    def reset_score(self) -> None:
        self.score = "0"

    def update_score(self, points: int = 1) -> None:
        self.score = str(int(self.score) + points)


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

    freesansbold_font = pygame.font.SysFont("verdana.ttf", 50)

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

        ball.move_logic(screen_width=screen_width, screen_height=screen_height, player=player, opponent=opponent)
        ball.paddle_interaction_logic(rects=[player, opponent])

        player.move_logic(screen_width=screen_width, screen_height=screen_height)

        opponent.move_logic(screen_width=screen_width, screen_height=screen_height)
        opponent.ball_tracking(ball=ball, screen_width=screen_width)

        # Score Display
        player_score = freesansbold_font.render(player.score, True, (255, 255, 255))

        # In order to have the text to the left of the center line grow left, a Rect() is needed, with a scaling .width
        opponent_score = freesansbold_font.render(opponent.score, True, (255, 255, 255))
        opponent_score_rect = opponent_score.get_rect(
            top=30, height=30, width=22 * len(opponent.score), right=screen_width // 2 - 15
        )

        # Visualize. The order here matters.
        screen.fill(color=bg_color_grey12)
        pygame.draw.rect(surface=screen, color=light_grey, rect=player)
        pygame.draw.rect(surface=screen, color=light_grey, rect=opponent)
        pygame.draw.ellipse(surface=screen, color=light_grey, rect=ball)
        pygame.draw.aaline(
            surface=screen, color=light_grey, start_pos=(screen_width / 2, 0), end_pos=(screen_width / 2, screen_height)
        )
        screen.blit(player_score, (screen_width // 2 + 20, 30))  # Adding a font surface to the screen
        screen.blit(opponent_score, opponent_score_rect)  # Adding a font surface to a Rect object to the screen

        # Update the window
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
