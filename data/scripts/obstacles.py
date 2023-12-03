import pygame


class Obstacles:
    def __init__(self, game, road_pos):
        self.game = game
        self.road_pos = road_pos
        self.skip_x = 0

    def render_skip(self, surface, speed):
        self.skip_x += speed / 30
        skip = self.game.assets['skip']
        skip = pygame.transform.smoothscale(skip, size=(skip.get_width() * 2.8, skip.get_height() * 2.8))
        if self.skip_x >= self.game.RESOLUTION[0] + skip.get_width():
            self.skip_x -= self.game.RESOLUTION[0] + skip.get_width()
        return surface.blit(skip, (self.game.RESOLUTION[0] - self.skip_x, (self.road_pos - skip.get_height())))

    def update(self, player):
        pass

    def render(self, surface, speed):
        self.render_skip(surface, speed)
