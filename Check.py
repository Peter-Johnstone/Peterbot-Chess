class Check:

    def __init__(self, checkingPieceCoords, kingPosition, direction = None):

        self.checkingPieceCoords = checkingPieceCoords
        self.kingPosition = kingPosition
        self.direction = direction


    def __str__(self):
        s = ''
        s += f'CHECKING PIECE AT {self.checkingPieceCoords} \n'
        s += f'CHECKING ACROSS {self.direction}'
        return s