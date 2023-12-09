import pygame
import random


class Obstacles:
    def __init__(self, game, road_pos):
        self.game = game
        self.road_pos = road_pos
        self.obstacle_x = 0
        self.obstacle_images = self.game.assets['obstacles']
        self.obstacle_image = self.game.assets['obstacles'][1]
        self.obstacle_mask = pygame.mask.from_surface(self.obstacle_image)
        self.obstacle_y = 70

        self.prev = self.game.assets['obstacles'][0]

    def get_random_obstacle(self):
        self.obstacle_image = random.choice(self.obstacle_images)
        while self.prev == self.obstacle_image:
            self.obstacle_image = random.choice(self.obstacle_images)
        return self.obstacle_image

    def render_obstacles(self, surface, speed):
        self.obstacle_x += speed / 30
        obstacle = self.obstacle_image
        obstacle = pygame.transform.smoothscale(obstacle, size=(obstacle.get_width() * 1.5, obstacle.get_height() * 1.5))
        if self.obstacle_x >= self.game.SCALE[0] + obstacle.get_width():
            self.obstacle_x -= self.game.SCALE[0] + obstacle.get_width()
            self.prev = self.obstacle_image
            obstacle = self.get_random_obstacle()
            self.obstacle_mask = pygame.mask.from_surface(self.obstacle_image)
        return surface.blit(obstacle, (self.game.SCALE[0] - self.obstacle_x, self.road_pos + self.obstacle_y))
