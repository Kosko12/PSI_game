import pygame


class Player():



    def __init__(self, x, y, xRange, yRange, image, maxSpeed):
        self.image = image
        self.xRange = xRange
        self.yRange = yRange
        self.x = x
        self.y = y
        self.speed = 0
        self.maxSpeed = maxSpeed

    def update(self, *args):
        self.x = args[0]
        self.y = args[1]

    def print_self(self):
        print("X: " + str(self.x) + " Y: " + str(self.y))