import pygame
import sys
from data.scripts.util import load_image, load_images
from data.scripts.motorcycle import Motorcycle
from data.scripts.background import Background
from data.scripts.obstacles import Obstacles
from data.scripts.score import Score
from data.scripts.info_board import InfoBoard

from datetime import datetime, timedelta


class Game:
    RESOLUTION = (1920, 1080)
    SCALE = (RESOLUTION[0] // 2, RESOLUTION[1] // 2)

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Paciak Racer")
        self.screen = pygame.display.set_mode(self.RESOLUTION)
        self.display = pygame.Surface(self.SCALE, pygame.SRCALPHA)

        self.clock = pygame.time.Clock()

        self.assets = {
            "control_board": load_image("boards/control_board.png", alpha_convert=True),
            "background": load_image("background/mirror-lake.png"),
            "ground": load_image("tiles/ground/0.png"),
            "road": load_image("tiles/ground/road.png"),
            "biker": load_image("motorcycles/biker.png", alpha_convert=True),
            "speedometer": load_image("speedometer/speedometer.png", alpha_convert=True),
            "needle": load_image("speedometer/needle.png", alpha_convert=True),
            "trees": load_images("background/trees", alpha_convert=True),
            "obstacles": load_images("background/obstacles", alpha_convert=True),
            "lantern": load_image("background/lantern.png", alpha_convert=True)
        }

        self.collision = False
        self.wheelie = False
        self.throttle_open = False
        self.jumping = False

        self.background = Background(self)

        self.board = InfoBoard(self)
        self.score = Score(self)
        self.motorcycle = Motorcycle(self, self.assets['biker'], (22, 77))
        self.motorcycle_mask_offset_y = self.motorcycle.motorcycle_pos[1] + 74
        self.obstacles = Obstacles(self, self.background.road_y)
        self.obstacle_mask_offset_y = 0


        self.last_key = None
        self.last_key_v = {"up": False, "down": False}

        self.show_board = True
        self.time_over = False
        self.current_time = None
        self.timer = 60 * 1000

    def restart_game(self):
        self.show_board = False
        self.current_time = self.timer
        self.time_over = False
        self.score.total_score = 0
        self.motorcycle.speed = 0
        self.motorcycle.current_gear = "N"
        self.motorcycle.position = [150, 442]
        self.obstacles.obstacle_x = 0
        self.last_key = None


    def run(self):
        while True:
            self.background.render_static_background(self.display)
            self.background.render_road(self.display)
            self.background.render(self.display, self.motorcycle.speed)

            if self.show_board:
                self.board.render_controls_board(self.display)
            elif self.time_over:
                self.board.render_end_game(self.display, self.score.total_score)
            else:
                self.score.render_timer(self.display, self.current_time)
                self.score.render_score(self.display)
                self.motorcycle.update()

                if (self.motorcycle_mask_offset_y) > self.obstacle_mask_offset_y:
                    obstacle_rect = self.obstacles.render_obstacles(self.display, self.motorcycle.speed)
                    self.motorcycle.render(self.display)
                else:
                    self.motorcycle.render(self.display)
                    obstacle_rect = self.obstacles.render_obstacles(self.display, self.motorcycle.speed)

                self.background.render_lanterns(self.display, self.motorcycle.speed)

                self.motorcycle_mask_offset_y = self.motorcycle.motorcycle_pos[1] + 88

                self.obstacle_mask_offset_y = (self.background.road_y + self.obstacles.obstacle_offset +
                                               (self.obstacles.obstacle_size[1] - self.obstacles.obstacle_mask.get_size()[1]))

                if self.motorcycle.motorcycle_mask.overlap(self.obstacles.obstacle_mask,
                                                           (obstacle_rect.x - self.motorcycle.motorcycle_pos[0],
                                                            self.obstacle_mask_offset_y - self.motorcycle_mask_offset_y)):
                    if self.motorcycle.speed != 0 and not self.collision:
                        self.score.substrate_points(100)
                    self.motorcycle.speed = 0
                    self.collision = True

                else:
                    self.collision = False

                if obstacle_rect.x in range(30, 100)  and not self.collision:
                    self.score.add_points(0.02*self.motorcycle.speed // 1)


            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if not self.show_board and not self.time_over:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:
                            self.motorcycle.change_gear("up")
                        if event.key == pygame.K_s:
                            self.motorcycle.change_gear("down")
                        if event.key == pygame.K_a:
                            self.throttle_open = True
                        if event.key == pygame.K_UP:
                            self.last_key = "up"
                            self.last_key_v["up"] = True
                        if event.key == pygame.K_DOWN:
                            self.last_key = "down"
                            self.last_key_v["down"] = True
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP:
                            self.last_key_v["up"] = False
                        if event.key == pygame.K_DOWN:
                            self.last_key_v["down"] = False
                        if event.key == pygame.K_a:
                            self.throttle_open = False
                elif self.show_board or self.time_over:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.restart_game()


            if self.current_time and self.current_time >= 0:
                self.current_time -= self.clock.get_rawtime()
            elif self.current_time and self.current_time <= 0:
                self.time_over = True

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)



if __name__ == "__main__":
    Game().run()
