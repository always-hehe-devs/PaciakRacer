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

    def draw_layers(self, surf, obj_img, bg_x, bg_y):
        bg_x = bg_x % self.game.RESOLUTION[0]
        surf.blit(obj_img, (bg_x - surf.get_width(), bg_y))
        surf.blit(obj_img, (bg_x, bg_y))

    def create_trees_layers(self):
        # TODO make it reusable
        self.scale_offset = 48 * 2
        layers = []
        for index, tree in enumerate(self.trees):
            tree = pygame.transform.smoothscale(tree, (self.scale_offset + 96, self.scale_offset + 96))
            layer = pygame.Surface((self.game.RESOLUTION[0], tree.get_height()), pygame.SRCALPHA)
            iteration_num = (self.game.RESOLUTION[0] // (tree.get_width()))
            if iteration_num <= 0:
                iteration_num = 1
            separator = (self.game.RESOLUTION[0] / iteration_num) - tree.get_width()
            for i in range(iteration_num):
                layer.blit(tree, (i * (separator + tree.get_width()), 0))
            layers.append(layer)
            self.scale_offset += 48 * 6
        return layers

    def render_trees(self, surface, speed):
        time_offset = 0.25
        speed = speed / 50
        for layer in self.create_trees_layers():
            self.move_x = self.move_x - speed
            Background.draw_layers(self, surface, layer, self.move_x * time_offset, 960-layer.get_height())
            time_offset += 0.25

    def update(self, speed):
        pass

    def render(self, surface, speed):
        self.render_trees(surface, speed)
