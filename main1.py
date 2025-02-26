"""
Точка входа в игру.

Этот модуль инициализирует Pygame, сначала показывает экран выбора режима, а затем – экран ввода никнеймов:
- Для одиночного режима показывается одно поле ввода.
- Для двухпользовательского режима – два поля ввода для никнеймов первого и второго игроков.
После ввода настроек создаётся объект игры с соответствующими параметрами.
"""

import pygame
from games import Game


def choose_mode():
    """
    Отображает экран выбора режима игры.
    Возвращает выбранный режим: 'single' или 'two'.
    """
    WIDTH, HEIGHT = 500, 300
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Выбор режима")
    font = pygame.font.SysFont("Arial", 24)
    clock = pygame.time.Clock()

    # Кнопки выбора режима
    single_btn = pygame.Rect(50, 100, 180, 50)
    two_btn = pygame.Rect(270, 100, 180, 50)
    mode = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if single_btn.collidepoint(event.pos):
                    mode = 'single'
                    running = False
                elif two_btn.collidepoint(event.pos):
                    mode = 'two'
                    running = False

        screen.fill((40, 40, 40))
        title = font.render("Выберите режим игры", True, (255, 255, 255))
        screen.blit(title, ((WIDTH - title.get_width()) // 2, 30))

        pygame.draw.rect(screen, pygame.Color('gray20'), single_btn)
        pygame.draw.rect(screen, pygame.Color('gray20'), two_btn)
        single_text = font.render("Одиночный режим", True, (255, 255, 255))
        two_text = font.render("Двух игроков", True, (255, 255, 255))
        screen.blit(single_text, (single_btn.x + (single_btn.w - single_text.get_width()) // 2,
                                  single_btn.y + (single_btn.h - single_text.get_height()) // 2))
        screen.blit(two_text, (two_btn.x + (two_btn.w - two_text.get_width()) // 2,
                               two_btn.y + (two_btn.h - two_text.get_height()) // 2))
        pygame.display.flip()
        clock.tick(30)
    return mode


def input_nicknames(mode):
    """
    Отображает окно ввода никнеймов.
    Если mode == 'single' – запрашивает один никнейм (для одиночного режима).
    Если mode == 'two' – запрашивает два никнейма (для первого и второго игроков).
    Возвращает кортеж с введёнными никнеймами.
    """
    WIDTH, HEIGHT = 500, 350
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ввод никнеймов")
    font = pygame.font.SysFont("Arial", 24)
    clock = pygame.time.Clock()

    input_box1 = pygame.Rect(50, 80, 400, 32)
    input_box2 = pygame.Rect(50, 160, 400, 32) if mode == 'two' else None
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color1 = color_inactive
    color2 = color_inactive if mode == 'two' else None
    active1 = False
    active2 = False
    nickname1 = ""
    nickname2 = ""
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active1 = True
                else:
                    active1 = False
                color1 = color_active if active1 else color_inactive
                if mode == 'two' and input_box2.collidepoint(event.pos):
                    active2 = True
                else:
                    active2 = False
                if mode == 'two':
                    color2 = color_active if active2 else color_inactive
            elif event.type == pygame.KEYDOWN:
                if active1:
                    if event.key == pygame.K_RETURN:
                        if mode == 'single':
                            done = True
                    elif event.key == pygame.K_BACKSPACE:
                        nickname1 = nickname1[:-1]
                    else:
                        nickname1 += event.unicode
                if mode == 'two' and active2:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        nickname2 = nickname2[:-1]
                    else:
                        nickname2 += event.unicode
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        screen.fill((30, 30, 30))
        if mode == 'single':
            prompt = font.render("Введите никнейм:", True, (255, 255, 255))
            screen.blit(prompt, (50, 40))
        else:
            prompt1 = font.render("Никнейм 1 игрока:", True, (255, 255, 255))
            prompt2 = font.render("Никнейм 2 игрока:", True, (255, 255, 255))
            screen.blit(prompt1, (50, 40))
            screen.blit(prompt2, (50, 120))

        txt_surface1 = font.render(nickname1, True, color1)
        screen.blit(txt_surface1, (input_box1.x+5, input_box1.y+5))
        pygame.draw.rect(screen, color1, input_box1, 2)
        if mode == 'two':
            txt_surface2 = font.render(nickname2, True, color2)
            screen.blit(txt_surface2, (input_box2.x+5, input_box2.y+5))
            pygame.draw.rect(screen, color2, input_box2, 2)

        done_btn = pygame.Rect(WIDTH//2 - 60, 250, 120, 40)
        pygame.draw.rect(screen, pygame.Color('gray20'), done_btn)
        done_text = font.render("Готово", True, (255, 255, 255))
        screen.blit(done_text, (done_btn.x + (done_btn.w - done_text.get_width())//2,
                                done_btn.y + (done_btn.h - done_text.get_height())//2))
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            mouse_pos = pygame.mouse.get_pos()
            if done_btn.collidepoint(mouse_pos):
                if mode == 'single' and nickname1.strip() != "":
                    done = True
                if mode == 'two' and nickname1.strip() != "" and nickname2.strip() != "":
                    done = True

        pygame.display.flip()
        clock.tick(30)

    if mode == 'single':
        if nickname1.strip() == "":
            nickname1 = "Player"
        return (nickname1, )
    else:
        if nickname1.strip() == "":
            nickname1 = "Player1"
        if nickname2.strip() == "":
            nickname2 = "Player2"
        return (nickname1, nickname2)


def main():
    pygame.init()
    mode = choose_mode()
    print(mode)
    names = input_nicknames(mode)

    # После ввода настроек создаём основное окно игры
    pygame.display.set_mode((800, 600))

    game = Game(*names, mode=mode)
    game.run()


if __name__ == '__main__':
    main()