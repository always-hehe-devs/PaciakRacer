import pygame
import math
import random


class Motorcycle:

    def __init__(self, game, motorcycle_image, wheel_axle_position):
        self.game = game
        self.motorcycle_image = motorcycle_image
        self.position = [200, 938]
        self.wheel_axle_position = wheel_axle_position
        self.motorcycle_rect = self.position
        self.angle = 0
        self.speed = 0
        self.current_gear = "N"
        self.low_rpm = 1000
        self.max_rpm = 13500
        self.current_rpm = self.low_rpm
        self.rev_limiter_on = False
        self.top_speed = 290
        self.gear_ratios = {"N": 0, 1: 0.5, 2: 0.6, 3: 0.7, 4: 0.85, 5: 0.94, 6: 0.98}
        self.gear_box = len(self.gear_ratios) - 1
        self.idling = True

        self.speedometer_pos = (self.game.RESOLUTION[0] - 550, 20)
        self.speedometer = pygame.transform.smoothscale(self.game.assets['speedometer'], (530, 319))

        self.needle_axle = (31, 9)
        self.needle = pygame.transform.smoothscale(self.game.assets['needle'], (160, 22))
        self.needle_rect = self.needle.get_rect()
        self.needle_angle = 0

        self.font = pygame.font.SysFont(None, 28)
        self.gear_font = pygame.font.Font("data/fonts/digital-7.ttf", 30)
        self.speedo_font = pygame.font.Font("data/fonts/digital-7.ttf", 78)
        self.speedo_unit = pygame.font.Font("data/fonts/digital-7.ttf", 20)

        self.gravity = 1
        self.jump_height = 20
        self.velocity = self.jump_height

    def wheelie(self, surface):
        self.motorcycle_rect = self.motorcycle_image.get_rect(topleft=(self.position[0] - self.wheel_axle_position[0],
                                                                       self.position[1] - self.wheel_axle_position[1]))
        offset_center_to_pivot = pygame.math.Vector2(self.position) - self.motorcycle_rect.center
        if self.angle >= 60:
            self.angle = 60
        rotated_offset = offset_center_to_pivot.rotate(-self.angle)
        rotated_image_center = (self.position[0] - rotated_offset.x, self.position[1] - rotated_offset.y)
        rotated_image = pygame.transform.rotate(self.motorcycle_image, self.angle)
        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

        return surface.blit(rotated_image, rotated_image_rect)

    def wheelie_state(self):
        if self.game.wheelie:
            self.angle += 2
        else:
            if self.angle != 0:
                self.angle -= 1
                if self.angle <= 0:
                    self.angle = 0

    def jump(self):
        if self.game.jumping:
            self.position[1] -= self.velocity
            self.velocity -= self.gravity
            if self.velocity <= -self.jump_height:
                self.game.jumping = False
                self.velocity = self.jump_height
        else:
            self.position[1] = 938

    def calculate_speed(self, engine_rpm):
        gear_ratio = self.gear_ratios[self.current_gear]
        if gear_ratio != 0:
            scaled_rpm = engine_rpm * gear_ratio
            updated_speed = math.floor(min(scaled_rpm / self.max_rpm * self.top_speed, self.top_speed))
            if updated_speed < self.speed:
                self.speed -= 1
            else:
                self.speed = updated_speed
        else:
            if self.speed >= 1:
                self.speed -= 1

    def rev_limiter(self):
        if self.current_rpm >= self.max_rpm:
            self.current_rpm = self.max_rpm - random.randint(100, 200)
            self.rev_limiter_on = True
        else:
            self.rev_limiter_on = False

    def set_rpm(self):
        if self.game.throttle_open and not self.rev_limiter_on:
            self.idling = False
            self.current_rpm += 200
        elif not self.game.throttle_open:
            self.current_rpm -= 100
            if self.current_rpm <= self.low_rpm:
                self.idling = True
                self.current_rpm = random.randint(self.low_rpm - 100, self.low_rpm + 100)
        return self.current_rpm

    def change_gear(self, direction: str):
        if direction == "up":
            if self.current_gear != "N" and self.current_gear != self.gear_box and self.current_gear != 1:
                self.current_rpm -= 2000
                self.current_gear += 1
            elif self.current_gear == 1:
                self.current_gear = "N"
            elif self.current_gear == "N":
                self.current_rpm -= 2000
                self.current_gear = 2
        elif direction == "down":
            if self.current_gear == 2:
                self.current_gear = "N"
            elif self.current_gear == "N" or self.current_gear == 1:
                self.current_gear = 1
                self.current_rpm += 2000
            else:
                self.current_gear -= 1
                after_drop_gear_rpm = self.current_rpm + 2000
                if after_drop_gear_rpm <= self.max_rpm:
                    self.current_rpm += 2000

    def draw_needle(self, surface):
        self.needle_angle = 225 - (self.current_rpm // 58)
        needle_pos = (self.speedometer_pos[0] + 372, 174)
        self.needle_rect = self.needle.get_rect(topleft=(needle_pos[0] - self.needle_axle[0],
                                                         needle_pos[1] - self.needle_axle[1]))
        offset_center_to_pivot = pygame.math.Vector2(needle_pos) - self.needle_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-self.needle_angle)
        rotated_image_center = (needle_pos[0] - rotated_offset.x, needle_pos[1] - rotated_offset.y)
        rotated_image = pygame.transform.rotate(self.needle, self.needle_angle)
        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

        return surface.blit(rotated_image, rotated_image_rect)

    def draw_speedometer(self, surface):
        surface.blit(self.speedometer, self.speedometer_pos)
        self.draw_needle(surface)
        speed = self.speedo_font.render(str(self.speed), True, (0, 0, 0))
        unit = self.speedo_unit.render("km/h", True, (0, 0, 0))

        str_gear = "N" if self.current_gear == 0 else self.current_gear
        gear = self.gear_font.render(f"GEAR {str_gear}", True, (0, 0, 0))
        surface.blit(gear, (self.speedometer_pos[0] + 338, self.speedometer_pos[1] + 228))

        if self.rev_limiter_on:
            pygame.draw.circle(surface, "red", (self.speedometer_pos[0] + 467, self.speedometer_pos[1] + 235), 10)
        if self.current_gear == "N":
            pygame.draw.circle(surface, "green", (self.speedometer_pos[0] + 141, self.speedometer_pos[1] + 288), 13)
            neutral = self.font.render("N", True, (255, 255, 255))
            surface.blit(neutral, (self.speedometer_pos[0] + 134, self.speedometer_pos[1] + 279))

        # bad init?
        counter_offset = 0
        if self.speed in range(10, 19):
            counter_offset = 12
        if self.speed in range(20, 111):
            counter_offset = 35
        if self.speed in range(112, 199):
            counter_offset = 50
        if self.speed >= 200:
            counter_offset = 72

        surface.blit(unit, (self.speedometer_pos[0] + 150, self.speedometer_pos[1] + 110))
        surface.blit(speed, (self.speedometer_pos[0] + 113 - counter_offset, self.speedometer_pos[1] + 100))

    def update(self):
        self.jump()
        self.wheelie_state()
        self.rev_limiter()
        self.calculate_speed(self.set_rpm())

    def render(self, surface):
        self.wheelie(surface)
        self.draw_speedometer(surface)

