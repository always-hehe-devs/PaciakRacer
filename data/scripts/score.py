import pygame
from data.scripts.util import draw_rotated_text


class Score:
    def __init__(self, game):
        self.game = game
        self.total_score = 0
        self.score_font = pygame.font.SysFont(None, 50)

    def add_points(self, points):
        self.total_score += points

    def render_score(self, surface):
        total_score_position = (100, 100)
        draw_rotated_text(surface, self.score_font, str(self.total_score), total_score_position, 20, draw_shadow=True)
