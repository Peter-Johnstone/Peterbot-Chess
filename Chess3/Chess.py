from Position import Position
from Utilities import Utils
from MoveGeneration import MoveGeneration
from MoveHandling import MoveHandling
from Display import Display
from Debugger import Debugger
from Engine import Engine
import threading
import time
import pygame
from copy import deepcopy



## READ https://chess.stackexchange.com/questions/15494/validate-engine-moves-using-perft-and-divide
class Chess:
    def __init__(self, COMPUTER_COLOR = 'b', PLAYER_COLOR = 'w', themeName = 'classic'):
        # Changing variables
        startingPosition = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.position = Position(startingPosition) # FEN notation
        self.legalMoves = [] # represents the legal moves of the piece at the presently selected field
        self.moveLog = []
        self.positionLog = []
        
        
        # Constant variables
        self.COMPUTER_COLOR = COMPUTER_COLOR
        self.PLAYER_COLOR = PLAYER_COLOR
        self.DISPLAY = Display(800, themeName)
        self.PLAYERS_ONLY = False
        self.ENGINES_ONLY = False
        self.FLIPPED = PLAYER_COLOR == 'b'


        self.ENGINE = Engine(2)
        self.ENGINE2 = Engine(1) # Engine2 plays as PLAYER_COLOR


    def startGame(self):
        self.DISPLAY.createBoard()
        self.run()

    def run(self):
        self.DISPLAY.drawBoard()
        self.DISPLAY.drawPieces(self.position.board)
        pygame.display.update()
        clock = pygame.time.Clock()
        while True:
            self.checkEvents()
            clock.tick(60) # This increases performance dramatically

    def checkEvents(self):
        uKeyPressed = False
        
        mouseDown = False
        pygame.display.update()


        for event in pygame.event.get():

            # Check if game quit
            if event.type == pygame.QUIT:
                pygame.quit()

            # Check if resize window
            elif event.type == pygame.VIDEORESIZE:
                    self.DISPLAY.handleResize(event.w, event.h, self.position.board, self.legalMoves)
                    pygame.display.update()

            # Check if left click
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not mouseDown:
                mouseDown = True
                clickedRow = int((event.pos[1] - self.DISPLAY.yOffset)// self.DISPLAY.gridSize)
                clickedCol = int((event.pos[0] - self.DISPLAY.xOffset)// self.DISPLAY.gridSize)
                if not (0<=clickedRow<=7 and 0<=clickedCol<=7): continue
                self.playerMove(clickedRow, clickedCol, event.pos[0], event.pos[1])
                pygame.display.update()
                self.engineMove()

            
            # Check if mouse lifted
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouseDown = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_u and not uKeyPressed:
                uKeyPressed = True
                self.position, self.moveLog = MoveHandling.undoMove(self.position, self.moveLog)
                self.DISPLAY.drawBoard()
                self.DISPLAY.drawPieces(self.position.board)

            elif event.type == pygame.KEYUP and event.key == pygame.K_u:
                uKeyPressed = False


    def playerMove(self, r, c, rMouse, cMouse):
        if self.gameOverEvent == True:
            return
        if self.position.currentTurn == self.PLAYER_COLOR or self.PLAYERS_ONLY and not self.ENGINES_ONLY:
            for move in self.legalMoves:
                if [r, c] == move.end:
                    if move.promotionPiece and not self.DISPLAY.handlingPromotion:
                        self.DISPLAY.handlePromotion(r,c, self.position.currentTurn)
                        return
                    if self.DISPLAY.handlingPromotion:
                        move = self.updateMovePromotionPiece(r, c, rMouse, cMouse, move)
                        self.DISPLAY.handlingPromotion = False
                    self.position, self.moveLog = MoveHandling.performMove(move, self.position, self.moveLog)
                    self.legalMoves = []
                    self.DISPLAY.highlightSelectedSquare(r, c, self.position)
                    return
            self.legalMoves = MoveGeneration.getPieceMoves(r, c, self.position)
            self.DISPLAY.highlightSelectedSquare(r, c, self.position)
            self.DISPLAY.displayPieceLegalMoves(self.legalMoves)
            return
        
        self.legalMoves = []
    
    def engineMove(self):
        if self.gameOverEvent() == True: 
            pygame.display.update()
            return
        if self.PLAYERS_ONLY: return
        def getMoveForEngine(engine):
            timeStart = time.time()
            engineMove = engine.getMove(deepcopy(self.position))
            timeEnd = time.time()
            print(round(timeEnd-timeStart, 2))
            self.position, self.moveLog = MoveHandling.performMove(engineMove, self.position, self.moveLog)
            self.DISPLAY.drawBoard()
            self.DISPLAY.drawPieces(self.position.board)
            pygame.display.update()

        if self.position.currentTurn == self.COMPUTER_COLOR:
            getMoveForEngine(self.ENGINE)
        if self.ENGINES_ONLY:
            getMoveForEngine(self.ENGINE2)
            self.engineMove()



    def updateMovePromotionPiece(self, clickedRow, clickedCol, mouseX, mouseY, move):
        squareCenterX = self.DISPLAY.gridSize * clickedCol + self.DISPLAY.gridSize/2
        squareCenterY = self.DISPLAY.gridSize * clickedRow + self.DISPLAY.gridSize/2
        if mouseX < squareCenterX:
            if mouseY < squareCenterY:
                move.promotionPiece = Utils.getPieceMatchTurn(self.PLAYER_COLOR,"N")
            else:
                move.promotionPiece = Utils.getPieceMatchTurn(self.PLAYER_COLOR,"R")
        else: 
            if mouseY < squareCenterY:
                move.promotionPiece = Utils.getPieceMatchTurn(self.PLAYER_COLOR,"B")
            else:
                move.promotionPiece = Utils.getPieceMatchTurn(self.PLAYER_COLOR,"Q")
        return move
    
    def gameOverEvent(self):
        self.position.gameOver = Position.checkGameOver(self.position)
        
        if self.position.gameOver != -1:
            if self.DISPLAY.gameResult == -1:
                if self.position.gameOver == 0:
                    self.DISPLAY.gameResult = 0
                else:
                    if self.position.currentTurn == 'w':
                        self.DISPLAY.gameResult = 100
                    else:
                        self.DISPLAY.gameResult = -100
                self.DISPLAY.drawGameOver()
                pygame.display.update()
            return True
        return False






chess = Chess()

# Debugger.runPerft(chess.position, 4)
# Debugger.testStaticEvaluation(chess.position)
# Debugger.runNegaMax(chess.position, 4)
# Debugger.testOrderMoves(chess.position)
chess.startGame()