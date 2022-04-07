class Ball():
    def __init__(self, color: str, position: (int, int), segment_number=0):
        self.color = color
        self.position = position
        self.segment_number = segment_number
        self.radius = 25
