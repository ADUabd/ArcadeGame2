import subprocess
import sys
import get_pip


def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])


try:
    print("[GAME] Trying to import pygame")
    import pygame
except:
    print("[EXCEPTION] Pygame not installed")

    try:
        print("[GAME] Trying to install pygame via pip")
        import pip

        install("pygame")
        print("[GAME] Pygame has been installed")
    except:
        print("[EXCEPTION] Pip not installed on system")
        print("[GAME] Trying to install pip")
        get_pip.main()
        print("[GAME] Pip has been installed")
        try:
            print("[GAME] Trying to install pygame")
            import pip

            install("pygame")
            print("[GAME] Pygame has been installed")
        except:
            print("[ERROR 1] Pygame could not be installed")

import pygame
import os
from client import Network

pygame.font.init()

board = pygame.transform.scale(pygame.image.load(os.path.join("img", "board_alt.png")), (750, 750))
chessbg = pygame.transform.scale(pygame.image.load(os.path.join("img", "chessbg.png")), (750, 750))
rect = (113, 113, 525, 525)

turn = "w"


def menu_screen(win, name):
    global bo, chessbg
    run = True
    offline = False

    while run:
        win.blit(chessbg, (0, 0))
        small_font = pygame.font.SysFont("Press Start 2P", 50)

        if offline:
            off = small_font.render("Server Offline, Try Again Later...", 1, (255, 0, 0))
            win.blit(off, (width / 2 - off.get_width() / 2, 500))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                offline = False
                try:
                    bo = connect()
                    run = False
                    main()
                    break
                except:
                    print("Server Offline")
                    offline = True


def redraw_gameWindow(win, bo, p1, p2, color, ready):
    win.blit(board, (0, 0))
    bo.draw(win, color)

    formatTime1 = str(int(p1 // 60)) + ":" + str(int(p1 % 60))
    formatTime2 = str(int(p2 // 60)) + ":" + str(int(p2 % 60))
    if int(p1 % 60) < 10:
        formatTime1 = formatTime1[:-1] + "0" + formatTime1[-1]
    if int(p2 % 60) < 10:
        formatTime2 = formatTime2[:-1] + "0" + formatTime2[-1]

    font = pygame.font.SysFont("Press Start 2P", 30)
    try:
        txt = font.render(bo.p1Name + "\'s Time: " + str(formatTime2), 1, (52, 59, 41))
        txt2 = font.render(bo.p2Name + "\'s Time: " + str(formatTime1), 1, (52, 59, 41))
    except Exception as e:
        print(e)
    win.blit(txt, (520, 10))
    win.blit(txt2, (520, 700))

    txt = font.render("Press q to Quit", 1, (52, 59, 41))
    win.blit(txt, (10, 20))

    if color == "s":
        txt3 = font.render("SPECTATOR MODE", 1, (255, 0, 0))
        win.blit(txt3, (width / 2 - txt3.get_width() / 2, 10))

    if not ready:
        show = "Waiting for Player"
        if color == "s":
            show = "Waiting for Players"
        font = pygame.font.SysFont("Press Start 2P", 80)
        txt = font.render(show, 1, (52, 59, 41))
        win.blit(txt, (width / 2 - txt.get_width() / 2, 300))

    if not color == "s":
        font = pygame.font.SysFont("Press Start 2P", 30)
        if color == "w":
            txt3 = font.render("YOU ARE WHITE", 1, (52, 59, 41))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 10))
        else:
            txt3 = font.render("YOU ARE BLACK", 1, (52, 59, 41))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 10))

        if bo.turn == color:
            txt3 = font.render("YOUR TURN", 1, (52, 59, 41))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 700))
        else:
            txt3 = font.render("THEIR TURN", 1, (52, 59, 41))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 700))

    pygame.display.update()


def end_screen(win, text):
    pygame.font.init()
    font = pygame.font.SysFont("Press Start 2P", 80)
    txt = font.render(text, 1, (52, 59, 41))
    win.blit(txt, (width / 2 - txt.get_width() / 2, 300))
    pygame.display.update()

    pygame.time.set_timer(pygame.USEREVENT + 1, 3000)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False
            elif event.type == pygame.KEYDOWN:
                run = False
            elif event.type == pygame.USEREVENT + 1:
                run = False


def click(pos):
    """
    :return: pos (x, y) in range 0-7 0-7
    """
    x = pos[0]
    y = pos[1]
    if rect[0] < x < rect[0] + rect[2]:
        if rect[1] < y < rect[1] + rect[3]:
            divX = x - rect[0]
            divY = y - rect[1]
            i = int(divX / (rect[2] / 8))
            j = int(divY / (rect[3] / 8))
            return i, j

    return -1, -1


def connect():
    global n
    n = Network()
    return n.board


def main():
    global turn, bo, name

    color = bo.start_user
    count = 0

    bo = n.send("update_moves")
    bo = n.send("name " + name)
    clock = pygame.time.Clock()
    run = True

    while run:
        if not color == "s":
            p1Time = bo.time1
            p2Time = bo.time2
            if count == 60:
                bo = n.send("get")
                count = 0
            else:
                count += 1
            clock.tick(30)

        try:
            redraw_gameWindow(win, bo, p1Time, p2Time, color, bo.ready)
        except Exception as e:
            print(e)
            end_screen(win, "Other player left")
            run = False
            break

        if not color == "s":
            if p1Time <= 0:
                bo = n.send("winner b")
            elif p2Time <= 0:
                bo = n.send("winner w")

            if bo.check_mate("b"):
                bo = n.send("winner b")
            elif bo.check_mate("w"):
                bo = n.send("winner w")

        if bo.winner == "w":
            end_screen(win, "White is the Winner!")
            run = False
        elif bo.winner == "b":
            end_screen(win, "Black is the winner")
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and color != "s":
                    # quit game
                    if color == "w":
                        bo = n.send("winner b")
                    else:
                        bo = n.send("winner w")

                if event.key == pygame.K_RIGHT:
                    bo = n.send("forward")

                if event.key == pygame.K_LEFT:
                    bo = n.send("back")

            if event.type == pygame.MOUSEBUTTONUP and color != "s":
                if color == bo.turn and bo.ready:
                    pos = pygame.mouse.get_pos()
                    bo = n.send("update moves")
                    i, j = click(pos)
                    bo = n.send("select " + str(i) + " " + str(j) + " " + color)

    n.disconnect()
    bo = 0
    menu_screen(win)


def input_nicknames(mode):
    WIDTH, HEIGHT = 750, 750
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ввод никнеймов")
    font = pygame.font.SysFont("Arial", 46)
    clock = pygame.time.Clock()

    input_box1 = pygame.Rect(50, 100, 600, 64)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color(255, 255, 255)
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
                active2 = False
            elif event.type == pygame.KEYDOWN:
                if active1:
                    if event.key == pygame.K_RETURN:
                        if mode == 'single':
                            done = True
                    elif event.key == pygame.K_BACKSPACE:
                        nickname1 = nickname1[:-1]
                    else:
                        nickname1 += event.unicode

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        screen.fill((1, 50, 32))
        if mode == 'single':
            prompt = font.render("Введите никнейм:", True, (255, 255, 255))
            screen.blit(prompt, (200, 40))

        txt_surface1 = font.render(nickname1, True, color1)
        screen.blit(txt_surface1, (input_box1.x + 5, input_box1.y + 5))
        pygame.draw.rect(screen, color1, input_box1, 2)

        done_btn = pygame.Rect(270, 250, 160, 60)
        pygame.draw.rect(screen, pygame.Color(141, 182, 0), done_btn)
        done_text = font.render("Готово", True, (255, 255, 255))
        screen.blit(done_text, (done_btn.x + (done_btn.w - done_text.get_width()) // 2,
                                done_btn.y + (done_btn.h - done_text.get_height()) // 2))
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            mouse_pos = pygame.mouse.get_pos()
            if done_btn.collidepoint(mouse_pos):
                if mode == 'single' and nickname1.strip() != "":
                    done = True

        pygame.display.flip()
        clock.tick(30)

    if mode == 'single':
        if nickname1.strip() == "":
            nickname1 = "Player"
        return (nickname1)


name = input_nicknames('single')
width = 750
height = 750
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess Game")
menu_screen(win, name)
