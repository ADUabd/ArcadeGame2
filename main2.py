import pygame
import sys


pygame.mixer.init()
pygame.mixer.music.load('sounds/sounds1.mp3')
menu_sounds = pygame.mixer.Sound("sounds/menu_sounds.wav")


def show_menu(screen, menu_image):
    menu_sounds.play()
    pygame.mixer.music.play(-1)
    return