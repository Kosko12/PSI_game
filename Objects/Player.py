import pygame


class Player:

    class Gene:
        def __init__(self, max_speed, x_orientation, y_orientation):
            self.max_speed = max_speed
            self.x_orientation = x_orientation
            self.y_orientation = y_orientation

    class Fear:
        def __init__(self, curr_dng, prev_dng):
            self.curr_dng = curr_dng
            self.prev_dng = prev_dng

    def __init__(self, x, y, xRange, yRange, image, dng, prev_dng):
        self.image = image
        self.xRange = xRange
        self.yRange = yRange
        self.x = x
        self.y = y
        self.fitness = 0
        self.speed = 0
        self.gene = Player.Gene(0, 0, 0)
        self.fear = Player.Fear(dng, prev_dng)

    def update_genes(self, *args):
        self.gene.max_speed = args[0]
        self.gene.x_orientation = args[1]
        self.gene.y_orientation = args[2]

    def get_max_speed(self):
        return self.gene.max_speed

    def update(self, *args):
        self.x = args[0]
        self.y = args[1]

    def print_self(self):
        print("X: " + str(self.x) + " Y: " + str(self.y))