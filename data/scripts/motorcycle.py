import pygame
import math
import random


class Motorcycle:

    def __init__(self, game, motorcycle_image, position, wheel_axle_position):
        self.game = game
        self.motorcycle_image = motorcycle_image
        self.position = position
        self.wheel_axle_position = wheel_axle_position
        self.motorcycle_rect = position
        self.angle = 0
        self.speed = 0
        self.gear_box = 6
        self.current_gear = 0
        self.low_rpm = 1200
        self.max_rpm = 12000
        self.current_rpm = self.low_rpm
        self.top_speed = 290
        self.gear_ratios = {0: 0, 1: 0.6, 2: 0.7, 3: 0.80, 4: 0.90, 5: 0.95, 6: 1.0}

        self.font = pygame.font.SysFont(None, 50)

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

    def calculate_speed(self, engine_rpm):
        gear_ratio = self.gear_ratios[self.current_gear]
        if gear_ratio != 0:
            scaled_rpm = engine_rpm * gear_ratio
            updated_speed = math.floor(min(scaled_rpm / self.max_rpm * self.top_speed, self.top_speed))
            if updated_speed < self.speed:
                self.speed -= 2
            else:
                self.speed = updated_speed
        else:
            if self.speed >= 2:
                self.speed -= 2

    def set_rpm(self):
        if self.game.throttle_open and self.current_rpm < self.max_rpm:
            self.current_rpm += 500
        elif not self.game.throttle_open:
            self.current_rpm -= 100
            if self.current_rpm <= self.low_rpm:
                self.current_rpm = random.randint(self.low_rpm - 300, self.low_rpm + 300)
        return self.current_rpm

    def change_gear(self, direction: str):
        if direction == "up":
            if self.current_gear >= self.gear_box:
                self.current_gear = self.gear_box
            else:
                self.current_gear += 1
                self.current_rpm -= 4000
        elif direction == "down":
            if self.current_gear <= 0:
                self.current_gear = 0
            else:
                self.current_gear -= 1
                after_drop_gear_rpm = self.current_rpm + 3000
                if after_drop_gear_rpm <= self.max_rpm:
                    self.current_rpm += 3000
                self.current_rpm = self.max_rpm

    def draw_speedometer(self, surface):
        pygame.draw.rect(surface=surface, color=(0, 0, 0), rect=(50, 100, self.max_rpm//30, 50))
        pygame.draw.rect(surface=surface, color=(139, 0, 0), rect=(50, 100, self.current_rpm//32, 50))

        # counter_shadow = self.font.render(f"{self.current_rpm} RPM", True, (0, 0, 0))
        counter_main = self.font.render(f"{self.current_rpm} RPM", True, (255, 255, 255))
        # counter_shadow_rotated = pygame.transform.rotate(counter_shadow, -30)
        # counter_main_rotated = pygame.transform.rotate(counter_main, -30)

        speed = self.font.render(f"{self.speed} km/h", True, (0, 0, 0))
        gear = self.font.render(str("N" if self.current_gear == 0 else self.current_gear), True, (245, 155, 0))
        surface.blit(gear, (100, 150))
        surface.blit(speed, (310, 150))
        surface.blit(counter_main, (50, 70))

    def render(self, surface):
        rotated_image, rotated_image_rect = self.wheelie()
        self.wheelie_state()
        self.calculate_speed(self.set_rpm())
        self.draw_speedometer(surface)
        surface.blit(rotated_image, rotated_image_rect)
