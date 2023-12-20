import pygame
from data.scripts.util import draw_rotated_text


class Score:
    def __init__(self, game):
        self.game = game
        self.total_score = 0
        self.score_font = pygame.font.SysFont(None, 70)
        self.total_score_font = pygame.font.SysFont(None, 50)

    def add_points(self, points):
        self.total_score += points

    def render_score(self, surface):
        self.draw_total_score(surface)

    def draw_total_score(self, surface):
        score_position_offset = 0
        if self.total_score in range(1, 99):
            score_position_offset = 10
        elif self.total_score in range(100, 999):
            score_position_offset = 17
        draw_rotated_text(surface, self.total_score_font,  "Total Score", (20, 20), 20, draw_shadow=True)
        draw_rotated_text(surface, self.score_font, str(int(self.total_score)), (84, 84 - score_position_offset), 20, draw_shadow=True)

