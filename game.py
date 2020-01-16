import random
import sys
import threading
import time
import numpy
import pygame
import Arrow
import Player
import StopableThread

# initializers

pygame.init()
random.seed()

# screen positions

screen = pygame.display.set_mode((800, 600))
maxXpos = 780
maxYpos = 780
pygame.display.set_caption("Test gra")

# arrow and players basic data

arrows = []
playerImg = pygame.image.load('ludek.png')
playerX = 370.
playerY = 566.
arrowX = random.randrange(800)
arrowY = 0
arrowExist = True
playerXchange = 0
arrowYchange = 3

# fun showing element


def show_player(p, x, y):

    playerImg = pygame.image.load(p.image)
    p.update(x, y)
    # p.print_self()
    screen.blit(playerImg, (x, y))

# fun which checks if collision has happened


def if_in_range(p, a):

    for e in p:
        for i in range(int(e.x), int(e.x + e.xRange)):
            if int(a.x) == i and (arrow.y == e.y - e.yRange or a.y > e.y - e.yRange):
                return True
    return False

# fun which loads arrows/players


def load_player(x_pos):
    pl = Player.Player(x_pos, playerY, 84., 31., 'ludek.png', random.uniform(-0.2, 0.2))
    return pl


arrow = Arrow.Arrow(arrowX, arrowY, 18., 28., 'arrow.png')



collapse = False

def load_arrow(timeGap):
    checker = True
    while checker:

        xPos = random.randrange(800)
        arrows.append(Arrow.Arrow(xPos, 0., 18., 28., 'arrow.png'))
        if timeGap >= .55:
            timeGap -= .25
        print(timeGap)
        print(len(arrows))
        time.sleep(timeGap)
        if collapse:
            checker = False
# main function
# loading players in amount of declared population


population = 10
generations = 5


thread = StopableThread.StopableThread(target=load_arrow, args=(4,), daemon=True)


# program loop
def main(thr):
    ifExit = False
    global collapse
    collapse = False
    player = []
    for x in range(population):
        player.append(load_player(random.uniform(0., 800.)))
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
        for xp in player:
            xp.x += xp.speed
            show_player(xp, xp.x, xp.y)
            if xp.x <= 0:
                xp.x = 0
            elif xp.x >= 716:
                xp.x = 715

        global generations
        for arr in arrows:
            arr.y += arrowYchange
            if arr.y < 600:
                show_player(arr, arr.x, arr.y)
            if if_in_range(player, arr) and arr.y <= 600:
                if generations > 0:


                    collapse = True
                    thr.join()
                    for ar in arrows:
                        arrows.remove(ar)
                    generations = generations - 1
                    main(StopableThread.StopableThread(target=load_arrow, args=(4,), daemon=True))

                else:
                    collapse = True
                    thr.join()
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


main(thread)
