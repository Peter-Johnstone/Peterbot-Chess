from Utilities import Utils
from Pin import Pin
from Check import Check
from MoveGeneration import MoveGeneration

class Position:
    directionPieceMapping = {
            'B': [[1,-1], [1, 1], [-1,-1], [-1,1]],
            'R': [[1, 0], [0, 1], [-1,0], [0,-1]],
            'Q': [[1,-1], [1, 1], [-1,-1], [-1,1],[1, 0], [0, 1], [-1,0], [0,-1]]
    }

    def __init__(self, FEN):
        self.readFen(FEN)
 

    def __str__(self):
        s = ''
        s +=  '\n+---+---+---+---+---+---+---+---+\n'
        for i, row in enumerate(self.board):
            for val in row:
                piece = ' ' if val == '.' else val
                s += '| ' + piece + ' '
            s += f'| {8-i}\n+---+---+---+---+---+---+---+---+\n'
        s += '  a   b   c   d   e   f   g   h \n'
        return s

    def readFen(self, FEN):
        fields = FEN.split()
        self.board = []      
        # Make the board
        fields[0] += '/'
        row, i = [], 0
        while i < len(fields[0]):
            val = fields[0][i]
            if val == '/':
                self.board.append(row)
                row = []
            elif val.isnumeric():
                row.extend(['.'] * int(val))
            else: # val is piece
                row.append(val)
            i+=1
        self.currentTurn = fields[1]
        self.canCastle = fields[2] if fields[2] != '-' else ''
        self.enPassantSquare = Utils.getCoordinateNotation(fields[3]) if fields[3] != '-' else []
        self.halfmoveClock = int(fields[4]) if len(fields) >= 5 else 0
        self.fullmoveClock = int(fields[5]) if len(fields) == 6 else 0
        self.getPieceLocations()
        self.getPinsAndChecks()
        self.gameOver = Position.checkGameOver(self)

    def getPieceLocations(self):
        self.pieceLocations = {'P':[], 'N':[], 'B':[], 'R':[], 'Q':[], 'K':[],
                               'p':[], 'n':[], 'b':[], 'r':[], 'q':[], 'k':[]}
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '.':
                    self.pieceLocations[piece].append([row, col])
        self.pieceLocations




    def getPinsAndChecks(self):

        self.pins, self.checks = [], []
        # Radially Outwards from king
        def getVectorAttacks(king):
            rKing, cKing = self.pieceLocations[king][0]
            diagonals =  [[-1,-1],
                          [-1, 1],
                          [1, -1],
                          [1,  1]]
            
            orthogonals = [[0, -1],
                           [0, +1],
                           [-1, 0],
                           [+1, 0]]
            
            for rMod, cMod in diagonals+orthogonals:
                isOrthogonal = rMod*cMod == 0
                rCur, cCur = rKing+rMod, cKing+cMod
                firstPieceCoords = None
                while Utils.inBounds(rCur, cCur):
                    piece = self.board[rCur][cCur]
                    if not firstPieceCoords and Utils.differentColors(piece, king):
                        # First piece is enemy piece
                        if (isOrthogonal and piece.lower() in ['r', 'q']) or (not isOrthogonal and piece.lower() in ['b', 'q']): 
                            self.checks.append(Check([rCur, cCur], [rKing, cKing], [-rMod, -cMod]))
                        break
                    elif firstPieceCoords and Utils.differentColors(piece, king):
                        # First piece ally and second piece is enemy piece
                        if (isOrthogonal and piece.lower() in ['r', 'q']) or (not isOrthogonal and piece.lower() in ['b', 'q']):
                            self.pins.append(Pin([rCur, cCur], firstPieceCoords, [-rMod, -cMod]))
                        break
                    elif firstPieceCoords and Utils.sameColors(piece, king): 
                        # First piece ally and second piece also ally --> no pin
                        break
                    elif not firstPieceCoords and Utils.sameColors(piece, king):
                        # First piece is ally piece
                        firstPieceCoords = [rCur, cCur]
                    rCur += rMod
                    cCur += cMod
                    

        def getKnightChecks(king):
            rKing, cKing = self.pieceLocations[king][0]
            relevantFields = [[rKing-2, cKing-1],
                              [rKing-2, cKing+1],
                              [rKing-1, cKing-2],
                              [rKing-1, cKing+2],
                              [rKing+1, cKing-2],
                              [rKing+1, cKing+2],
                              [rKing+2, cKing-1],
                              [rKing+2, cKing+1]]
            
            for r, c in relevantFields:
                if [r, c] in self.pieceLocations[Utils.opposeFirstPieceColor(king, 'n')]:
                    self.checks.append(Check([r,c],[rKing, cKing]))

        def getPawnChecks(king):
            rKing, cKing = self.pieceLocations[king][0]
            relevantFields = {'k': [[rKing+1,cKing-1],[rKing+1,cKing+1]],
                              'K': [[rKing-1,cKing-1],[rKing-1,cKing+1]]}

            for r, c in relevantFields[king]:
                if [r, c] in self.pieceLocations[Utils.opposeFirstPieceColor(king, 'p')]:
                    self.checks.append(Check([r, c],[rKing, cKing]))
        
        for king in ['k', 'K']:
            getVectorAttacks(king)
            getKnightChecks(king)
            getPawnChecks(king)



  


    def checkGameOver(position):
        whitePieces = []
        blackPieces = []
        for key, value in position.pieceLocations.items():
            if key.isupper(): whitePieces += value
            else: blackPieces += value
    
        if len(whitePieces) == len(blackPieces) == 1:
            return 0

        if len(MoveGeneration.getLegalMoves(position)) == 0:
            # Either stalemate or loss
            # checkmated
            if MoveGeneration.detectCheck(position):
                return -1000000
            # stalemate
            else:
                return 0
        return -1






'''
    def updatePinsAndChecks(self, move):
  
        if move.piece.lower() == 'k':
            return self.getPinsAndChecks() # If king move we need to reset entirely
        self.correctOldPinsChecks(move) # Fixes any checks pins or checks that targeted the king of the player who made the move
        self.addNewPinsChecks(move) # Only deals with potential new pins and checks directed at opponent king
        
        print("PINS AND CHECKS")

        for pin in self.pins:
            print(pin)

        for check in self.checks:
            print(check)

    def correctOldPinsChecks(self, move):


    def addNewPinsChecks(self, move):
        '''
        #  Possible New Pins/Checks:
        # 1) Piece that moved gives pin/check
        # 2) Piece behind the piece that moves gives pin/check
'''
        # Coords of enemy king
        rKing, cKing = self.pieceLocations[Utils.opposeFirstPieceColor(move.piece, 'k')][0]

        def checkMovedPiece():       
        '''
        #    If applicable, appends new check or pin that's caused by the moved piece
'''
            if move.piece.upper() not in Position.directionPieceMapping: return  # Moved piece was a not relevant piece, we can ignore
            print("Getting here 1")
            direction = Utils.calculateDirection([rKing, cKing], move.end)       # We get the direction from opposing king to that moved piece
            print(direction)
            if direction in Position.directionPieceMapping[move.piece.upper()]:  # We check if the direction matches the direction that would threaten opposing king
                print("Getting here 2")
                self.checkInBetweenCoords(rKing, cKing, *move.end, *direction)   # Now we must check the fields in the middle
                return

        def checkDiscoveredPiece():
        '''
            # Finds any relevant potentially checking/pinned pieces that were 'discovered' by the last move
'''
            direction = Utils.calculateDirection([rKing, cKing], move.start)     # Gets the direction away from the king
            if not direction: return                                             # King was not in line with where the piece started
            rMod, cMod = direction                                               # Gets the modifiers, used for iterating past move.start
            rCur, cCur = move.start[0]+rMod, move.start[1]+cMod                  # Sets the r and c pointers, we iterate on these
            king = self.board[rKing][cKing]
            firstPieceCoords = None
            while Utils.inBounds(rCur, cCur):
                piece = self.board[rCur][cCur]
                if Utils.sameColors(king, piece):
                    if firstPieceCoords: return
                    firstPieceCoords = [rCur, cCur]
                if Utils.differentColors(king, piece):
                    if piece.upper() not in Position.directionPieceMapping: return
                    if [rMod, cMod] not in Position.directionPieceMapping[piece.upper()]: return
                    return self.checkInBetweenCoords(rKing, cKing, rCur, cCur, rMod, cMod)
                rCur += rMod
                cCur += cMod
        checkMovedPiece()
        checkDiscoveredPiece()
        


    def checkInBetweenCoords(self, rKing,cKing, rAttacker,cAttacker, rMod,cMod): 
    '''
        # Find potential pin/check between an attacking piece and an opposing king
'''
        rCur, cCur = rKing, cKing
        king = self.board[rKing][cKing]
        firstPieceCoords = None
        iterationDistance = max(abs(rKing-rAttacker), abs(cKing-cAttacker))-1
        for _ in range(iterationDistance):
            rCur += rMod
            cCur += cMod
            piece = self.board[rCur][cCur]
            if Utils.sameColors(king, piece):
                if firstPieceCoords: return
                firstPieceCoords = [rCur, cCur]
            elif Utils.differentColors(king, piece):
                return
        if firstPieceCoords:
            self.pins.append(Pin([rAttacker, cAttacker], firstPieceCoords, [rMod, cMod]))
        else:
            self.checks.append(Check([rAttacker, cAttacker], [rKing, cKing], [rMod, cMod]))
        '''