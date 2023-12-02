import random

import pygame
from data.scripts.util import scale_images


class Background:

    def __init__(self, game):
        self.game = game
        self.move_tree_x = 1
        self.trees = self.game.assets['trees']
        self.move_x = 0
        self.scale_offset = 0


    def draw_objects(self, surf, obj_img, bg_x, bg_y):
        surf.blit(obj_img, (bg_x - surf.get_width(), bg_y))
        surf.blit(obj_img, (bg_x, bg_y))

    def create_trees_layers(self):
        self.scale_offset = 50
        layers = []
        for index, tree in enumerate(self.trees):
            tree = pygame.transform.smoothscale(tree, (self.scale_offset + 75, self.scale_offset + 75))
            layer = pygame.Surface((self.game.RESOLUTION[0], tree.get_height()), pygame.SRCALPHA)
            for i in range(12):
                layer.blit(tree, (i * (1.5 * tree.get_width()), 0))
            layers.append(layer)
            self.scale_offset += 100
        return layers

    def render_trees(self, surface):
        time_offset = 0.25
        for layer in self.create_trees_layers():
            self.move_x = (self.move_x - self.move_tree_x) % (2 * self.game.RESOLUTION[0])
            Background.draw_objects(self, surface, layer, self.move_x * time_offset, 960-layer.get_height())
            time_offset += 0.25

    def update(self, speed):
        pass

    def render(self, surface):
        self.render_trees(surface)

# https://stackoverflow.com/questions/63712333/how-to-make-parallax-scrolling-work-properly-with-a-camera-that-stops-at-edges-p/74002486#74002486