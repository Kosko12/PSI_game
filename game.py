import random
import sys
import threading
import time
import numpy
import pygame
import Arrow
import Player
import StopableThread
import Map

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

lock = threading.Lock()

arrow_for_player = []
def if_in_danger(p):
    while collapse == False:
        global arrows
        left = 0
        right = 800
        lock.acquire()
        if len(arrows) > 5:
            for ar in arrows:
                if p.x - 1 <= ar.x and (p.x + p.xRange) + 1 > ar.x:
                    for a1 in arrows:
                        clRight, clLeft = get_closest(a1, arrows)
                        if if_match(clLeft, a1.x, p.x + p.xRangex):
                            if p.x > clLeft:
                                p.speed = -1 * p.maxSpeed

                        elif if_match(a1.x, clRight, p.x + p.xRangex):
                            if p.x < clRight:
                                p.speed = 1 * p.maxSpeed

                else:
                    p.speed = 0
            lock.release()
        else:
            for ar in arrows:
                if p.x - 1 <= ar.x and (p.x + p.xRange) + 1 > ar.x:
                    for closest in arrows:
                        if closest != ar:
                            if closest.x < ar.x:
                                if closest.x > left:
                                    left = closest.x
                            else:
                                if closest.x < right:
                                    right = closest.x
                        else:
                            if p.speed == 0:
                                if 800 - p.x < p.x + p.xRange:
                                    p.speed = -1. * p.maxSpeed
                                else:
                                    p.speed = p.maxSpeed
                    if if_match(ar.x, right, p.x + p.xRange):
                        if p.speed <= 0:
                            p.speed = p.maxSpeed
                    elif if_match(left, ar.x, p.x + p.xRange):
                        if p.speed >= 0:
                            p.speed = -1. * p.maxSpeed
                else:
                    p.speed = 0
            lock.release()
# fun showing element

def get_closest(a, arrow):
    left = 0
    right = 800
    if len(arrows) > 2:
        for ar in arrows:
            for closest in arrows:
                if closest != ar:
                    if closest.x < ar.x:
                        if closest.x > left:
                            left = closest
                    else:
                        if closest.x < right:
                            right = closest
        return left, right
def if_match(x_o, x_k, r):
    sub = x_k - x_o
    if sub > r:
        return True
    return False

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
    pl = Player.Player(x_pos, playerY, 84., 31., 'ludek.png', random.uniform(1.5, 2.))
    return pl


arrow = Arrow.Arrow(arrowX, arrowY, 18., 28., 'arrow.png')



collapse = False

def load_arrow(timeGap):
    checker = True
    while checker:
        lock.acquire()
        xPos = random.randrange(800)
        ar = Arrow.Arrow(xPos, 0., 18., 28., 'arrow.png')
        arrows.append(ar)
        if timeGap >= .55:
            timeGap -= .25
        lock.release()
        #print(timeGap)
        #print(len(arrows))
        time.sleep(timeGap)
        if collapse:
            checker = False
# main function
# loading players in amount of declared population


population = 2
generations = 4

player = []
thread = StopableThread.StopableThread(target=load_arrow, args=(4,), daemon=True)


# program loop
def main(thr):
    ifExit = False
    global collapse
    collapse = False
    global player
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
            threading.Thread(target=if_in_danger, args=(xp,), daemon=True).start()
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
                    for pl in player:
                        player.remove(pl)
                    generations = generations - 1
                    main(StopableThread.StopableThread(target=load_arrow, args=(4,), daemon=True))

                else:
                    collapse = True
                    thr.join()
                    pygame.quit()
                    sys.exit()
            elif arr.y > 600:
                arrows.remove(arr)
                #print("Arrow removed!")

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
