from random import choice

COLOURS = [
    (254, 67, 101),
    (252, 157, 154),
    (249, 205, 173),
    (200, 200, 169),
    (131, 175, 155),
]


class Colour:

    def __init__(self, r: int=0, g: int=0, b: int=0) -> None:
        self.r = r
        self.g = g
        self.b = b

    @property
    def colour(self):
        return (self.r, self.g, self.b)

    @classmethod
    def randomise(cls) -> 'Colour':
        instance = Colour()
        colour = choice(COLOURS)
        instance.r = colour[0]
        instance.g = colour[1]
        instance.b = colour[2]
        return instance