"""
Основной модуль игры.

Поддерживаются два режима:
 - Одиночный режим: один игрок управляет кораблём (управление стрелками для перемещения, пробел – стрельба).
 - Режим двух игроков: два игрока (игрок 1 управляется WASD + пробел, игрок 2 – стрелками + Enter).

Никнеймы передаются из экрана настроек. Изображение корабля используется в исходном виде (без поворотов).

Также реализована озвучка событий:
 - **laser-blast.mp3**: воспроизводится при выстреле (игрока или врага);
 - **hit.wav**: воспроизводится, если игрок получает удар (но остаётся жив);
 - **explosion.wav**: воспроизводится, когда у игрока заканчиваются жизни (игрок умирает и игра завершается).
"""

import sys
import random
import pygame
import os
from entities import Player, Enemy, Projectile
from levels import Level, load_records, save_record, draw_records

# Глобальные константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)

# Настройки для врагов
ENEMY_ROWS = 4
ENEMY_COLS = 8

class Game:
    def __init__(self, *names, mode):
        """
        Инициализирует игру.

        Аргументы:
          names – кортеж с никнеймами:
              для одиночного режима: (player1_name, )
              для режима двух игроков: (player1_name, player2_name)
          mode – 'single' или 'two'
        """
        pygame.init()
        pygame.mixer.init()  # Инициализация микшера для звуков
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Space Shooter')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.running = True

        # Загрузка звуков из папки sounds
        self.sound_explosion = pygame.mixer.Sound(os.path.join("sounds", "explosion.wav"))
        self.sound_hit       = pygame.mixer.Sound(os.path.join("sounds", "hit.wav"))
        self.sound_laser     = pygame.mixer.Sound(os.path.join("sounds", "laser-blast.mp3"))

        self.mode = mode
        if self.mode == 'single':
            self.player1_name = names[0]
        else:
            self.player1_name = names[0]
            self.player2_name = names[1]

        # Создаем игрока(ов)
        if self.mode == 'single':
            self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70)
        else:
            # Игрок 1 – стандартный скин
            self.player1 = Player(50, SCREEN_HEIGHT // 2)
            # Игрок 2 – с другим скином (файл spaces3.png)
            self.player2 = Player(SCREEN_WIDTH - 50 - 50, SCREEN_HEIGHT // 2, skin_filename="spaces3.png")

        # Враги и снаряды общие для обоих режимов
        self.enemies = self.create_enemies(ENEMY_ROWS, ENEMY_COLS)
        self.projectiles = []          # снаряды первого игрока (или одиночного)
        self.enemy_projectiles = []    # снаряды врагов
        if self.mode == 'two':
            self.projectiles2 = []     # снаряды второго игрока

        # Уровень и счёт
        self.level = Level(1)
        self.score_player1 = 0  # Счёт игрока 1
        self.score_player2 = 0  # Счёт игрока 2

        # Таймер для выстрелов врагов – увеличена частота (700 мс)
        self.enemy_shoot_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_shoot_event, 700)

    def create_enemies(self, rows, cols):
        """
        Создает сетку врагов и возвращает список объектов Enemy.
        """
        enemies = []
        offset_x = 50
        offset_y = 50
        spacing_x = 80
        spacing_y = 50
        for row in range(rows):
            for col in range(cols):
                x = offset_x + col * spacing_x
                y = offset_y + row * spacing_y
                enemy = Enemy(x, y)
                enemies.append(enemy)
        return enemies

    def process_events(self):
        """
        Обрабатывает входные события.
        В режиме двух игроков:
          - Игрок 1 стреляет пробелом.
          - Игрок 2 стреляет клавишей Enter.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.mode == 'single':
                    save_record(self.player1_name, self.score_player1)
                else:
                    save_record("P1: " + self.player1_name, self.score_player1)
                    save_record("P2: " + self.player2_name, self.score_player2)
                self.running = False
            elif event.type == self.enemy_shoot_event:
                if self.enemies:
                    shooter = random.choice(self.enemies)
                    proj = shooter.shoot()
                    if proj:
                        self.enemy_projectiles.append(proj)
                        self.sound_laser.play()  # звук выстрела врага
            elif event.type == pygame.KEYDOWN:
                if self.mode == 'single':
                    if event.key == pygame.K_SPACE:
                        proj = self.player.shoot()
                        if proj:
                            self.projectiles.append(proj)
                            self.sound_laser.play()  # звук выстрела игрока
                else:
                    if event.key == pygame.K_SPACE:
                        proj = self.player1.shoot()
                        if proj:
                            self.projectiles.append(proj)
                            self.sound_laser.play()
                    if event.key == pygame.K_RETURN:
                        proj2 = self.player2.shoot()
                        if proj2:
                            self.projectiles2.append(proj2)
                            self.sound_laser.play()

    def update(self):
        """
        Обновляет состояния всех игровых объектов.
        """
        keys = pygame.key.get_pressed()
        if self.mode == 'single':
            self.player.move(keys)
            self.player.update()
        else:
            # Игрок 1 (WASD)
            if keys[pygame.K_a]:
                self.player1.move_left()
            if keys[pygame.K_d]:
                self.player1.move_right()
            if keys[pygame.K_w]:
                self.player1.move_up()
            if keys[pygame.K_s]:
                self.player1.move_down()
            self.player1.update()
            # Игрок 2 (стрелки)
            if keys[pygame.K_LEFT]:
                self.player2.move_left()
            if keys[pygame.K_RIGHT]:
                self.player2.move_right()
            if keys[pygame.K_UP]:
                self.player2.move_up()
            if keys[pygame.K_DOWN]:
                self.player2.move_down()
            self.player2.update()

        for enemy in self.enemies:
            enemy.update()

        if self.mode == 'single':
            for proj in self.projectiles:
                proj.update()
            self.projectiles = [p for p in self.projectiles if p.is_on_screen(SCREEN_HEIGHT)]
        else:
            for proj in self.projectiles:
                proj.update()
            self.projectiles = [p for p in self.projectiles if p.is_on_screen(SCREEN_HEIGHT)]
            for proj in self.projectiles2:
                proj.update()
            self.projectiles2 = [p for p in self.projectiles2 if p.is_on_screen(SCREEN_HEIGHT)]

        for proj in self.enemy_projectiles:
            proj.update()
        self.enemy_projectiles = [p for p in self.enemy_projectiles if p.is_on_screen(SCREEN_HEIGHT)]

        self.check_collisions()

        # Если враги опускаются ниже уровня игроков – завершаем игру
        for enemy in self.enemies:
            if self.mode == 'single':
                if enemy.y + enemy.height >= self.player.y:
                    self.sound_explosion.play()  # звук смерти игрока
                    save_record(self.player1_name, self.score_player1)
                    self.running = False
                    return
            else:
                if enemy.y + enemy.height >= min(self.player1.y, self.player2.y):
                    self.sound_explosion.play()
                    save_record("P1: " + self.player1_name, self.score_player1)
                    save_record("P2: " + self.player2_name, self.score_player2)
                    self.running = False
                    return

    def check_collisions(self):
        """
        Проверяет столкновения снарядов с врагами и врагов с кораблями игроков.
        """
        if self.mode == 'single':
            for proj in self.projectiles[:]:
                for enemy in self.enemies[:]:
                    if proj.rect.colliderect(enemy.rect):
                        self.projectiles.remove(proj)
                        self.enemies.remove(enemy)
                        self.score_player1 += 10  # Очки для игрока 1
                        self.sound_explosion.play()  # Воспроизводим звук взрыва
                        break
            for proj in self.enemy_projectiles[:]:
                if proj.rect.colliderect(self.player.rect):
                    self.enemy_projectiles.remove(proj)
                    self.player.lives -= 1
                    if self.player.lives > 0:
                        self.sound_hit.play()
                    else:
                        self.sound_explosion.play()
                        save_record(self.player1_name, self.score_player1)
                        self.running = False
        else:
            for proj in self.projectiles[:]:
                for enemy in self.enemies[:]:
                    if proj.rect.colliderect(enemy.rect):
                        self.projectiles.remove(proj)
                        self.enemies.remove(enemy)
                        self.score_player1 += 10  # Очки для игрока 1
                        self.sound_explosion.play()
                        break
            for proj in self.projectiles2[:]:
                for enemy in self.enemies[:]:
                    if proj.rect.colliderect(enemy.rect):
                        self.projectiles2.remove(proj)
                        self.enemies.remove(enemy)
                        self.score_player2 += 10  # Очки для игрока 2
                        self.sound_explosion.play()
                        break
            # Обработка попаданий врагов по игрокам
            for proj in self.enemy_projectiles[:]:
                collided1 = proj.rect.colliderect(self.player1.rect)
                collided2 = proj.rect.colliderect(self.player2.rect)
                if collided1 or collided2:
                    # Удаляем снаряд, попавший в кого-либо
                    self.enemy_projectiles.remove(proj)
                    if collided1:
                        self.player1.lives -= 1
                    if collided2:
                        self.player2.lives -= 1
                    # Если у хотя бы одного игрока жизни закончились, сохраняем оба результата и завершаем игру
                    if self.player1.lives <= 0 or self.player2.lives <= 0:
                        self.sound_explosion.play()
                        save_record(f"P1: {self.player1_name}", self.score_player1)
                        save_record(f"P2: {self.player2_name}", self.score_player2)
                        self.running = False
                    else:
                        self.sound_hit.play()

    def render(self):
        """
        Отрисовывает все игровые объекты и интерфейс.
        """
        self.screen.fill(BLACK)
        draw_records(self.screen)
        
        if self.mode == 'single':
            self.player.draw(self.screen)
        else:
            self.player1.draw(self.screen)
            self.player2.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        if self.mode == 'single':
            for proj in self.projectiles:
                proj.draw(self.screen)
        else:
            for proj in self.projectiles:
                proj.draw(self.screen)
            for proj in self.projectiles2:
                proj.draw(self.screen)

        for proj in self.enemy_projectiles:
            proj.draw(self.screen)

        info_font = pygame.font.SysFont('Arial', 24)
        info_texts = [
            f"Очки P1: {self.score_player1}",
            f"Очки P2: {self.score_player2}" if self.mode == 'two' else f"Очки: {self.score_player1}",
            f"Уровень: {self.level.number}"
        ]
        if self.mode == 'two':
            info_texts.append(f"P1 Жизни: {self.player1.lives}   P2 Жизни: {self.player2.lives}")
        else:
            info_texts.append(f"Жизни: {self.player.lives}")
            
        y_offset = 10
        for text in info_texts:
            rendered = info_font.render(text, True, WHITE)
            self.screen.blit(rendered, (SCREEN_WIDTH - rendered.get_width() - 10, y_offset))
            y_offset += rendered.get_height() + 5

        pygame.display.flip()

    def run(self):
        """
        Основной игровой цикл.
        """
        while self.running:
            self.clock.tick(FPS)
            self.process_events()
            self.update()
            self.render()

            if not self.enemies:
                self.level.next_level()
                self.enemies = self.create_enemies(ENEMY_ROWS, ENEMY_COLS)
                for enemy in self.enemies:
                    enemy.speed += self.level.number * 0.5
                # Увеличиваем скорость выстрела врагов на следующем уровне
                pygame.time.set_timer(self.enemy_shoot_event, max(700 - self.level.number * 50, 100))
                self.score_player1 += 50  # Добавляем бонус за переход на новый уровень
                self.score_player2 += 50  # Для второго игрока тоже добавляем

        self.game_over()

    def game_over(self):
        """
        Отображает экран "Game Over" с финальным счётом.
        """
        game_over_font = pygame.font.SysFont('Arial', 48)
        game_over_text = game_over_font.render("GAME OVER", True, RED)
        final_score_text = self.font.render(f"Окончательный результат P1: {self.score_player1}  P2: {self.score_player2}", True, WHITE)
        self.screen.fill(BLACK)
        self.screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2,
                                          (SCREEN_HEIGHT - game_over_text.get_height()) // 2))
        self.screen.blit(final_score_text, ((SCREEN_WIDTH - final_score_text.get_width()) // 2,
                                            (SCREEN_HEIGHT - final_score_text.get_height()) // 2 + 60))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    # Здесь может быть запуск игры (например, из main.py)
    pass
