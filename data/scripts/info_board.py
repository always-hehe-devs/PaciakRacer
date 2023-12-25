import pygame


class InfoBoard:
    def __init__(self, game):
        self.game = game
        self.basic_font = pygame.font.Font("data/fonts/Pixeled.ttf", 15)
        self.title_font = pygame.font.Font("data/fonts/PixelCards.ttf", 80)

    def render_controls_board(self, surface):
        text = [("GEAR UP", 33),
                ("GEAR DOWN", 44),
                ("MOVE UP", 33),
                ("MOVE DOWN", 44),
                ("ACCELERATE", 42),
                ("QUIT GAME", 73),
                ("      PRESS                       TO START GAME", 0)]
        control_board = self.game.assets['control_board']
        asset_center = control_board.get_rect(center=surface.get_rect().center)
        surface.blit(control_board, asset_center)
        text_offset = 0
        for line in text:
            text_pos = [asset_center[0] + 120, 137 + text_offset]
            controls_desc = self.basic_font.render(line[0], True, (37, 37, 37))
            text_offset += line[1]
            surface.blit(controls_desc, (text_pos[0], text_pos[1]))
        game_name = self.title_font.render("Paciak", True, (112, 20, 96))
        surface.blit(game_name, (asset_center[0] + 140, asset_center[1] + 30))
        game_sub_name = self.basic_font.render("RACER", True, (64, 17, 56))
        surface.blit(game_sub_name, (asset_center[0] + 300, asset_center[1] + 75))

    def render_end_game(self, surface):
        game_sub_name = self.title_font.render("Time's up!", True, (255, 255, 255))
        surface.blit(game_sub_name, (self.game.SCALE[0] // 2, self.game.SCALE[1] // 2))
