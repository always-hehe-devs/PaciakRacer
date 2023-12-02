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


def scale_images(images, size: tuple):
    scaled_images = []
    for image in images:
        pygame.transform.smoothscale(image, size=size)
        scaled_images.append(image)
    return scaled_images


def load_images(path, color_key=None):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name, color_key=color_key))
    return images


def round_up(first_number: int, second_number: int):
    return (first_number // second_number) + 1
