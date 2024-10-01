from MoveGeneration import MoveGeneration
from MoveHandling import MoveHandling
from Engine import Engine
from copy import deepcopy
import timeit
import time

class Debugger:


    def perft(position, moveLog, depth):
        if depth == 0:
            return 1
        
        totalNodes = 0
        allMoves = MoveGeneration.getLegalMoves(position)
        for move in allMoves:
            position, moveLog = MoveHandling.performMove(move, position, moveLog, False)

            moveNodes = Debugger.perft(position, moveLog, depth - 1)
            # if depth == 3:
            #     print(move, moveNodes)
            totalNodes += moveNodes


            # totalNodes += Debugger.perft(position, positionLog, depth - 1)
            position, moveLog = MoveHandling.undoMove(position, moveLog)
        
        return totalNodes
    
    def runPerft(position, depth):
        startTime = time.time()
        perftResult = Debugger.perft(deepcopy(position), [], depth)
        endTime = time.time()

        print(f'PERFT AT DEPTH {depth} TOOK {round(endTime-startTime,2)} SECONDS, WITH A RESULT OF: {perftResult}')

        
    def runNegaMax(position, depth):
        startTime = time.time()
        eval = Engine.search(position, depth)
        endTime = time.time()
        print(f'NEGAMAX AT DEPTH {depth} TOOK {round(endTime-startTime,2)} SECONDS, WITH A RESULT OF: {eval}')

    def testOrderMoves(position):
        allMoves = MoveGeneration.getLegalMoves(position)
        for move in allMoves:
            print(move)

        print('\n\n\n')
        orderedMoves = Engine.orderMoves(allMoves)
        for move in orderedMoves:
            print(move)

    
    def testStaticEvaluation(position):
        print(Engine.staticEvaluation(position))