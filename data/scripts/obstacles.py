import pygame
import random


class Obstacles:
    def __init__(self, game, road_pos):
        self.game = game
        self.road_pos = road_pos
        self.skip_x = 0
        self.obstacle_images = self.game.assets['obstacles']
        self.obstacle_image = self.game.assets['obstacles'][1]

        self.prev = self.game.assets['obstacles'][0]

    def get_random_obstacle(self):
        self.obstacle_image = random.choice(self.obstacle_images)
        while self.prev == self.obstacle_image:
            self.obstacle_image = random.choice(self.obstacle_images)
        return self.obstacle_image

    def render_obstacles(self, surface, speed):
        self.skip_x += speed / 30
        skip = self.obstacle_image
        skip = pygame.transform.smoothscale(skip, size=(skip.get_width() * 2.8, skip.get_height() * 2.8))
        if self.skip_x >= self.game.RESOLUTION[0] + skip.get_width():
            self.skip_x -= self.game.RESOLUTION[0] + skip.get_width()
            self.prev = self.obstacle_image
            skip = self.get_random_obstacle()
        return surface.blit(skip, (self.game.RESOLUTION[0] - self.skip_x, (self.road_pos - skip.get_height())))

