import pygame
import random
from typing import TYPE_CHECKING, List

from pygame_practice_pong.lib.game_objects.npc  import Npc
from pygame_practice_pong.lib.game_objects.pc import Pc

if TYPE_CHECKING:
    pass


class Ball(pygame.Rect):
    def __init__(self, start_x: int, start_y: int, width: int, height: int) -> None:
        self.start_x: int = start_x
        self.start_y: int = start_y
        super().__init__(self.start_x, self.start_y, width, height)

        self.original: bool = False
        self.remove: bool = False  # A Ball that should be removed from the playing field.

        self.speed_x: float = random.uniform(3, 8)
        self.speed_y: float = random.uniform(3, 8)

    def duplicate(self) -> "Ball":
        ball = Ball(start_x=self.x, start_y=self.y, width=30, height=30)
        ball.randomize_direction()
        return ball

    def __repr__(self) -> str:
        if self.original:
            return f"Original Ball {self.speed_x}, {self.speed_y}"
        else:
            return f"Ball ({id(self)}) {self.speed_x}, {self.speed_y}"

    def move_logic(self, screen_width: int, screen_height: int, player: "Pc", opponent: "Npc") -> None:
        """
        The ball will constantly move at a specific rate, reversing the axis that hits the wall.
        ie ball hits the top wall, reverse the y axis.
        """
        self.move_ip(self.speed_x, self.speed_y)

        # If the ball touches the top or bottom of the screen, reverse it's y movement by multiplying it by -1
        if self.top <= 0:
            self.top = 0
            self.speed_y *= -1  # Reverse y axis direction

        if self.bottom >= screen_height:
            self.bottom = screen_height
            self.speed_y *= -1  # Reverse y axis direction

        # If the ball touches the left or right side of the screen, reverse it's x movement by multiplying it by -1
        if self.left <= 0:
            if self.original:
                self.reset_position(screen_height=screen_height)
                self.randomize_direction()
            else:
                self.remove = True
            player.update_score()
            opponent.update_speed(player=player)

        if self.right >= screen_width:
            if self.original:
                self.reset_position(screen_height=screen_height)
                self.randomize_direction()
            else:
                self.remove = True
            opponent.update_score()


    def reset_position(self, screen_height: int) -> None:
        # 1, and screen_height - 1, are to keep the ball from bouncing between the walls and the outside boundary.
        self.center = (self.start_x, random.randrange(1, screen_height - 1))

    def randomize_direction(self) -> None:
        self.speed_x *= random.choice([1, -1])
        self.speed_y *= random.choice([1, -1])

    def paddle_interaction_logic(self, rects: List[pygame.Rect], ball_list: List["Ball"], player: "Pc") -> None:
        """
        Define the Player/Opponent paddle interaction with the ball.
        Might change when abilities are added.
        """

        # Iterate through the known list of edges/objects the ball might hit.
        for rect in rects:
            if isinstance(rect, Npc):
                if self.colliderect(rect):
                    self.left = rect.right
                    self.speed_x *= -1  # Reverse x axis direction.
                    if len(ball_list) <= (int(player.score) / 10):  # 1 extra ball for every 10 player points.
                        ball_list.append(ball_list[0].duplicate())  # Duplicates the first ball in the ball_list

            if isinstance(rect, Pc):
                if self.colliderect(rect):
                    self.right = rect.left
                    self.speed_x *= -1  # Reverse x axis direction.
