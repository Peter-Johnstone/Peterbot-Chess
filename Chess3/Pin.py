class Pin:

    def __init__(self, pinningPieceCoords, pinnedPieceCoords, direction):
        self.pinningPieceCoords = pinningPieceCoords
        self.pinnedPieceCoords = pinnedPieceCoords
        self.direction = direction
    
    def __str__(self):
        s = ''
        s += f'PIECE PINNED AT: {self.pinnedPieceCoords} \n'
        s += f'PINNED TO: {self.direction}'
        return s