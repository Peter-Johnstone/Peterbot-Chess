from Move import Move
from Utilities import Utils

class MoveGeneration:

    castleInfo = {
            'w': {'kingside': {'rookPosition':[7,7], 'castleCrosses': [[7,5], [7,6]], 'crossingCheck': [7,5]},
                  'queenside': {'rookPosition': [7,0], 'castleCrosses': [[7,3], [7,2], [7,1]], 'crossingCheck': [7,3]}},
            'b': {'kingside': {'rookPosition': [0,7], 'castleCrosses': [[0,5], [0,6]], 'crossingCheck': [0,5]},
                  'queenside': {'rookPosition': [0,0], 'castleCrosses': [[0,3], [0,2], [0,1]], 'crossingCheck': [0,3]}}
        }


    def getLegalMoves(position):
        possibleMoves = []
        pieceCoords = []
        for piece, coords in position.pieceLocations.items():
            if Utils.turnMatchesPiece(position.currentTurn, piece):
                pieceCoords += coords
        for r, c in pieceCoords:
            possibleMoves += MoveGeneration.getPieceMoves(r, c, position)
        return possibleMoves

    
    def getPieceMoves(r, c, position):
        piece = position.board[r][c]

        if piece not in ['k','K'] and len(position.checks) == 2:
            return []
        
        moves = []
        pin = next((pinInstance for pinInstance in position.pins if pinInstance.pinnedPieceCoords == [r, c]), None)
        check = position.checks[0] if len(position.checks) == 1 else None
        # Not your turn
        if not Utils.turnMatchesPiece(position.currentTurn, piece) or piece == '.':
            return []
        
        # Identify the Piece and then call appropriate function
        if piece.upper() == 'P':
            moves = MoveGeneration.getPawnMoves(r, c, position, pin, check)
        elif piece.upper() == 'N':
            moves = MoveGeneration.getKnightMoves(r, c, position, pin, check)
        elif piece.upper() == 'B':
            moves = MoveGeneration.getBishopMoves(r, c, position, pin, check)
        elif piece.upper() == 'R':
            moves = MoveGeneration.getRookMoves(r, c, position, pin, check)
        elif piece.upper() == 'Q':
            moves = MoveGeneration.getQueenMoves(r, c, position, pin, check)
        elif piece.upper() == 'K':
            moves = MoveGeneration.getKingMoves(r, c, position, position.checks)
        return moves
    

    def isLegal(move, pin, check): # Assumes one check at most

        if pin and check:
            return False
        
        if check and not check.direction:  # Either Knight or Pawn Check
            return move.end == check.checkingPieceCoords 
        
        if check: # Bishop, rook, or queen check (accounts for blocking)
            collinear = Utils.collinearVectors([move.end[0]-check.checkingPieceCoords[0], move.end[1]-check.checkingPieceCoords[1]], check.direction)
            inRowSpan =  min(check.kingPosition[0], check.checkingPieceCoords[0]) <= move.end[0] <= max(check.kingPosition[0], check.checkingPieceCoords[0])
            inColSpan =  min(check.kingPosition[1], check.checkingPieceCoords[1]) <= move.end[1] <= max(check.kingPosition[1], check.checkingPieceCoords[1])
            return collinear and inRowSpan and inColSpan
        
        if pin:           
            return Utils.collinearVectors([move.end[0]-move.start[0], move.end[1]-move.start[1]], pin.direction)
        return True # No pin or check
            

    def addLegalMove(move, moves, pin, check):
        if MoveGeneration.isLegal(move, pin, check):
            moves.append(move)
        return moves

    def getPawnMoves(r, c, position, pin, check):
        pawnMoves = []
        piece = position.board[r][c]
        whiteToMove = Utils.isWhite(piece)
        a = -1 if whiteToMove else 1

        def checkPromotion(move):
            if not MoveGeneration.isLegal(move, pin, check):
                return
            if move.end[0] in [0, 7]:
                promotions = ['N', 'B', 'R', 'Q'] if whiteToMove else ['n', 'b', 'r', 'q']
                pawnMoves.extend(Move(move.piece, move.start, move.end, position.board, piece) for piece in promotions)
            else:
                pawnMoves.append(move)
        
        # Check capture left
        if Utils.inBounds(r + a, c-1) and Utils.differentColors(piece, position.board[r + a][c-1]):
            checkPromotion(Move(piece, [r, c], [r + a, c-1], position.board))

        # Check capture right
        if Utils.inBounds(r + a, c+1) and Utils.differentColors(piece, position.board[r + a][c+1]):
            checkPromotion(Move(piece, [r, c], [r + a, c+1], position.board))

        # Check push pawn
        if Utils.inBounds(r + a, c) and position.board[r + a][c] == '.':
            checkPromotion(Move(piece, [r, c], [r + a, c], position.board))

        # Check double move
        if r == int(3.5 - 2.5*a):
            if position.board[r + a][c] == position.board[r + 2*a][c] == '.':
                pawnMoves = MoveGeneration.addLegalMove(Move(piece, [r, c], [r + 2*a, c], position.board), pawnMoves, pin, check)

        # Check en passant
        if position.enPassantSquare:
            if abs(position.enPassantSquare[1]-c) == 1 and r == int(3.5 + .5*a):
                move = Move(piece, [r, c], [r + a, position.enPassantSquare[1]], position.board, promotionPiece = None, isEnPassant = True)
                if MoveGeneration.checkEnPassantLegal(move, position):
                    pawnMoves = MoveGeneration.addLegalMove(move, pawnMoves, pin, check)
        return pawnMoves
 


    def checkEnPassantLegal(move, position): ## Addresses the bug where the pawn can en passant exposing a rook or queen check to king
        rKing, cKing = position.pieceLocations[Utils.matchFirstPieceColor(move.piece, 'k')][0]
    
        if rKing != move.start[0]:
            return True

        enemyPieceDistance = 9
        enemyPieceCol = -1

        for rEnemy, cEnemy in position.pieceLocations[Utils.opposeFirstPieceColor(move.piece, 'r')] + \
                                position.pieceLocations[Utils.opposeFirstPieceColor(move.piece, 'q')]:
            if rEnemy != rKing:
                continue

            if Utils.inBetween(cKing, move.start[1], cEnemy) and abs(cKing - cEnemy) < enemyPieceDistance:
                enemyPieceDistance = abs(cKing - cEnemy)
                enemyPieceCol = cEnemy

        if enemyPieceCol == -1:
            return True

        minCol, maxCol = min(cKing, enemyPieceCol), max(cKing, enemyPieceCol)
        pieceCount = sum(1 for c in range(minCol + 1, maxCol) if position.board[rKing][c] != '.')
        return pieceCount != 2
        






    def getKnightMoves(row, col, position, pin, check):
        knightMoves = []

        piece = position.board[row][col]

        relevantFields = [[row-2, col-1],
                          [row-2, col+1],
                          [row-1, col-2],
                          [row-1, col+2],
                          [row+1, col-2],
                          [row+1, col+2],
                          [row+2, col-1],
                          [row+2, col+1]]
        
        for r, c in relevantFields:
            if Utils.inBounds(r, c) and not Utils.sameColors(piece, position.board[r][c]):
                knightMoves = MoveGeneration.addLegalMove(Move(piece, [row, col], [r,c], position.board), knightMoves, pin, check)

        return knightMoves



    def getBishopMoves(r, c, position, pin, check):
        piece = position.board[r][c]
        bishopMoves = []
    
        relevantDiagonals = [[-1,-1],
                             [-1, 1],
                             [1, -1],
                             [1,  1]]
        
        for rMod, cMod in relevantDiagonals:
            bishopMoves += MoveGeneration.getSlidingMove(piece, r, c, rMod, cMod, position.board, pin, check)

        return bishopMoves
    

    def getRookMoves(r, c, position, pin, check):
        piece = position.board[r][c]
        rookMoves = []

        relevantOrthogonals = [[0, -1],
                               [0, +1],
                               [-1, 0],
                               [+1, 0]]
        
        for rMod, cMod in relevantOrthogonals:
            rookMoves += MoveGeneration.getSlidingMove(piece, r, c, rMod, cMod, position.board, pin, check)

        return rookMoves
    
    def getQueenMoves(r, c, position, pin, check):
        piece = position.board[r][c]
        queenMoves = []

        relevantDirections = [[-1,-1],
                              [-1, 1],
                              [1, -1],
                              [1,  1],
                              [0, -1],
                              [0, +1],
                              [-1, 0],
                              [+1, 0]]

        for rMod, cMod in relevantDirections:
            queenMoves += MoveGeneration.getSlidingMove(piece, r, c, rMod, cMod, position.board, pin, check)

        return queenMoves
    



    def getSlidingMove(piece, row, col, rMod, cMod, board, pin, check):
        # Finds all the moves in the specified direction on the game board.
        moves = []

        r, c = row+rMod, col+cMod

        while Utils.inBounds(r, c) and not Utils.sameColors(piece, board[r][c]):
            moves = MoveGeneration.addLegalMove(Move(piece, [row, col], [r,c], board), moves, pin, check)
            if Utils.differentColors(piece, board[r][c]): 
                break
            r += rMod
            c += cMod
        return moves
    

    def detectCheck(position):
        return MoveGeneration.attackedSquare(position.pieceLocations[Utils.getPieceMatchTurn(position.currentTurn, 'k')][0], position)

    def attackedSquare(coords, position):
        rKing, cKing = coords

        def isVectorCheck():
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

                while Utils.inBounds(rCur, cCur):
                    piece = position.board[rCur][cCur]
                    rCur += rMod
                    cCur += cMod
                    if piece == '.': continue
                    if Utils.turnMatchesPiece(position.currentTurn, piece): # your piece
                        break
                    if not Utils.turnMatchesPiece(position.currentTurn, piece): # enemy piece
                        if (isOrthogonal and piece.lower() in ['r', 'q']) or (not isOrthogonal and piece.lower() in ['b', 'q']):
                            return True
                        break
            return False
                    
    

        def isKnightCheck():
            relevantFields = [[rKing-2, cKing-1],
                              [rKing-2, cKing+1],
                              [rKing-1, cKing-2],
                              [rKing-1, cKing+2],
                              [rKing+1, cKing-2],
                              [rKing+1, cKing+2],
                              [rKing+2, cKing-1],
                              [rKing+2, cKing+1]]
            
            for r, c in relevantFields:
                if [r, c] in position.pieceLocations[Utils.getPieceOpposeTurn(position.currentTurn, 'n')]:
                    return True
            return False

        def isPawnCheck():
            relevantFields = {'b': [[rKing+1,cKing-1],[rKing+1,cKing+1]],
                              'w': [[rKing-1,cKing-1],[rKing-1,cKing+1]]}

            for r, c in relevantFields[position.currentTurn]:
                if [r, c] in position.pieceLocations[Utils.getPieceOpposeTurn(position.currentTurn, 'p')]:
                    return True
            return False
        def isKingCheck():
            relevantFields = [[rKing-1, cKing-1],
                              [rKing-1,   cKing],
                              [rKing-1, cKing+1],
                              [rKing  , cKing-1],
                              [rKing  ,   cKing],
                              [rKing  , cKing+1],
                              [rKing+1, cKing-1],
                              [rKing+1,   cKing],
                              [rKing+1, cKing+1]]
            for r, c in relevantFields:
                if [r, c] == position.pieceLocations[Utils.getPieceOpposeTurn(position.currentTurn, 'k')][0]:
                    return True
            return False
        return isPawnCheck() or isKnightCheck() or isVectorCheck() or isKingCheck()

    def isLegalKingMove(move, position, checks):
        for check in checks:
            if check.direction and Utils.collinearVectors([move.end[0]-move.start[0], move.end[1]-move.start[1]], check.direction) and (move.end != check.checkingPieceCoords): # Moving along check diagonal and not capturing checking piece
                return False
        return not MoveGeneration.attackedSquare(move.end, position)

    def addLegalKingMove(move, moves, position, checks):
        if MoveGeneration.isLegalKingMove(move, position, checks):
            moves.append(move)
        return moves

    def getKingMoves(row, col, position, checks):
        piece = position.board[row][col]
        kingMoves = []

        relevantFields = [[row-1, col-1],
                          [row-1,   col],
                          [row-1, col+1],
                          [row  , col-1],
                          [row  ,   col],
                          [row  , col+1],
                          [row+1, col-1],
                          [row+1,   col],
                          [row+1, col+1]]

        for r, c in relevantFields:
            if Utils.inBounds(r, c) and not Utils.sameColors(piece, position.board[r][c]):
                kingMoves = MoveGeneration.addLegalKingMove(Move(piece, [row, col], [r,c], position.board), kingMoves, position, checks)

        def canCastle(side):
            if checks: # currently active check instance
                return False
            castlePiece = 'k' if side == 'kingside' else 'q'
            if Utils.getPieceMatchTurn(position.currentTurn, castlePiece) not in position.canCastle:
                return False
            # Checks to make sure the fields between rook and king are empty
            for r, c in MoveGeneration.castleInfo[position.currentTurn][side]['castleCrosses']:
                if position.board[r][c] != '.':
                    return False
            # Checks to make sure the rook still exists
            rookR, rookC = MoveGeneration.castleInfo[position.currentTurn][side]['rookPosition']
            if position.board[rookR][rookC] != Utils.getPieceMatchTurn(position.currentTurn, 'r'):
                return False
            if MoveGeneration.attackedSquare(MoveGeneration.castleInfo[position.currentTurn][side]['crossingCheck'], position): # Crosses check
                return False
            return True
        
        if canCastle('kingside'):
            kingMoves = MoveGeneration.addLegalKingMove(Move(piece, [row, col], [row, col+2], position.board, promotionPiece = None, isEnPassant = False, castleSide = 'kingside'), kingMoves, position, checks)
        if canCastle('queenside'):
            kingMoves = MoveGeneration.addLegalKingMove(Move(piece, [row, col], [row, col-2], position.board, promotionPiece = None, isEnPassant = False, castleSide = 'queenside'), kingMoves, position, checks)
        return kingMoves
    

   




