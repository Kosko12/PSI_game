

class Arrow:

    def __init__(self, x, y, xRange, yRange, image):
        # pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.xRange = xRange
        self.yRange = yRange
        self.x = x
        self.y = y

    def update(self, *args):
        self.x = args[0]
        self.y = args[1]