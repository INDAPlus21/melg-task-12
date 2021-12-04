# Program that generates a tree using L-system
import pygame
import random
from pygame.math import Vector2

lines = []
# F = forward + = rotate positive - = rotate negative [ = save branch ] = load branch
rule = ("F", "FF+[+F-F-F]-[-F+F+F]")
saved_lines = []  # Line, rotation and depth


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

        screen.fill((255, 255, 255))

        # Draw all lines
        for depth in range(0, len(lines)):
            for line in lines[depth]:
                pygame.draw.line(screen, (143, 79, 30),
                                 line[0], line[1], max(1, int(5 * 0.95 ** depth)))

                if depth == len(lines) - 1:
                    pygame.draw.circle(screen, (0, 0, 255), line[1], 5)

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

    for step in generation_string:
        match step:
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