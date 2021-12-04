# Program that generates a tree using L-system
import pygame
import random
import math
import copy
from pygame.math import Vector2, Vector3

lines = []
# F = forward + = rotate positive - = rotate negative [ = save branch ] = load branch
rule = ("F", "FF+[+F-F-F]-[-F+F+F]")
saved_lines = []  # Line, rotation and depth
leaf_nodes = set()


def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Simulation Fractals")
    return screen


def game_loop(screen):
    running = True

    while running:
        # Check for exit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                generate_new_tree()

        screen.fill((184, 227, 226))

        wind_factor = math.sin(pygame.time.get_ticks() / 1000)
        wind_force = 50

        # Draw all lines
        leaf_index = 0
        for depth in range(0, len(lines)):
            for line in range(0, len(lines[depth])):
                # Add wind
                start_position = copy.copy(lines[depth][line][0])
                wind_multiplier = (600 - start_position[1]) / 600
                start_position += Vector2(1, 0) * \
                    wind_multiplier * wind_force * wind_factor

                end_position = copy.copy(lines[depth][line][1])
                wind_multiplier = (600 - end_position[1]) / 600
                end_position += Vector2(1, 0) * \
                    wind_multiplier * wind_force * wind_factor

                # Draw branches and leaves
                pygame.draw.line(screen, (143, 79, 30),
                                 start_position, end_position, max(1, int(5 * 0.95 ** depth)))

                if (depth, line) in leaf_nodes:
                    pygame.draw.circle(screen, (97, 212, 109),
                                       end_position, 10)

                    if leaf_index < len(leaf_nodes) - 1:
                        leaf_index += 1

        pygame.display.flip()

    pygame.quit()


def generate_new_tree():
    global lines

    lines = [[(Vector2(300, 600), Vector2(300, 580))]]
    generation_string = generate_string(0, "F")
    add_lines(generation_string)


def generate_string(recursion_depth, string):
    if recursion_depth == 3:
        return string

    new_string = ""
    for char in string:
        if char == rule[0]:
            for result in rule[1]:
                new_string += result
        else:
            new_string += char

    return generate_string(recursion_depth + 1, new_string)


def add_lines(generation_string):
    branch_depth = 0
    last_line = lines[0][len(lines) - 1]
    current_angle = 0

    for step in range(0, len(generation_string)):
        match generation_string[step]:
            case "F":
                # Go forward
                direction = (last_line[1] - last_line[0]
                             ).normalize().rotate(current_angle)

                length = (last_line[1] - last_line[0]).length()
                line = (last_line[1], last_line[1] +
                        direction * length)

                # All branches of the recursion should add to the correct depth
                if len(lines) > branch_depth:
                    lines[branch_depth].append(line)
                else:
                    lines.append([line])

                # Detect leaf nodes
                if step < len(generation_string) - 1 and generation_string[step + 1] == "]":
                    leaf_nodes.add(
                        (branch_depth, len(lines[branch_depth]) - 1))

                last_line = line
                current_angle = 0
                branch_depth += 1
            case "+":
                current_angle += random.randint(25, 35)
            case "-":
                current_angle += random.randint(-35, -25)
            case "[":
                # Save branch
                global saved_lines
                saved_lines.append(
                    (last_line, current_angle, branch_depth))
            case "]":
                # Load branch
                saved_line = saved_lines.pop()
                last_line = saved_line[0]
                current_angle = 0
                current_angle = saved_line[1]
                branch_depth = saved_line[2]
            case _:
                pass


screen = initialize_game()
generate_new_tree()
game_loop(screen)
