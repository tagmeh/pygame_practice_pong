import random
import sys
from typing import List

import pygame


class Ball(pygame.Rect):
    def __init__(self, start_x: int, start_y: int, width: int, height: int) -> None:
        self.start_x: int = start_x
        self.start_y: int = start_y
        super().__init__(self.start_x, self.start_y, width, height)

        self.original: bool = False
        self.remove: bool = False  # A Ball that should be removed from the playing field.

        self.speed_x: float = random.uniform(3, 8)
        self.speed_y: float = random.uniform(3, 8)

    def duplicate(self):
        ball = Ball(start_x=self.x, start_y=self.y, width=30, height=30)
        ball.randomize_direction()
        return ball

    def __repr__(self):
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

        # Todo: Implement the same .top .bottom reset for the top and bottom of the screen.
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
                    if len(ball_list) <= (int(player.score)/10):  # 1 extra ball for every 10 player points.
                        ball_list.append(ball_list[0].duplicate())  # Duplicates the first ball in the ball_list

            if isinstance(rect, Pc):
                if self.colliderect(rect):
                    self.right = rect.left
                    self.speed_x *= -1  # Reverse x axis direction.


# Not sure if there's a difference between the PC and NPC yet
class Npc(pygame.Rect):
    def __init__(self, start_x: int, start_y: int, width: int, height: int) -> None:
        super().__init__(start_x, start_y, width, height)

        self.score: str = "0"
        self.starting_speed: int = 5
        self.max_speed_multiplier: int = 3  # Limits the max self.speed value, based on the self.starting_speed.
        self.speed: float = self.starting_speed  # This value changes as the game goes on. See self._update_speed()
        self.fog_of_war: bool = True  # A handicap imposed on the npc. Limits visibility across the center line.

    def move_logic(self, screen_width: int, screen_height: int) -> None:
        # Prevent paddle from leaving screen
        if self.top <= 0:
            self.top = 0
        if self.bottom >= screen_height:
            self.bottom = screen_height

    def _update_speed(self):
        # Allow the Npc paddle's speed to increase to a multiple of it's starting speed.
        if self.speed <= self.starting_speed * self.max_speed_multiplier:
            self.speed *= (1 + int(self.score) / 100)  # Exponentially increase speed, to a point.
            # For linear speed growth: self.speed = self.starting_speed * (1 + int(self.score) / 100)

    def ball_tracking(self, ball_list: List[Ball], screen_width: int) -> None:
        """
        Tracks the nearest ball to the paddle.
        Has a "fog of war" handicap, where it can only respond to a ball's position, if it's left of the center line.
        """
        self._update_speed()
        # Sort ball_list by how close the balls are to the opponent paddle.
        ball_list.sort(key=lambda _ball: _ball.x)
        nearest_ball = ball_list[0]  # First item should either be the OG ball, or the nearest ball.

        # Opponent Logic
        # Prevent opponent from reacting to the ball before it's in its court. "Fog of War"
        if self.fog_of_war:
            if nearest_ball.left > screen_width // 2:
                return
            else:
                if self.top < nearest_ball.top:
                    self.top += self.speed
                if self.bottom > nearest_ball.bottom:
                    self.bottom -= self.speed

    def reset_score(self) -> None:
        self.score = "0"

    def update_score(self, points: int = 1) -> None:
        self.score = str(int(self.score) + points)


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


def event_handling(player: Pc, ball_list: List[Ball]) -> None:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player.speed += player.speed_adjustment
            if event.key == pygame.K_UP:
                player.speed -= player.speed_adjustment

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player.speed -= player.speed_adjustment
            if event.key == pygame.K_UP:
                player.speed += player.speed_adjustment
            if event.key == pygame.K_a:
                # Create a new ball based on another ball's location
                first_ball = ball_list[0]
                new_ball = Ball(start_x=first_ball.x, start_y=first_ball.y, width=30, height=30)
                new_ball.randomize_direction()
                ball_list.append(new_ball)


def main() -> None:
    # General setup
    pygame.init()
    clock = pygame.time.Clock()

    # Setup main window
    screen_width = 800  # 1280
    screen_height = 600  # 960
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pong")

    ball_list: List[Ball] = []
    ball = Ball(start_x=screen_width // 2 - 15, start_y=screen_height // 2 - 15, width=30, height=30)
    ball.original = True  # This ball is the only ball to reset upon scoring (reset is in center of screen)
    ball.speed_x, ball.speed_y = 7, 7  # The OG ball is always the sam speed.
    ball_list.append(ball)  # The OG Ball is not always guaranteed to be the first ball in the list.

    # player = Pc(start_x=screen_width - 20, start_y=screen_height // 2 - 70, width=10, height=300)
    player = Pc(start_x=screen_width - 20, start_y=screen_height // 2 - 70, width=10, height=140)
    opponent = Npc(start_x=10, start_y=screen_height // 2 - 70, width=10, height=140)

    bg_color_grey12 = pygame.Color("grey12")
    light_grey = (200, 200, 200)

    freesansbold_font = pygame.font.SysFont("verdana.ttf", 50)

    while True:

        event_handling(player=player, ball_list=ball_list)

        for ball in ball_list:
            ball.move_logic(screen_width=screen_width, screen_height=screen_height, player=player, opponent=opponent)
            ball.paddle_interaction_logic(rects=[player, opponent], ball_list=ball_list, player=player)

        player.move_logic(screen_width=screen_width, screen_height=screen_height)

        opponent.move_logic(screen_width=screen_width, screen_height=screen_height)
        opponent.ball_tracking(ball_list=ball_list, screen_width=screen_width)

        # Score Display Setup
        player_score = freesansbold_font.render(player.score, True, (255, 255, 255))
        opponent_score = freesansbold_font.render(opponent.score, True, (255, 255, 255))
        # In order to have the text to the left of the center line grow left, a Rect() is needed, with a scaling .width
        opponent_score_rect = opponent_score.get_rect(
            top=30, height=30, width=22 * len(opponent.score), right=screen_width // 2 - 15
        )

        # Cleanup
        for ball in ball_list:
            if ball.remove:  # An event has caused the ball to be marked for removal. (usually scoring)
                ball_list.remove(ball)

        # Visualize. The order here matters.
        # Set background to color
        screen.fill(color=bg_color_grey12)
        # Draw player
        pygame.draw.rect(surface=screen, color=light_grey, rect=player)
        # Draw opponent
        pygame.draw.rect(surface=screen, color=light_grey, rect=opponent)
        # Draw each ball
        for ball in ball_list:
            pygame.draw.ellipse(surface=screen, color=light_grey, rect=ball)
        # Draw center vertical line
        pygame.draw.aaline(
            surface=screen, color=light_grey, start_pos=(screen_width / 2, 0), end_pos=(screen_width / 2, screen_height)
        )
        # Display Score on Screen
        screen.blit(player_score, (screen_width // 2 + 20, 30))  # Adding a font surface to the screen
        screen.blit(opponent_score, opponent_score_rect)  # Adding a font surface to a Rect object to the screen

        # Update the window
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
