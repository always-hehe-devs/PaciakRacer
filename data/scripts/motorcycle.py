import pygame


class Motorcycle:

    def __init__(self, game, motorcycle_image, position, wheel_axle_position):
        self.game = game
        self.motorcycle_image = motorcycle_image
        self.position = position
        self.wheel_axle_position = wheel_axle_position
        self.motorcycle_rect = position
        self.angle = 0

    def wheelie(self):
        self.motorcycle_rect = self.motorcycle_image.get_rect(topleft=(self.position[0] - self.wheel_axle_position[0],
                                                                       self.position[1] - self.wheel_axle_position[1]))
        offset_center_to_pivot = pygame.math.Vector2(self.position) - self.motorcycle_rect.center
        if self.angle >= 60:
            self.angle = 60
        rotated_offset = offset_center_to_pivot.rotate(-self.angle)
        rotated_image_center = (self.position[0] - rotated_offset.x, self.position[1] - rotated_offset.y)
        rotated_image = pygame.transform.rotate(self.motorcycle_image, self.angle)
        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

        return rotated_image, rotated_image_rect

    def wheelie_state(self):
        if self.game.wheelie:
            self.angle += 2
        else:
            if self.angle != 0:
                self.angle -= 1
                if self.angle <= 0:
                    self.angle = 0

    def render(self, surface):
        rotated_image, rotated_image_rect = self.wheelie()
        self.wheelie_state()
        return surface.blit(rotated_image, rotated_image_rect)
