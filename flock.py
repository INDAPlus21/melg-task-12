# Program that simulates simple vehicle movement
import random
import pygame
from pygame.math import Vector2


class Vehicle:
    location = Vector2(0, 0)
    velocity = Vector2(0, 0)
    acceleration = Vector2(0, 0)
    max_speed = 0
    max_acceleration = 0

    def __init__(self, location, max_speed, max_acceleration) -> None:
        self.location = location
        self.max_speed = max_speed
        self.max_acceleration = max_acceleration

    def apply_force(self, force) -> None:
        self.acceleration = force.normalize() * min(force.length(), self.max_acceleration)

    def update_force(self) -> None:
        self.velocity += self.acceleration
        speed = min(self.velocity.length(), self.max_speed)

        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * speed

        self.location += self.velocity
        self.acceleration = Vector2(0, 0)

    def avoid_collision(self, vehicles) -> None:
        total_sum = Vector2(0, 0)
        count = 0

        for other in vehicles:
            distance = Vector2.distance_squared_to(
                self.location, other.location)

            if distance > 0 and distance < 400:
                difference = (self.location - other.location).normalize()
                total_sum += difference
                count += 1

        if count > 0:
            total_sum /= count * self.max_speed
            steer = total_sum - self.velocity

            if steer.length() > 0:
                self.apply_force(steer)


def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Vehicle movement")
    return screen


vehicles = []

for i in range(0, 25):
    vehicles.append(Vehicle(Vector2(250 + random.randint(-200, 200),
                    250 + random.randint(-200, 200)), 0.4, 0.002))


def game_loop(screen):
    running = True

    while running:
        # Check for exit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update vehicles
        for vehicle in vehicles:
            desired_velocity = Vector2(
                pygame.mouse.get_pos()) - vehicle.location

            if desired_velocity.length() < 100:
                desired_velocity = desired_velocity.normalize() * desired_velocity.length() / \
                    100 * vehicle.max_speed
            else:
                desired_velocity = desired_velocity.normalize() * vehicle.max_speed

            steer_force = desired_velocity - vehicle.velocity

            if steer_force.length() > 0:
                vehicle.apply_force(steer_force)

            vehicle.avoid_collision(vehicles)
            vehicle.update_force()

        # Draw
        screen.fill((184, 227, 226))

        for vehicle in vehicles:
            pygame.draw.circle(screen, (100, 100, 100), vehicle.location, 5)

        pygame.display.flip()

    pygame.quit()


screen = initialize_game()
game_loop(screen)
