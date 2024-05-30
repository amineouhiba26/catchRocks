from gameTextUpdateMethods import gameTextUpdateMethods
import pygame
from player import Player
from Rock import Rock
import random
from constValue import *

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/sound/backgrpund.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=1, fade_ms=500)

bg = pygame.image.load("assets/images/backgroundResized.png")


def gamePausedLogic():
    global gamePaused
    gameTextUpdateMethods.draw_paused(screen)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_o]:
        gamePaused = False


def gameWonLogic():
    global gamePaused
    global someoneWon
    global running
    gameTextUpdateMethods.draw_restart_prompt(screen)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        reset_game(player1, player2, rocks)
        gamePaused = False
        someoneWon = False
    elif keys[pygame.K_ESCAPE]:
        running = False


def spawn_rock():
    global rocks
    x = random.randint(0+32, screenWidth-32)
    rock = Rock(x, 0, 64, 64)
    rocks.append(rock)


def spawn_rockOld():
    global rocks
    freeInterval = []
    rocks.sort(key=lambda rock: rock.rockRect.left)

    if (len(rocks) == 0):
        rock = Rock(random.randint(64, screenWidth - 64), 0, 64, 64)
        rocks.append(rock)
        return

    for index, rock in enumerate(rocks):
        leftSide = rock.rockRect.left
        if (index == 0 and leftSide > (rock.width * 1.6)):
            freeInterval.append([0, leftSide])
        else:
            prevRockRightSide = rocks[index-1].rockRect.right
            distance = abs(leftSide-prevRockRightSide)
            if (distance > (rock.width * 1.6)):
                freeInterval.append([prevRockRightSide, leftSide])

    if abs(rocks[-1].rockRect.right - screenWidth) > 64 * 1.6:
        freeInterval.append([rocks[-1].rockRect.right, screenWidth])

    if (len(freeInterval) == 0):
        rock = Rock(random.randint(64, screenWidth - 64), 0, 64, 64)
        rocks.append(rock)
        return

    radomChoice = random.choice(freeInterval)
    x1, x2 = radomChoice[0], radomChoice[1]
    print(radomChoice)

    if (x2 > x1):
        x = random.randint(x1+32, x2-32)
    else:
        x = random.randint(x2, x1)

    rock = Rock(x, 0, 64, 64)
    rocks.append(rock)


def reset_game(player1: Player, player2: Player, rocks):
    player1.score = 0
    player2.score = 0
    player1.resetPlayerPos()
    player2.resetPlayerPos()
    for rock in rocks:
        rocks.remove(rock)


def mainGameLogic1Player():
    global gamePaused
    global someoneWon
    global timeSinceLastSpawn
    # Check for player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:  # MOVE LEFT
        player1.moveRightPlayer(screenWidth)
    if keys[pygame.K_q]:  # MOVE RIGHT
        player1.moveLeftPlayer()
    if keys[pygame.K_p]:
        gamePaused = True
        gameTextUpdateMethods.draw_paused(screen)

    # Fill background
    screen.blit(bg, (0, 0))

    #  check for not inscreen rocks
    for rock in rocks:
        # rock.draw(screen)
        rock.Fall()
        if rock.rockRect.top > screenHeight:
            rocks.remove(rock)
            continue

        # check for rock colission
        if player1.detectCollision(rock.rockRect):
            rocks.remove(rock)
            player1.score += scoreIncerement

    screen.blits([(rock.rockImg, rock.rockRect) for rock in rocks])
    if len(rocks) < 5 and timeSinceLastSpawn > spawnTimer:
        timeSinceLastSpawn = 0
        spawn_rock()

    player1.drawPlayer(screen)

    gameTextUpdateMethods.updatePlayer1Score(
        font, screen, player1.score, f"{player1.name} Score")

    if player1.score >= scoreToWin:
        gameTextUpdateMethods.draw_winner(screen, player1.name)
        someoneWon = True


def mainGameLogic2Players():
    global gamePaused
    global someoneWon
    global timeSinceLastSpawn
    # Check for player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:  # MOVE LEFT
        player1.moveRightPlayer(screenWidth)
    if keys[pygame.K_q]:  # MOVE RIGHT
        player1.moveLeftPlayer()
    if keys[pygame.K_RIGHT]:
        player2.moveRightPlayer(screenWidth)
    if keys[pygame.K_LEFT]:
        player2.moveLeftPlayer()
    if keys[pygame.K_p]:
        gamePaused = True
        gameTextUpdateMethods.draw_paused(screen)

    # Fill background
    screen.blit(bg, (0, 0))

    #  check for not inscreen rocks
    for rock in rocks:
        # rock.draw(screen)
        rock.Fall()
        if rock.rockRect.top > screenHeight:
            rocks.remove(rock)
            continue

        # check for rock colission
        if player1.detectCollision(rock.rockRect):
            rocks.remove(rock)
            player1.score += scoreIncerement
        elif player2.detectCollision(rock.rockRect):
            rocks.remove(rock)
            player2.score += scoreIncerement

    # screen.blits(rockToBlit)
    screen.blits([(rock.rockImg, rock.rockRect) for rock in rocks])
    if len(rocks) < 5 and timeSinceLastSpawn > spawnTimer:
        timeSinceLastSpawn = 0
        spawn_rock()

    player1.drawPlayer(screen)
    player2.drawPlayer(screen)

    gameTextUpdateMethods.updatePlayer1Score(
        font, screen, player1.score, f"{player1.name} Score")
    gameTextUpdateMethods.updatePlayer2Score(
        font, screen, player2.score, f"{player2.name} Score")

    if player1.score >= scoreToWin:
        gameTextUpdateMethods.draw_winner(screen, player1.name)
        someoneWon = True

    elif player2.score >= scoreToWin:
        gameTextUpdateMethods.draw_winner(screen, player2.name)
        someoneWon = True


def button_create(text, rect, inactive_color, active_color, action):

    font = pygame.font.Font(None, 40)

    button_rect = pygame.Rect(rect)
    button_rect.centerx = screenWidth//2
    textSurface = font.render(text, True, (0, 0, 0))
    text_rect = textSurface.get_rect(center=button_rect.center)

    return [textSurface, text_rect, button_rect, inactive_color, active_color, action, False, text]


def button_draw(screen, info):

    text, text_rect, rect, inactive_color, active_color, action, hover, textStrign = info

    if hover:
        color = active_color
    else:
        color = inactive_color

    pygame.draw.rect(screen, color, rect)
    screen.blit(text, text_rect)


def on_click_button_1():
    global mode
    global showMenu
    global player1
    print('You clicked Button 1')
    mode = "1player"
    showMenu = False
    player1.name = "player 1"


def on_click_button_2():
    global mode
    global showMenu
    print('You clicked Button 2')
    mode = "playername"
    showMenu = False


def on_click_button_3():
    print('You clicked Button 3')
    global mode
    global input1Focused
    global input2Focused
    input2Focused = False
    input1Focused = True


def on_click_button_4():
    global mode
    global input1Focused
    global input2Focused
    input1Focused = False
    input2Focused = True


def on_click_button_5():
    global mode
    global input1Focused
    global input2Focused
    global player1
    global player2
    global player1input
    global player2input
    input2Focused = False
    input1Focused = False
    mode = "2player"
    player1.name = player1input[-1]
    player2.name = player2input[-1]

    if (player1.name == "player1 name" or player1.name == ""):
        player1.name = "player 1"
    if (player2.name == "player2 name" or player1.name == ""):
        player2.name = "player 2"


def button_check(info, event):

    text, text_rect, rect, inactive_color, active_color, action, hover, textstring = info

    if event.type == pygame.MOUSEMOTION:
        # hover = True/False
        info[-2] = rect.collidepoint(event.pos)

    elif event.type == pygame.MOUSEBUTTONDOWN:
        if hover and action:
            action()


screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
player1 = Player(height=100)
player2 = Player(height=100)
font = pygame.font.Font(None, 36)
rocks: list[Rock] = []

showMenu = True
someoneWon = False
gamePaused = False
running = True
timeSinceLastSpawn = 300
mode = None
input1Focused = False
input2Focused = False


player1btn = button_create("1 player", (screenWidth//2, screenHeight//2 - 60, 200, 75),
                           (255, 255, 0), (0, 255, 0), on_click_button_1)

player2btn = button_create("2 player", (screenWidth//2, screenHeight//2 + 40, 200, 75),
                           (255, 255, 0), (0, 255, 0), on_click_button_2)

player1input = button_create("player1 name", (screenWidth//2, screenHeight//2 - 100, 200, 75),
                             (255, 255, 0), (0, 255, 0), on_click_button_3)

player2input = button_create("player2 name", (screenWidth//2, screenHeight//2, 200, 75),
                             (255, 255, 0), (0, 255, 0), on_click_button_4)

playPlayer2Mode = button_create("Play", (screenWidth//2, screenHeight//2 + 100, 200, 75),
                                (255, 255, 0), (0, 255, 0), on_click_button_5)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if (showMenu == True):
            button_check(player1btn, event)
            button_check(player2btn, event)
        if (mode == "playername"):
            button_check(player1input, event)
            button_check(player2input, event)
            button_check(playPlayer2Mode, event)

        if event.type == pygame.KEYDOWN and (input1Focused or input2Focused):
            if (input1Focused):
                text = player1input[-1]
                if (text == "player1 name"):
                    text = ""
            else:
                text = player2input[-1]
                if (text == "player2 name"):
                    text = ""

            if event.key == pygame.K_RETURN:
                input2Focused = False
                input1Focused = False
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += event.unicode
            if (input1Focused):
                player1input = button_create(text, (screenWidth//2, screenHeight//2 - 100, 200, 75),
                                             (255, 255, 0), (0, 255, 0), on_click_button_3)
            else:
                player2input = button_create(text, (screenWidth//2, screenHeight//2 + 0, 200, 75),
                                             (255, 255, 0), (0, 255, 0), on_click_button_4)

    if (showMenu == True):
        screen.blit(bg, (0, 0))
        button_draw(screen, player1btn)
        button_draw(screen, player2btn)
    else:
        if (someoneWon == True or gamePaused == True):
            if (someoneWon):
                gameWonLogic()
            elif (gamePaused):
                gamePausedLogic()
        else:
            if (mode == "playername"):
                screen.blit(bg, (0, 0))
                button_draw(screen, player1input)
                button_draw(screen, player2input)
                button_draw(screen, playPlayer2Mode)
            elif (mode == "2player"):
                mainGameLogic2Players()
            else:
                mainGameLogic1Player()
    pygame.display.flip()
    dt = clock.tick()
    timeSinceLastSpawn += dt


pygame.quit()
