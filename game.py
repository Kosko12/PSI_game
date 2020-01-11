import random
import sys
import threading
import time

import pygame
import Objects.Player
# initializers
pygame.init()
random.seed()

screen = pygame.display.set_mode((800, 600))
maxXpos = 780
maxYpos = 780
pygame.display.set_caption("Test gra")

arrows = []
playerImg = pygame.image.load('ludek.png')
playerX = 370
playerY = 566
arrowX = random.randrange(800)
arrowY = 0
arrowExist = True
playerXchange = 0
arrowYchange = 3


def show_player(p, x, y):
    playerImg = pygame.image.load(p.image)
    p.update(x, y)
    # p.print_self()
    screen.blit(playerImg, (x, y))


def if_in_range(p, a):
    for i in range(p.x, p.x + p.xRange):
        if a.x == i and (arrow.y == p.y - p.yRange or a.y > p.y - p.yRange):
            return True
    return False


def load_player():
    pl = Objects.Player.Player(playerX, playerY, 84, 31, 'ludek.png')
    return pl
# player = Objects.Player.Player(playerX, playerY, 84, 31, 'ludek.png')
arrow = Objects.Player.Player(arrowX, arrowY, 18, 28, 'arrow.png')
# print(player.image)
ifExit = False


def load_arrow(timeGap):
    while True:

        xPos = random.randrange(800)
        arrows.append(Objects.Player.Player(xPos, 0, 18, 28, 'arrow.png'))
        if timeGap >= .55:
            timeGap -= .25
        print(timeGap)
        print(len(arrows))
        time.sleep(timeGap)
# main function
# loading player


player = load_player()
thr = threading.Thread(target=load_arrow, args=(4,), daemon=True)
thr.start()
while not ifExit:
    # screen.fill((255, 255, 255))
    screen.blit(pygame.image.load('bg.png'), [0, 0])
    # playerX += 0.3
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ifExit = True
        elif event.type == pygame.KEYDOWN:
            print("keystoroke pressed")
            print(event.type)
            if event.key == pygame.K_RIGHT:
                playerXchange = 2
                print("Key right")
            elif event.key == pygame.K_LEFT:
                playerXchange = -2
                print("Key left")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerXchange = 0
    player.x += playerXchange

    show_player(player, player.x, player.y)
    if player.x <= 0:
        player.x = 0
    elif player.x >= 716:
        player.x = 715
    for arr in arrows:
        arr.y += arrowYchange
        if arr.y < 600:
            show_player(arr, arr.x, arr.y)
        if if_in_range(player, arr) and arr.y <= 600:
            ifExit = True
            pygame.quit()
            sys.exit()
        elif arr.y > 600:
            arrows.remove(arr)
            print("Arrow removed!")

    #if arrowY < 600:
    #    showPlayer(arrow, arrowX, arrowY)
    #elif arrowY >= 600:
    #    del arrow
    #if ifInRange(player, arrow) and arrowY <= 600:
    #    ifExit = True
    #    pygame.quit()
    #    sys.exit()
    pygame.display.update()
