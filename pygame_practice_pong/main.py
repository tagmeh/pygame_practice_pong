import pygame
import sys
from typing import List

from pygame_practice_pong.lib.game_objects import Ball, Pc, Npc


def event_handling(player: Pc, ball_list: List["Ball"]) -> None:
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
