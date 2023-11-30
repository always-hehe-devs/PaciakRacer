import pygame
import sys
from data.scripts.util import load_image, round_up
from data.scripts.motorcycle import Motorcycle


class Game:
    RESOLUTION = (1920, 1080)
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Paciak Racer")
        self.screen = pygame.display.set_mode(self.RESOLUTION)

        self.clock = pygame.time.Clock()

        self.assets = {
            "background": load_image("background/background_0.png"),
            "ground": load_image("tiles/ground/0.png"),
            "car": load_image("cars/car.png", color_key=(0, 0, 0)),
            "yamaha_r6": load_image("motorcycles/yamaha_r6.png", color_key=(235, 235, 235)),
            "speedometer": load_image("speedometer/speedometer.png", alpha_convert=True),
            "needle": load_image("speedometer/needle.png", alpha_convert=True),
        }

        self.car_x_pos = 1000
        self.car_rect = self.assets['car'].get_rect(bottomleft=(self.car_x_pos, 960))

        self.collision = False
        self.wheelie = False
        self.throttle_open = False

        self.motorcycle_position = [200, 938]
        self.motorcycle = Motorcycle(self, self.assets['yamaha_r6'], self.motorcycle_position, (32, 78))

    def run(self):
        while True:
            self.screen.blit(self.assets['background'], (0, 0))

            img_width = 0
            for _ in range(round_up(self.RESOLUTION[0], self.assets["ground"].get_width())):
                tile_position = (img_width, 960)
                self.screen.blit(self.assets['ground'], tile_position)
                img_width = img_width + self.assets["ground"].get_width()

            # if not self.collision:
            #     self.car_rect.x -= 10
            #     if self.car_rect.x < -(self.assets['car'].get_width()):
            #         self.car_rect.x = RESOLUTION[0]
            # self.screen.blit(self.assets['car'], self.car_rect)

            self.motorcycle.update()
            self.motorcycle.render(self.screen)

            if self.motorcycle.motorcycle_rect.colliderect(self.car_rect):
                self.collision = True
            else:
                self.collision = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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
                        self.motorcycle_position[1] -= 150
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.wheelie = False
                    if event.key == pygame.K_a:
                        self.throttle_open = False
                    if event.key == pygame.K_SPACE:
                        self.motorcycle_position[1] += 150

            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()
