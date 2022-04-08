class userBall():
    def __init__(self, color: str, position: (int, int)):
        self.color = color
        self.position = position
        self.radius = 25
        self.moveSpeed = (0, 0)
    
    def __eq__(self, other):
        return True

class userBalls():
    def __init__(self):
        self.moving = list()
        self.static = userBall("", (200, 200))
    