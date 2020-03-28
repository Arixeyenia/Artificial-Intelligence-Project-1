import enum

class Piece:
    def __init__(self, coordinates, colour):
        self.coordinates = coordinates
        self.colour = colour

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates
    
    def __str__(self):
        return self.colour

class Stack:
    def __init__(self, pieces, colour):
        self.pieces = pieces
        self.colour = colour
        self.number = len(pieces)
        self.coordinates = pieces[0].coordinates

    def __str__(self):
        return self.colour + str(self.number)

    def remove_piece(self, piece):
        self.pieces.remove(piece)
        self.number -= 1

class Directions(enum.Enum):
    left = 1
    right = 2
    up = 3
    down = 4