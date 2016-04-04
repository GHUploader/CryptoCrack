

class Point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def toString(self):
        return str(self.getX()) + str(self.getY())



