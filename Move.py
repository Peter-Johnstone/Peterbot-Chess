from Utilities import Utils

class Move:

    def __init__(self, piece, start, end, board, promotionPiece = None, isEnPassant = False, castleSide = None):
        self.piece = piece
        self.start = start
        self.end = end
    
        self.promotionPiece = promotionPiece

        # Booleans
        self.isEnPassant = isEnPassant
        self.castleSide = castleSide

        self.changesCastleAvailability = False

        self.checkCapture(board)
    
    def checkCapture(self, board):
        piece = board[self.end[0]][self.end[1]]
        if piece != '.':
            self.capturedPiece = piece
        else:
            self.capturedPiece = None


    
    def __str__(self):
        if self.castleSide:
            return f'CASTLE {self.castleSide.upper()} FROM {Utils.getChessNotation(self.start)} TO {Utils.getChessNotation(self.end)}'
        if self.isEnPassant:
            return f'EN PASSANT FROM {Utils.getChessNotation(self.start)} TO {Utils.getChessNotation(self.end)}'
        if self.promotionPiece:
            return f'PROMOTING INTO {self.promotionPiece}. {Utils.getChessNotation(self.start)} TO {Utils.getChessNotation(self.end)}'
        return f'{Utils.getChessNotation(self.start)} TO {Utils.getChessNotation(self.end)}'
        