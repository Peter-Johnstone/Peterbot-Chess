from random import randint

class Utils:
    piecePositionTable = [[0 for _ in range(12)] for _ in range(64)]
    piecesHashmap = {
        'p': 0,
        'b': 1, 
        'n': 2,
        'r': 3,
        'q': 4,
        'k': 5,

        'P': 6,
        'B': 7, 
        'N': 8,
        'R': 9,
        'Q': 10,
        'K': 11
    }

    def getChessNotation(coords):
        y, x = coords
        letters = 'abcdefgh'
        return letters[x]+str(8-y)
    
    def getCoordinateNotation(chessNotation):
        letters = 'abcdefgh'
        return [8-int(chessNotation[1]), letters.index(chessNotation[0])]

    def isWhite(piece):
        if piece == '.':
            return False
        return piece.isupper()
    
    def isBlack(piece):
        if piece == '.':
            return False
        return piece.islower()
    
    def differentColors(piece1, piece2):
        if piece1 == '.' or piece2 == '.':
            return False
        return (Utils.isWhite(piece1) and Utils.isBlack(piece2)) or (Utils.isBlack(piece1) and Utils.isWhite(piece2))
    
    def sameColors(piece1, piece2):
        if piece1 == '.' or piece2 == '.':
            return False
        return not((Utils.isWhite(piece1) and Utils.isBlack(piece2)) or (Utils.isBlack(piece1) and Utils.isWhite(piece2)))
    
    def turnMatchesPiece(turn, piece):
        if piece == '.': return False
        return (turn == 'w') == Utils.isWhite(piece)

    def turnOpposesPiece(turn, piece):
        if piece == '.': return False
        return not (turn == 'w') == Utils.isWhite(piece)
    
    def inBounds(row, col):
        return 0<=row<=7 and 0<=col<=7

    def matchFirstPieceColor(templatePiece, changingPiece):
        if templatePiece.isupper():
            return changingPiece.upper()
        else:
            return changingPiece.lower()
        
    def opposeFirstPieceColor(templatePiece, changingPiece):
        if templatePiece.isupper():
            return changingPiece.lower()
        else:
            return changingPiece.upper()


    def getPieceMatchTurn(turn, piece):
        if Utils.turnMatchesPiece(turn, piece):
            return piece
        elif piece.islower():
            return piece.upper()
        else:
            return piece.lower()
        
    def getPieceOpposeTurn(turn, piece):
        if not Utils.turnMatchesPiece(turn, piece):
            return piece
        elif piece.islower():
            return piece.upper()
        else:
            return piece.lower()
    

    def collinearVectors(vector1, vector2):
        # Same or opposite direction vectors
        return (vector1[1]*vector2[0] - vector1[0]*vector2[1]) == 0
    
    def switchTurns(currentTurn):
        if currentTurn == 'b':
            return 'w'
        else:
            return 'b'

    def inBetween(a, b, c): # b in between a and c?
        if a<b<c:
            return True
        if c<b<a:
            return True
        return False
    
    def calculateDirection(pointA, pointB): 
        '''
        Makes sure two pieces are on the same isle (diagonal or orthogonal)
        if so, it returns the direction we take from pointA to pointB
        '''
        rMod = 1 if pointA[0] < pointB[0] else -1 if pointA[0] > pointB[0] else 0
        cMod = 1 if pointA[1] < pointB[1] else -1 if pointA[1] > pointB[1] else 0
        if not Utils.collinearVectors([pointA[0]-pointB[0], pointA[1]-pointB[1]], [rMod, cMod]): return False
        return [rMod, cMod]

    def flipBoard(board):
        flippedRows = board[::-1]
        board = [row[::-1] for row in flippedRows]
        return board

    def flipCoords(row, col):
        return 7-row, 7-col
    

    def initializeZobristKeys():
        for i in range(64):
            for j in range(12):
                Utils.piecePositionTable[i][j] = randint(0, pow(2, 30))

    def hashKey(position):
        hashValue = 0
        for r, row in enumerate(position.board):
            for c, piece in enumerate(row):
                if piece in Utils.piecesHashmap:
                    pos = r * 8 + c
                    idx = Utils.piecesHashmap[piece]
                    hashValue ^= Utils.piecePositionTable[pos][idx]
        # castling right, en passant, and is black's turn
        
        return hashValue



        



        

