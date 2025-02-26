"""
Модуль с определением игровых сущностей:
  - Player: игрок, его изображение загружается из файла images1/spaces.png
            (либо другого файла, если передан параметр skin_filename).
  - Enemy: враги, которые движутся и стреляют. Их скин загружается из файла images1/spaces2.png.
  - Projectile: снаряды, выпущенные игроком или врагами.
"""

import pygame
import os

# Глобальные константы для размеров
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50

ENEMY_WIDTH = 40
ENEMY_HEIGHT = 30

PROJECTILE_WIDTH = 5
PROJECTILE_HEIGHT = 10

# Цвета
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Загрузка изображения корабля игрока по умолчанию из папки images1
try:
    PLAYER_IMG_ORIG = pygame.image.load(os.path.join('images1', 'spaces.png'))
    PLAYER_IMG_ORIG = pygame.transform.scale(PLAYER_IMG_ORIG, (PLAYER_WIDTH, PLAYER_HEIGHT))
except Exception as e:
    print(f"Ошибка загрузки изображения игрока: {e}")
    PLAYER_IMG_ORIG = None

# Загрузка изображения врага из файла images1/spaces2.png
try:
    ENEMY_IMG_ORIG = pygame.image.load(os.path.join('images1', 'spaces2.png'))
    ENEMY_IMG_ORIG = pygame.transform.scale(ENEMY_IMG_ORIG, (ENEMY_WIDTH, ENEMY_HEIGHT))
except Exception as e:
    print(f"Ошибка загрузки изображения врага: {e}")
    ENEMY_IMG_ORIG = None

class Player:
    def __init__(self, x, y, skin_filename=None):
        """
        Инициализирует игрока.

        Аргументы:
          x, y - координаты игрока
          skin_filename - (необязательно) имя файла с изображением для скина игрока.
                          Если None, используется изображение по умолчанию (PLAYER_IMG_ORIG).
        """
        self.x = x
        self.y = y
        self.vel = 5
        self.lives = 3
        if skin_filename is None:
            self.image = PLAYER_IMG_ORIG.copy() if PLAYER_IMG_ORIG else None
        else:
            try:
                loaded_img = pygame.image.load(os.path.join('images1', skin_filename))
                loaded_img = pygame.transform.scale(loaded_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
                self.image = loaded_img
            except Exception as e:
                print(f"Ошибка загрузки изображения для игрока: {e}")
                self.image = None
        self.rect = pygame.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

    def set_rotation(self, angle):
        """
        Метод для поворота изображения игрока (не используется в данном варианте).
        """
        if self.image:
            self.image = pygame.transform.rotate(self.image, angle)
            self.width, self.height = self.image.get_size()
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys):
        """
        Перемещает игрока (для одиночного режима; управление стрелками).
        """
        if keys[pygame.K_LEFT] and self.x - self.vel > 0:
            self.x -= self.vel
        if keys[pygame.K_RIGHT] and self.x + self.vel + self.width < 800:
            self.x += self.vel
        if keys[pygame.K_UP] and self.y - self.vel > 0:
            self.y -= self.vel
        if keys[pygame.K_DOWN] and self.y + self.vel + self.height < 600:
            self.y += self.vel
        self.rect.topleft = (self.x, self.y)

    # Методы для перемещения в двухпользовательском режиме
    def move_left(self):
        if self.x - self.vel > 0:
            self.x -= self.vel
            self.rect.x = self.x

    def move_right(self):
        if self.x + self.vel + self.width < 800:
            self.x += self.vel
            self.rect.x = self.x

    def move_up(self):
        if self.y - self.vel > 0:
            self.y -= self.vel
            self.rect.y = self.y

    def move_down(self):
        if self.y + self.vel + self.height < 600:
            self.y += self.vel
            self.rect.y = self.y

    def shoot(self):
        """
        Создает снаряд.
        """
        proj_x = self.x + self.width // 2 - PROJECTILE_WIDTH // 2
        proj_y = self.y
        return Projectile(proj_x, proj_y, -7, WHITE)

    def update(self):
        """
        Обновление состояния игрока.
        """
        pass

    def draw(self, screen):
        """
        Отрисовка игрока.
        """
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, WHITE, self.rect)

class Enemy:
    def __init__(self, x, y):
        """
        Инициализация врага.
        """
        self.x = x
        self.y = y
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 1
        self.direction = 1  # 1: вправо, -1: влево

    def update(self):
        """
        Обновление позиции врага.
        """
        self.x += self.speed * self.direction
        if self.x <= 0 or self.x >= 800 - self.width:
            self.direction *= -1
            self.y += self.height
        self.rect.topleft = (self.x, self.y)

    def shoot(self):
        """
        Создает снаряд, движущийся вниз.
        """
        proj_x = self.x + self.width // 2 - PROJECTILE_WIDTH // 2
        proj_y = self.y + self.height
        return Projectile(proj_x, proj_y, 7, YELLOW)

    def draw(self, screen):
        """
        Отрисовка врага.
        Если изображение загружено, отображает его, иначе – зеленый прямоугольник.
        """
        if ENEMY_IMG_ORIG:
            screen.blit(ENEMY_IMG_ORIG, (self.x, self.y))
        else:
            pygame.draw.rect(screen, GREEN, self.rect)

class Projectile:
    def __init__(self, x, y, speed, color):
        """
        Инициализация снаряда.
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.width = PROJECTILE_WIDTH
        self.height = PROJECTILE_HEIGHT
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        """
        Обновляет позицию снаряда.
        """
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)

    def is_on_screen(self, screen_height):
        """
        Проверяет, находится ли снаряд в пределах экрана.
        """
        return 0 <= self.y <= screen_height

    def draw(self, screen):
        """
        Отрисовка снаряда.
        """
        pygame.draw.rect(screen, self.color, self.rect)
