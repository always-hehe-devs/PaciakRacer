import pygame
import sys
from data.scripts.util import load_image, load_images
from data.scripts.motorcycle import Motorcycle
from data.scripts.background import Background
from data.scripts.obstacles import Obstacles


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
            "background": load_image("background/background_0.png"),
            "ground": load_image("tiles/ground/0.png"),
            "road": load_image("tiles/ground/road.png"),
            "car": load_image("cars/car.png", color_key=(0, 0, 0)),
            "biker": load_image("motorcycles/biker.png", alpha_convert=True),
            "speedometer": load_image("speedometer/speedometer.png", alpha_convert=True),
            "needle": load_image("speedometer/needle.png", alpha_convert=True),
            "trees": load_images("background/trees", alpha_convert=True),
            "obstacles": load_images("background/obstacles", alpha_convert=True),
            "lantern": load_image("background/lantern.png", alpha_convert=True)
        }

        self.car_x_pos = 1000
        self.car_rect = self.assets['car'].get_rect(bottomleft=(self.car_x_pos, 960))

        self.collision = False
        self.wheelie = False
        self.throttle_open = False
        self.jumping = False

        self.background = Background(self)
        self.motorcycle = Motorcycle(self, self.assets['biker'], (22, 77))
        self.obstacles = Obstacles(self, self.background.road_y)

    def run(self):
        while True:
            self.background.render_static_background(self.display)
            self.background.render_road(self.display)
            self.background.render(self.display, self.motorcycle.speed)

            obstacle_rect = self.obstacles.render_obstacles(self.display, self.motorcycle.speed)

            self.motorcycle.update()
            self.motorcycle.render(self.display)

            self.background.render_lanterns(self.display, self.motorcycle.speed)

            if self.motorcycle.motorcycle_mask.overlap(self.obstacles.obstacle_mask,
                                                       (obstacle_rect.x - self.motorcycle.motorcycle_pos[0],
                                                        obstacle_rect.y- self.motorcycle.motorcycle_pos[1])):
                self.motorcycle.speed = 0
                self.collision = True
            else:
                self.collision = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.motorcycle.change_gear("up")
                    if event.key == pygame.K_s:
                        self.motorcycle.change_gear("down")
                    if event.key == pygame.K_UP:
                        self.wheelie = True
                    if event.key == pygame.K_a:
                        self.throttle_open = True
                    if event.key == pygame.K_SPACE:
                        self.jumping = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.wheelie = False
                    if event.key == pygame.K_a:
                        self.throttle_open = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()
