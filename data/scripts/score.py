import pygame


class Score:
    def __init__(self, game):
        self.game = game
        self.total_score = 0

    def add_points(self, points):
        self.total_score += points

    def render_damage(self):
        pass

    def render_score(self, screen):
        pass
