from MoveGeneration import MoveGeneration
from MoveHandling import MoveHandling
from Utilities import Utils
from Position import Position
from copy import deepcopy
import random

class Engine:

    positionHashes = {}

    pieceValues = {'P': 100, 
                   'N': 320, 
                   'B': 330, 
                   'R': 500, 
                   'Q': 900,
                   'K': 0}
    pawnTableWhite = (0,  0,  0,  0,  0,  0,  0,  0,
                      50, 50, 50, 50, 50, 50, 50, 50,
                      10, 10, 20, 30, 30, 20, 10, 10,
                      5,  5, 10, 25, 25, 10,  5,  5,
                      0,  0,  0, 20, 20,  0,  0,  0,
                      5, -5,-10,  0,  0,-10, -5,  5,
                      5, 10, 10,-20,-20, 10, 10,  5,
                      0,  0,  0,  0,  0,  0,  0,  0)
    pawnTableBlack = pawnTableWhite[::-1]
    
    knightTableWhite = (-50,-40,-30,-30,-30,-30,-40,-50,
                        -40,-20,  0,  0,  0,  0,-20,-40,
                        -30,  0, 10, 15, 15, 10,  0,-30,
                        -30,  5, 15, 20, 20, 15,  5,-30,
                        -30,  0, 15, 20, 20, 15,  0,-30,
                        -30,  5, 10, 15, 15, 10,  5,-30,
                        -40,-20,  0,  5,  5,  0,-20,-40,
                        -50,-40,-30,-30,-30,-30,-40,-50)
    knightTableBlack = knightTableWhite[::-1]

    bishopTableWhite = (-20,-10,-10,-10,-10,-10,-10,-20,
                        -10,  0,  0,  0,  0,  0,  0,-10,
                        -10,  0,  5, 10, 10,  5,  0,-10,
                        -10,  5,  5, 10, 10,  5,  5,-10,
                        -10,  0, 10, 10, 10, 10,  0,-10,
                        -10, 10, 10, 10, 10, 10, 10,-10,
                        -10,  5,  0,  0,  0,  0,  5,-10,
                        -20,-10,-10,-10,-10,-10,-10,-20)
    bishopTableBlack = bishopTableWhite[::-1]

    rookTableWhite = (0,  0,  0,  0,  0,  0,  0,  0,
                      5, 10, 10, 10, 10, 10, 10,  5,
                     -5,  0,  0,  0,  0,  0,  0, -5,
                     -5,  0,  0,  0,  0,  0,  0, -5,
                     -5,  0,  0,  0,  0,  0,  0, -5,
                     -5,  0,  0,  0,  0,  0,  0, -5,
                     -5,  0,  0,  0,  0,  0,  0, -5,
                      0,  0,  0,  5,  5,  0,  0,  0)
    rookTableBlack = rookTableWhite[::-1]

    queenTableWhite = (-20,-10,-10, -5, -5,-10,-10,-20,
                       -10,  0,  0,  0,  0,  0,  0,-10,
                       -10,  0,  5,  5,  5,  5,  0,-10,
                       -5,  0,  5,  5,  5,  5,  0, -5,
                        0,  0,  5,  5,  5,  5,  0, -5,
                       -10,  5,  5,  5,  5,  5,  0,-10,
                       -10,  0,  5,  0,  0,  0,  0,-10,
                       -20,-10,-10, -5, -5,-10,-10,-20)
    queenTableBlack = queenTableWhite[::-1]

    whiteKingMiddleGameTable = (-30,-40,-40,-50,-50,-40,-40,-30,
                                -30,-40,-40,-50,-50,-40,-40,-30,
                                -30,-40,-40,-50,-50,-40,-40,-30,
                                -30,-40,-40,-50,-50,-40,-40,-30,
                                -20,-30,-30,-40,-40,-30,-30,-20,
                                -10,-20,-20,-20,-20,-20,-20,-10,
                                 20, 20,  0,  0,  0,  0, 20, 20,
                                 20, 30, 10,  0,  0, 10, 30, 20)
    blackKingMiddleGameTable = whiteKingMiddleGameTable[::-1]

    whiteKingEndGameTable = (-50,-40,-30,-20,-20,-30,-40,-50,
                            -30,-20,-10,  0,  0,-10,-20,-30,
                            -30,-10, 20, 30, 30, 20,-10,-30,
                            -30,-10, 30, 40, 40, 30,-10,-30,
                            -30,-10, 30, 40, 40, 30,-10,-30,
                            -30,-10, 20, 30, 30, 20,-10,-30,
                            -30,-30,  0,  0,  0,  0,-30,-30,
                            -50,-30,-30,-30,-30,-30,-30,-50)
    blackKingEndGameTable = whiteKingEndGameTable[::-1]

    dummyKingTable = (0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0)

    pieceSquareTableMapping = {
        'P': pawnTableWhite,
        'N': knightTableWhite,
        'B': bishopTableWhite,
        'R': rookTableWhite,
        'Q': queenTableWhite,

        'p': pawnTableBlack,
        'n': knightTableBlack,
        'b': bishopTableBlack,
        'r': rookTableBlack,
        'q': queenTableBlack,

        'K': dummyKingTable,
        'k': dummyKingTable
    }
    kingSquareTableMapping = {
        False: {'K': whiteKingMiddleGameTable,
                'k': blackKingMiddleGameTable},
        True: {'K': whiteKingEndGameTable,
               'k': blackKingEndGameTable}
    }

    def __init__(self, strength):   
        self.strength = strength

    
    def getMove(self, position):
        if self.strength == 0:
            return Engine.playRandom(position)

        if self.strength == 1:
            return self.playStrength1(position)
        
        if self.strength == 2:
            return self.playStrength2(position)
        
    
    def playRandom(position):
        moves = MoveGeneration.getLegalMoves(position)
        return random.choice(moves)

    def playStrength1(self, position):
        numMoves = len(MoveGeneration.getLegalMoves(position))
        numOppMoves = len(MoveGeneration.getLegalMoves(MoveHandling.nullMove(deepcopy(position))))
        if numMoves+numOppMoves >= 40 or position.checks: depth = 4
        elif numMoves+numOppMoves >= 30: depth = 5
        elif numMoves+numOppMoves >= 14: depth = 6 
        elif numMoves+numOppMoves >= 8: depth = 7
        else: depth = 8
        def negamaxBad(position, moveLog, alpha, beta, depth):
            if depth == 0 or Position.checkGameOver(position) != -1: 
                return Engine.staticEvaluation(position)*(depth+1), None # From current player's perspective:
            maxEval, bestMove = float('-inf'), None
            moves = Engine.orderMoves(MoveGeneration.getLegalMoves(position))
            for move in moves:
                position, moveLog = MoveHandling.performMove(move, position, moveLog, False)
                eval, _ = negamaxBad(position, moveLog, -beta, -alpha, depth-1)
                eval = - eval
                if eval > maxEval: maxEval, bestMove = eval, move
                alpha = max(alpha, maxEval)
                position, moveLog = MoveHandling.undoMove(position, moveLog)
                if alpha >= beta:
                    break
            return maxEval, bestMove
        _, bestMove = negamaxBad(position, [], float('-inf'), float('inf'), depth)
        return bestMove



    def playStrength2(self, position):
        
        # Tampering depth to minimize search time
        numMoves = len(MoveGeneration.getLegalMoves(position))
        numOppMoves = len(MoveGeneration.getLegalMoves(MoveHandling.nullMove(deepcopy(position))))
        if numMoves+numOppMoves >= 40 or position.checks: depth = 4
        elif numMoves+numOppMoves >= 30: depth = 5
        elif numMoves+numOppMoves >= 11: depth = 6 
        else: depth = 7
        _, bestMove = Engine.negamax(position, [], float('-inf'), float('inf'), depth)
        return bestMove
    
    def negamax(position, moveLog, alpha, beta, depth):
        if depth == 0:
            return Engine.quiescence(position, moveLog, alpha, beta), None
        if Position.checkGameOver(position) != -1: 
            return Engine.staticEvaluation(position)*(depth+1), None # From current player's perspective
        maxEval, bestMove = float('-inf'), None
        moves = Engine.orderMoves(MoveGeneration.getLegalMoves(position))
        for move in moves:
            position, moveLog = MoveHandling.performMove(move, position, moveLog, False)
            # if Utils.hashKey(position) in Engine.positionHashes:

            eval, _ = Engine.negamax(position, moveLog, -beta, -alpha, depth-1)
            eval = - eval
            if eval > maxEval: maxEval, bestMove = eval, move
            alpha = max(alpha, maxEval)
            position, moveLog = MoveHandling.undoMove(position, moveLog)
            if alpha >= beta:
                break
        return maxEval, bestMove
    
    def quiescence(position, moveLog, alpha, beta):
        eval = Engine.staticEvaluation(position)
        if eval >= beta:
            return beta
        if eval > alpha:
            alpha = eval
        moves = MoveGeneration.getLegalMoves(position)
        orderedCaptures = Engine.orderMoves([move for move in moves if move.capturedPiece])
        for move in orderedCaptures:
            position, moveLog = MoveHandling.performMove(move, position, moveLog, False)
            score = - Engine.quiescence(position, moveLog, -beta, -alpha)
            position, moveLog = MoveHandling.undoMove(position, moveLog)
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        return alpha



    def orderMoves(moves):
        movePriorities = []
        for move in moves:
            if not move.capturedPiece: 
                movePriorities.append([0, move]) # no capture, don't prioritize
                continue
            capturedDiff = Engine.pieceValues[move.capturedPiece.upper()] - Engine.pieceValues[move.piece.upper()] + 300
            movePriorities.append([capturedDiff, move])
        orderedMoves = sorted(movePriorities, key=lambda x: x[0], reverse=True)
        return [movePrio[1] for movePrio in orderedMoves]


    def staticEvaluation(position):
        gameResult = Position.checkGameOver(position)
        if gameResult != -1: return gameResult

        whiteScore, blackScore = 0, 0
        for piece, value in Engine.pieceValues.items():
            for r, c in position.pieceLocations[piece]:
                whiteScore += value + Engine.pieceSquareTableMapping[piece][r*8+c]
            for r, c in position.pieceLocations[piece.lower()]:
                blackScore += value + Engine.pieceSquareTableMapping[piece.lower()][r*8+c]

        if whiteScore == 0 or blackScore == 0: # Winning player wants kings close
            wKR, wKC = position.pieceLocations['K'][0]
            bKR, bKC = position.pieceLocations['k'][0]
            distance = ((wKR-bKR)**2+(wKC-bKC)**2)**.5
            kingDistanceScore = 500 - 30*distance
            if blackScore == 0: 
                whiteScore += kingDistanceScore
                avoidSideRow = min(bKR, 7-bKR)
                avoidSideCol = min(bKC, 7-bKC)
                blackScore -= (7-avoidSideRow)*50
                blackScore -= (7-avoidSideCol)*50
            elif whiteScore == 0: 
                blackScore += kingDistanceScore
                avoidSideRow = min(wKR, 7-wKR)
                avoidSideCol = min(wKC, 7-wKC)
                whiteScore -= (7-avoidSideRow)*50
                whiteScore -= (7-avoidSideCol)*50

        whiteScore += Engine.kingSquareTableMapping[whiteScore<=900 and blackScore<=900]['K'][position.pieceLocations['K'][0][0]*8+position.pieceLocations['K'][0][1]]
        blackScore += Engine.kingSquareTableMapping[whiteScore<=900 and blackScore<=900]['k'][position.pieceLocations['k'][0][0]*8+position.pieceLocations['K'][0][1]]



        if position.currentTurn == 'b':
            return blackScore - whiteScore
        else: # White to move
            return whiteScore - blackScore