# Program that generates a random simple tree

from math import ceil, floor
import pygame
import random
from pygame.math import Vector2

lines = []
widths = []
start_time = 0


def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Simulation Fractals")
    return screen


def game_loop(screen):
    running = True
    current_depth = -1.0

    while running:
        # Check for exit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                generate_new_tree()

        screen.fill((255, 255, 255))

        # Draw all lines
        current_progress = current_depth - floor(current_depth)
        current_layer = ceil(current_depth)

        for depth in range(0, current_layer + 1):
            for i in range(0, len(lines[depth])):
                # Draw partial branch
                if depth == current_layer:
                    start_position = lines[depth][i][0]
                    direction = lines[depth][i][1] - start_position
                    end_position = start_position + direction * current_progress
                    pygame.draw.line(screen, (143, 79, 30),
                                     start_position, end_position, int(widths[depth]))
                # Draw full branch
                else:
                    pygame.draw.line(screen, (143, 79, 30),
                                     lines[depth][i][0], lines[depth][i][1], int(widths[depth]))

        # Increase tree growth
        # Clamp depth at max depth to prevent starting to grow non-existant branch
        # Offset to simulate first branch as well
        current_depth = min(
            len(lines) - 0.0001, (pygame.time.get_ticks() - start_time) / 500) - 1.0

        pygame.display.flip()

    pygame.quit()


def generate_new_tree():
    # Reset all variables
    global lines
    global widths
    global start_time

    lines = [[(Vector2(250, 500), Vector2(random.randint(235, 265), 330))]]
    widths = [10]
    add_lines(1, lines[0][len(lines) - 1], widths[len(widths) - 1])
    start_time = pygame.time.get_ticks()


def add_lines(depth, last_line, current_width):
    if depth == 6:
        return

    direction = (last_line[1] - last_line[0]).normalize()
    length = (last_line[1] - last_line[0]).length()

    # Calculate new lines
    left_line = (last_line[1], last_line[1] +
                 direction.rotate(random.randint(-45, -20)) * length * random.uniform(0.5, 0.8))
    right_line = (last_line[1], last_line[1] +
                  direction.rotate(random.randint(20, 45)) * length * random.uniform(0.5, 0.8))

    # All branches of the recursion should add to the correct depth
    if len(lines) > depth:
        lines[depth].append(left_line)
        lines[depth].append(right_line)
    else:
        lines.append([left_line, right_line])

    widths.append(current_width)

    # Continue recursion
    add_lines(depth + 1, left_line, current_width * 0.66)
    add_lines(depth + 1, right_line, current_width * 0.66)


screen = initialize_game()
generate_new_tree()
game_loop(screen)
