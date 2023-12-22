import pygame


class InfoBoard:
    def __init__(self, game):
        self.game = game

    def render_controls_board(self, surface):
        control_board = self.game.assets['control_board']
        asset_center = control_board.get_rect(center=surface.get_rect().center)
        surface.blit(control_board, asset_center)

    def render_score_board(self):
        pass
