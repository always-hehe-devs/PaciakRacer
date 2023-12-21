import pygame
import random


class Obstacles:
    def __init__(self, game, road_pos):
        self.game = game
        self.road_pos = road_pos
        self.obstacle_x = 0
        self.obstacle_images = self.game.assets['obstacles']
        self.obstacle_image = self.game.assets['obstacles'][1]
        self.obstacle_size = self.obstacle_image.get_size()
        self.obstacle_mask = pygame.mask.from_surface(self.obstacle_image)
        self.obstacle_offset = 70

        self.prev = self.game.assets['obstacles'][0]

    def get_random_obstacle(self):
        self.obstacle_image = random.choice(self.obstacle_images)
        while self.prev == self.obstacle_image:
            self.obstacle_image = random.choice(self.obstacle_images)
        self.obstacle_offset = random.randint(20, 72)
        return self.obstacle_image

    def render_obstacles(self, surface, speed):
        self.obstacle_x += speed // 16
        obstacle = self.obstacle_image
        self.obstacle_size = (obstacle.get_width() * 2, obstacle.get_height() * 2)
        obstacle = pygame.transform.smoothscale(obstacle, size=self.obstacle_size)
        obstacle_mask_size_height = min(26, max(0, (self.obstacle_size[1] // 2) - 8))
        self.obstacle_mask = pygame.mask.Mask(size=(self.obstacle_size[0], obstacle_mask_size_height), fill=True)
        if self.obstacle_x >= self.game.SCALE[0] + obstacle.get_width():
            self.obstacle_x -= self.game.SCALE[0] + obstacle.get_width()
            self.prev = self.obstacle_image
            obstacle = self.get_random_obstacle()
        return surface.blit(obstacle, (self.game.SCALE[0] - self.obstacle_x, self.road_pos + self.obstacle_offset))
