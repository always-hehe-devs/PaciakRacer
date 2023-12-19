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


def load_images(path, color_key=None, alpha_convert=None):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name, color_key=color_key, alpha_convert=alpha_convert))
    return images


def draw_rotated_text(surface, font, text, text_position, angle, color="WHITE", draw_shadow=None, shadow_color="BLACK"):
    if draw_shadow:
        text_offset = (text_position[0]+4, text_position[1]+1)
        text_to_draw = font.render(text, True, shadow_color)
        text_to_draw = pygame.transform.rotate(text_to_draw, angle)
        surface.blit(text_to_draw, text_offset)
    text_to_draw = font.render(text, True, color)
    text_to_draw = pygame.transform.rotate(text_to_draw, angle)
    surface.blit(text_to_draw, text_position)

