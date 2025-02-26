import pygame
import sys
import subprocess

pygame.init()


image = pygame.image.load("oboi.png")
img1 = pygame.transform.scale(image, (750, 750))
scr1 = pygame.display.set_mode((750, 750))
pygame.display.set_caption('ArcadeGame')
scr1.blit(img1, (0, 0))
pygame.display.flip()
show_image = True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                pygame.quit()
                subprocess.run(['python', 'game.py'])
            elif event.key == pygame.K_s:
                pygame.quit()
                subprocess.run(['python', 'main1.py'])
            elif event.key == pygame.K_c:
                pygame.quit()
                subprocess.run(['python', 'game1.py'])
            elif event.key == pygame.K_v:
                pygame.quit()
                subprocess.run(['python', 'game2.py'])

pygame.quit()
sys.exit()