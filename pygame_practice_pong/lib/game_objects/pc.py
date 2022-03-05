import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


# Not sure if there's a difference between the PC and NPC yet
class Pc(pygame.Rect):
    def __init__(self, start_x: int, start_y: int, width: int, height: int) -> None:
        super().__init__(start_x, start_y, width, height)

        self.speed: int = 0  # Player paddle speed is handled in the event handling method(s)
        self.speed_adjustment: int = 10  # Increase/decrease the player paddle speed by this number (in event handling)
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
