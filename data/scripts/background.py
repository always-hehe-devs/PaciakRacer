import pygame


class Background:

    def __init__(self, game):
        self.game = game
        self.move_tree_x = 1
        self.trees = self.game.assets['trees']
        self.move_x = 0
        self.scale_offset = 0
        self.road_y = self.game.SCALE[1] - self.game.assets["road"].get_height()

    def draw_layers(self, surface, obj_img, bg_x, bg_y):
        bg_x = bg_x % self.game.SCALE[0]
        surface.blit(obj_img, (bg_x - surface.get_width(), bg_y))
        surface.blit(obj_img, (bg_x, bg_y))

    def render_static_background(self, surface):
        surface.blit(self.game.assets['background'], (0, 0))

    def create_lanterns_layers(self):
        lantern = self.game.assets['lantern']
        lantern = pygame.transform.smoothscale(lantern, (lantern.get_width() * 2, lantern.get_height() * 2))
        layer = pygame.Surface((self.game.SCALE[0], lantern.get_height()), pygame.SRCALPHA)
        layer.blit(lantern, dest=(self.game.SCALE[0] - (self.game.SCALE[0] // 2), 0))
        return layer

    def create_road_layer(self):
        road = self.game.assets['road']
        layer = pygame.Surface((self.game.SCALE[0], road.get_height()), pygame.SRCALPHA)
        for i in range((self.game.SCALE[0] // road.get_width()) + 1):
            layer.blit(road, dest=(i * road.get_width(), 0))
        return layer

    def render_road(self, surface):
        layer = self.create_road_layer()
        move_x_road = self.move_x // 3
        return Background.draw_layers(self, surface, layer, move_x_road, self.road_y)

    def create_trees_layers(self):
        self.scale_offset = 0
        layers = []
        for index, tree in enumerate(self.trees):
            layer = pygame.Surface((self.game.SCALE[0], tree.get_height()), pygame.SRCALPHA)
            iteration_num = (self.game.SCALE[0] // (tree.get_width()))
            if iteration_num <= 0:
                iteration_num = 1
            separator = (self.game.SCALE[0] / iteration_num) - tree.get_width()
            for i in range(iteration_num):
                layer.blit(tree, (i * (separator + tree.get_width()), 0))
            layers.append(layer)
            self.scale_offset += 48 * 4
        return layers

    def render_trees(self, surface, speed):
        time_offset = 0.25
        speed = speed / 30
        for layer in self.create_trees_layers():
            self.move_x = self.move_x - speed
            Background.draw_layers(self, surface, layer, self.move_x * time_offset, self.game.SCALE[0] - layer.get_height())
            time_offset += 0.25

    def render_lanterns(self, surface, speed):
        layer = self.create_lanterns_layers()
        speed = speed / 50
        move_x_lantern = self.move_x - speed
        return Background.draw_layers(self, surface, layer, move_x_lantern, (self.game.SCALE[1] - layer.get_height()) - 3)

    def render(self, surface, speed):
        self.render_trees(surface, speed)
