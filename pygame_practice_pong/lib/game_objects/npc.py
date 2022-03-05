import pygame
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:  # Prevent circular import errors
    from pygame_practice_pong.lib.game_objects.ball import Ball
    from pygame_practice_pong.lib.game_objects.pc import Pc


# Some differences between Npc and Pc, might pull out the similarities in a base_object,
#  that doesn't move (precursor for certain environmental hazards and stationary powerups/abilities if I go that route.)
class Npc(pygame.Rect):
    def __init__(self, start_x: int, start_y: int, width: int, height: int) -> None:
        super().__init__(start_x, start_y, width, height)

        self.score: str = "0"
        self.starting_speed: int = 5
        self.max_speed_multiplier: int = 3  # Limits the max self.speed value, based on the self.starting_speed.
        # This value changes as the game goes on. See self._update_speed()
        self.speed: float = float(self.starting_speed)
        self.fog_of_war: bool = True  # A handicap imposed on the npc. Limits visibility across the center line.

    def move_logic(self, screen_width: int, screen_height: int) -> None:
        # Prevent paddle from leaving screen
        if self.top <= 0:
            self.top = 0
        if self.bottom >= screen_height:
            self.bottom = screen_height

    def update_speed(self, player: "Pc") -> None:
        """
        Updates the paddle speed by 1% of its current speed, per player score,
        up to a pre-determined multiple of the self.starting_speed
        May add options to switch between linear and exponential growth.
        """
        # Allow the Npc paddle's speed to increase to a multiple of it's starting speed.
        if self.speed <= self.starting_speed * self.max_speed_multiplier:
            # self.speed *= 1 + int(player.score) / 100  # Exponentially increase speed, to a point.
            # self.speed += self.starting_speed * (int(self.score) / 100)  # linear speed growth
            self.speed += self.speed / 100
        print(f"{self.speed=}")

    def ball_tracking(self, ball_list: List["Ball"], screen_width: int) -> None:
        """
        Tracks the nearest ball to the paddle.
        Has a "fog of war" handicap, where it can only respond to a ball's position, if it's left of the center line.
        """
        # in-place sort ball_list by how close the balls are to the opponent paddle.
        ball_list.sort(key=lambda _ball: _ball.x)  # Type List[Ball]
        nearest_ball = ball_list[0]  # First item should either be the OG ball, or the nearest ball.

        # Opponent Logic
        # Prevent opponent from reacting to the ball before it's in its court. "Fog of War"
        if self.fog_of_war:
            if nearest_ball.left > screen_width // 2:
                return  # Ignore ball position when all balls are right of the center line.

        if self.top < nearest_ball.top:
            self.top += int(self.speed)  # int/float doesn't matter to pygame, but mypy complains.
        if self.bottom > nearest_ball.bottom:
            self.bottom -= int(self.speed)  # int/float doesn't matter to pygame, but mypy complains.

    def reset_score(self) -> None:
        self.score = "0"

    def update_score(self, points: int = 1) -> None:
        self.score = str(int(self.score) + points)
