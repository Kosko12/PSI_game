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
players = []
generation_players = []
arrows = []
playerImg = pygame.image.load('ludek.png')
playerY = 566.
arrowYchange = 3

lock = threading.Lock()
busy = {}
arrow_for_player = []

population = 8
generations = 65
gen_counter = 1
###########################################################################


def mutate(x, y, z):
    xmodifier = random.uniform(0.1, 0.5)
    ymodifier = random.uniform(0.1, 0.5)
    zmodifier = random.uniform(0.1, 0.5)
    return xmodifier + x, y + ymodifier, z + zmodifier


def get_best_genes(players):
    tmp_pl = []
    for x in players:
        tmp_pl.append(x)
    to_ret = []
    guard = tmp_pl[0]
    val = 0

    for i in range(4):
        for p1 in tmp_pl:
            if p1.fitness > val:
                guard = p1
        to_ret.append(guard)
        tmp_pl.remove(guard)

    return to_ret


def cross(tab):
    parents = []
    for i in range(2):
        choice = random.randrange(1, 4)
        if choice == 1:
            parents.append(tab[0])
        elif choice == 2:
            parents.append(tab[1])
        elif choice == 3:
            parents.append(tab[2])
        elif choice == 4:
            parents.append(tab[3])
    kid_speed = (0.5 * parents[0].gene.max_speed) + (0.5 * parents[1].gene.max_speed)
    kid_x = (0.5 * parents[0].gene.x_orientation) + (0.5 * parents[1].gene.x_orientation)
    kid_y = (0.5 * parents[0].gene.y_orientation) + (0.5 * parents[1].gene.y_orientation)
    if_mutate = random.randrange(10)
    if if_mutate < 2:
        kid_speed, kid_x, kid_y = mutate(kid_speed, kid_x, kid_y)
    return Player.Player.Gene(kid_speed, kid_x, kid_y)

###########################################################################


def if_in_danger(p):
    while not collapse:
        lock.acquire()
        loc_a = arrows
        lock.release()
        leftx = 1
        lefty = 1
        rightx = 800
        righty = 1
        guard = False
        if_moving = False
        danger = p.fear.curr_dng
        prev_dng = p.fear.prev_dng
        for ar in loc_a:
            if if_moving == False:
                if p.x - 1 <= ar.x and (p.x + p.xRange) + 1 > ar.x:
                    if_moving = True
                    guard = 1
                    busy.update({p: 1})
                    for closest in loc_a:
                        if closest != ar:
                            if closest.x < ar.x:
                                if closest.x > leftx:
                                    leftx = closest.x
                                    lefty = closest.y
                            else:
                                if closest.x < rightx:
                                    rightx = closest.x
                                    righty = closest.y
                    l_attr = p.gene.x_orientation * (pow(p.gene.x_orientation*(ar.x - leftx), 2) +
                                                     pow(abs(p.gene.y_orientation * (ar.y - lefty)), 2))
                    r_attr = p.gene.x_orientation * (pow(p.gene.x_orientation*(rightx - ar.x), 2) +
                                                     pow(abs(p.gene.x_orientation*(righty - ar.y)), 2))
                    danger = r_attr - l_attr
                    if danger > 0 or p.x + p.xRange < 800:
                        p.speed = p.get_max_speed()
                    elif danger <= 0 or p.x - p.xRange > 0:
                        p.speed = -1 * p.get_max_speed()
                    else:
                        p.speed = 0
            else:
                if_moving = False
                if not guard:
                    busy.update({p: 0})
                if busy.get(p) == 0:
                    p.speed = 0


def get_closest(a, arrow):
    left = 0
    right = 800
    if len(arrow) > 2:
        for closest in arrow:
            if closest != a:
                if closest.x < a.x:
                    if closest.x > left:
                        left = closest.x
                else:
                    if closest.x < right:
                        right = closest.x
        return left, right


def if_match(x_o, x_k, r):
    sub = x_k - x_o
    if sub > r:
        return True
    return False


def show_player(p, x, y):  # fun showing element

    playerImg = pygame.image.load(p.image)
    p.update(x, y)
    # p.print_self()
    screen.blit(playerImg, (x, y))


def if_in_range(p, a):  # fun which checks if collision has happened

    for e in p:
        for i in range(int(e.x), int(e.x + e.xRange - 4)):
            if int(a.x) == i and (a.y == e.y - e.yRange or a.y > e.y - e.yRange):
                p.remove(e)


def load_player(x_pos):  # fun which loads arrows/players
    if gen_counter == 1:
        pl = Player.Player(x_pos, playerY, 84., 31., 'ludek.png', 0, 0)
        speed_gene = random.uniform(0.1, 0.2)
        x_mod_gene = random.uniform(0, 0.1)
        y_mod_gene = random.uniform(0, 0.1)
        pl.update_genes(speed_gene, x_mod_gene, y_mod_gene)
    else:
        pl = Player.Player(x_pos, playerY, 84., 31., 'ludek.png', 0, 0)
        pl.gene = cross(get_best_genes(generation_players))
    return pl


collapse = False


def load_arrow(time_gap):  # thread function which loads arrow into the screen
    checker = True

    while checker:
        lock.acquire()
        xPos = random.randrange(800)
        if len(arrows) < 13:
            ar = Arrow.Arrow(xPos, 0., 18., 28., 'arrow.png')
            arrows.append(ar)

        if time_gap >= .55:
            time_gap -= .25

        lock.release()
        time.sleep(0.30)

        if collapse:
            checker = False


def get_champion(champions):
    tmp = []

    for p in champions:
        tmp.append(p)
    max = tmp[0]
    for p1 in tmp:
        if p1.fitness > max.fitness:
            max = p1
    return max


# loading players in amount of declared population


thread = StopableThread.StopableThread(target=load_arrow, args=(4,), daemon=True)

player_threads = []
# program loop


def main(thr):  # main function
    lock.acquire()
    loc_arr = arrows
    lock.release()

    ifExit = False

    global collapse
    global busy
    global gen_counter
    global players
    global generation_players

    collapse = False

    busy.clear()
    if len(players) > 0:
        for p in players:
            players.remove(p)
    for x in range(population):
        players.append(load_player(random.uniform(0., 800.)))
        tmp = {x: 0}
        busy.update(tmp)
    for gp in generation_players:
        generation_players.remove(gp)
    xa = busy
    if len(loc_arr) > 0:
        for a in loc_arr:
            loc_arr.remove(a)
    for p in players:
        generation_players.append(p)
    print(xa)

    for p in players:
        t = threading.Thread(target=if_in_danger, args=(p,), daemon=True)
        player_threads.append(t)
        t.start()
    thr.start()

    while not ifExit:

        screen.blit(pygame.image.load('bg.png'), [0, 0])
        font = pygame.font.Font('freesansbold.ttf', 14)
        text = font.render('Players: ' + str(len(players)) + '     Arrows: ' + str(len(loc_arr)) + '     Generation: '
                           + str(gen_counter), True, (0, 0, 0), (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (138, 7)
        screen.blit(text, textRect)

        champion = get_champion(players)
        font = pygame.font.Font('freesansbold.ttf', 14)
        text = font.render('Best fitness: ' + str(champion.fitness) + '  Speed: ' + str(champion.gene.max_speed)[0:4] +
                           '  X_modifier: ' + str(champion.gene.x_orientation)[0:4] + '  Y_modifier: ' +
                           str(champion.gene.y_orientation)[0:4] , True, (0, 0, 0), (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (520, 7)
        screen.blit(text, textRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ifExit = True

        for xp in players:
            xp.x += xp.speed
            xp.fitness = xp.fitness + 1
            show_player(xp, xp.x, xp.y)
            if xp.x <= 0:
                xp.x = 0
            elif xp.x >= 716:
                xp.x = 715

        global generations
        for arr in loc_arr:
            arr.y += arrowYchange
            if arr.y < 600:
                show_player(arr, arr.x, arr.y)
            if_in_range(players, arr)
            if len(players) == 0 and arr.y <= 600:
                if generations > 0:

                    gen_counter = gen_counter + 1
                    collapse = True
                    thr.join()
                    for t in player_threads:
                        t.join()
                    for ar in loc_arr:
                        lock.acquire()
                        arrows.remove(ar)
                        lock.release()
                    for pl in players:
                        players.remove(pl)
                        busy.clear()
                    generations = generations - 1
                    time.sleep(1)
                    main(StopableThread.StopableThread(target=load_arrow, args=(4,), daemon=True))

                else:
                    collapse = True
                    thr.join()
                    pygame.quit()
                    sys.exit()
            elif arr.y > 550:
                lock.acquire()
                loc_arr.remove(arr)
                lock.release()

        pygame.display.update()


main(thread)
