import pygame
import sys
from data.scripts.util import load_image, round_up

RESOLUTION = (1920, 1080)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Paciak Racer")
        self.screen = pygame.display.set_mode(RESOLUTION)

        self.clock = pygame.time.Clock()

        self.assets = {
            "background": load_image("background/background_0.png"),
            "ground": load_image("tiles/ground/0.png"),
            "car": load_image("cars/car.png", color_key=(0, 0, 0)),
            "player": load_image("player/player.png", color_key=(235, 235, 235))
        }

        self.car_x_pos = 1000
        self.car_rect = self.assets['car'].get_rect(bottomleft=(self.car_x_pos, 960))

        self.collision = False
        self.angle = 0

        self.player_x_pos = 100
        self.player_y_pos = 960
        self.player_rect = self.assets['player'].get_rect(bottomleft=(self.player_x_pos, self.player_y_pos))

    def wheelie(self):
        player = self.assets["player"]
        rotated_image = pygame.transform.rotate(player, self.angle)
        new_rect = rotated_image.get_rect(center=player.get_rect(bottomleft=(self.player_x_pos, self.player_y_pos)).bottomleft)

        return self.screen.blit(rotated_image, new_rect.center)

    def run(self):
        while True:
            self.screen.blit(self.assets['background'], (0, 0))

            img_width = 0
            for _ in range(round_up(RESOLUTION[0], self.assets["ground"].get_width())):
                tile_position = (img_width, 960)
                self.screen.blit(self.assets['ground'], tile_position)
                img_width = img_width + self.assets["ground"].get_width()

            if not self.collision:
                self.car_rect.x -= 10
                if self.car_rect.x < -(self.assets['car'].get_width()):
                    self.car_rect.x = RESOLUTION[0]
            self.screen.blit(self.assets['car'], self.car_rect)

            self.wheelie()

            if self.player_rect.colliderect(self.car_rect):
                self.collision = True
            else:
                self.collision = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.angle += 10
                    if event.key == pygame.K_SPACE:
                        self.player_rect.y -= 150
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.player_rect.y += 150

            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()
