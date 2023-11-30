import pygame
import os

BASE_IMG_PATH = "data/img/"


def load_image(path, color_key=None, alpha_convert=None):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    if alpha_convert:
        img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    if color_key:
        img.set_colorkey(color_key)
    return img


def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images


def round_up(first_number: int, second_number: int):
    return (first_number // second_number) + 1


class Animation:
    def __init__(self, images, img_duration=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_duration
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]
