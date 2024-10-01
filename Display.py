import pygame
import pygame.gfxdraw
from AssetManager import AssetManager
from Utilities import Utils
import json

class Display:

    def __init__(self, boardSize, themeName):

        # changing variables
        self.boardSize = boardSize
        self.gridSize = boardSize/8
        self.width = boardSize
        self.height = boardSize
        self.xOffset = 0
        self.yOffset = 0
        self.gameResult = -1
        self.handlingPromotion = False

        # constant variables
        with open('themes.json', 'r') as file:
            themes = json.load(file)
            selectedTheme = themes.get(themeName, themes[themeName])
        self.WHITE = selectedTheme['WHITE']
        self.BLACK = selectedTheme['BLACK']
        self.SELECTED_SQUARE_COLOR = selectedTheme['SELECTED_SQUARE_COLOR']
        self.BACKGROUND_COLOR = selectedTheme['BACKGROUND_COLOR']
        self.LINE_COLOR = selectedTheme['LINE_COLOR']
        self.CIRCLE_OUTLINE_COLOR = selectedTheme['CIRCLE_OUTLINE_COLOR']
        self.CIRCLE_COLOR = selectedTheme['CIRCLE_COLOR']
        # https://github.com/lichess-org/lila/tree/master/public/piece
        self.ASSETS = AssetManager(self.gridSize, themeName) # Initialize images and sounds

    def createBoard(self):
        self.boardDisplay = pygame.display.set_mode((self.boardSize,self.boardSize), pygame.RESIZABLE)
        self.boardDisplay.fill(self.BACKGROUND_COLOR)
        pygame.display.set_caption('Chess')
        pygame.display.set_icon(self.ASSETS.icon)

    def handleResize(self, width, height, board, legalMoves):
        self.height = height
        self.width = width
        self.boardSize = min(self.width, self.height)
        self.gridSize = self.boardSize/8
        self.boardDisplay.fill(self.BACKGROUND_COLOR)
        self.ASSETS.scaleImages(self.gridSize)
        self.xOffset = max((self.width - self.height) // 2, 0)
        self.yOffset = max((self.height - self.width) // 2, 0)  
        
        self.drawBoard()
        self.drawPieces(board)
        self.displayPieceLegalMoves(legalMoves)

    
    def displayPiece(self, row, col, x, y, board):
        piece = board[row][col]
        if piece == '.': return
        piece_mapping = {
            'P': self.ASSETS.whitePawn,
            'N': self.ASSETS.whiteKnight,
            'B': self.ASSETS.whiteBishop,
            'R': self.ASSETS.whiteRook,
            'Q': self.ASSETS.whiteQueen,
            'K': self.ASSETS.whiteKing,
            'p': self.ASSETS.blackPawn,
            'n': self.ASSETS.blackKnight,
            'b': self.ASSETS.blackBishop,
            'r': self.ASSETS.blackRook,
            'q': self.ASSETS.blackQueen,
            'k': self.ASSETS.blackKing,
        }
        self.boardDisplay.blit(piece_mapping[piece], (x, y))

    def drawBoard(self):
        pygame.draw.rect(self.boardDisplay, self.WHITE, (self.xOffset, self.yOffset, self.boardSize, self.boardSize))
        for row in range(8):
            for col in range(8):
                
                x = col * self.gridSize + self.xOffset
                y = row * self.gridSize + self.yOffset
                # Alternate colors
                color = self.WHITE if (row + col) % 2 == 0 else self.BLACK
                pygame.draw.rect(self.boardDisplay, color, (x, y, self.gridSize, self.gridSize))
    

    def drawPieces(self, board):
        for row in range(8):
            for col in range(8):
                x = col * self.gridSize + self.xOffset
                y = row * self.gridSize + self.yOffset
                self.displayPiece(row, col, x, y, board)


    def displayPieceLegalMoves(self, pieceLegalMoves):
        for move in pieceLegalMoves:
            xCenter = int(move.end[1] * self.gridSize + self.xOffset + self.gridSize/2)
            yCenter = int(move.end[0] * self.gridSize + self.yOffset + self.gridSize/2)
            circleRadius = int(self.gridSize/6)
            pygame.gfxdraw.filled_circle(self.boardDisplay, xCenter, yCenter, circleRadius, self.CIRCLE_COLOR)
            pygame.gfxdraw.aacircle(self.boardDisplay, xCenter, yCenter, circleRadius, self.CIRCLE_OUTLINE_COLOR)
    

    def highlightSelectedSquare(self, row, col, position):
        self.drawBoard()
        if Utils.turnMatchesPiece(position.currentTurn, position.board[row][col]):
            rect = (
                col * self.gridSize + self.xOffset,
                row * self.gridSize + self.yOffset,
                self.gridSize,
                self.gridSize
            )
            pygame.draw.rect(self.boardDisplay, self.SELECTED_SQUARE_COLOR, rect)
        self.drawPieces(position.board)


    def handlePromotion(self, r, c, turn):
        self.handlingPromotion = True
        x = c * self.gridSize + self.xOffset
        y = r * self.gridSize + self.yOffset

        pygame.draw.rect(self.boardDisplay, self.BACKGROUND_COLOR, (x, y,self.gridSize,self.gridSize))
                                                                                            # this -1 makes it fit better for some reason
        pygame.draw.line(self.boardDisplay, (self.LINE_COLOR), (x, y+self.gridSize/2), (x+self.gridSize-1, y+self.gridSize/2))
        pygame.draw.line(self.boardDisplay, (self.LINE_COLOR), (x+self.gridSize/2, y), (x+self.gridSize/2, y+self.gridSize-1))

        self.ASSETS.handlePromotionImages(self.gridSize/2)

        if turn == 'w':
            self.boardDisplay.blit(self.ASSETS.whiteKnightPromotion, (x, y))
            self.boardDisplay.blit(self.ASSETS.whiteBishopPromotion, (x+self.gridSize/2, y))
            self.boardDisplay.blit(self.ASSETS.whiteRookPromotion, (x, y+self.gridSize/2))
            self.boardDisplay.blit(self.ASSETS.whiteQueenPromotion, (x+self.gridSize/2, y+self.gridSize/2))
        
        elif turn == 'b':
            self.boardDisplay.blit(self.ASSETS.blackKnightPromotion, (x, y))
            self.boardDisplay.blit(self.ASSETS.blackBishopPromotion, (x+self.gridSize/2, y))
            self.boardDisplay.blit(self.ASSETS.blackRookPromotion, (x, y+self.gridSize/2))
            self.boardDisplay.blit(self.ASSETS.blackQueenPromotion, (x+self.gridSize/2, y+self.gridSize/2))

    def drawGameOver(self):
        font = pygame.font.Font(None, 36)
        textColor = (1, 50, 32)
        textDict = {0: "DRAW", 100: "BLACK WINS", -100: "WHITE WINS"}

        if self.gameResult in textDict:
            text = textDict[self.gameResult]
            textSurface = font.render(text, True, textColor)
            textRect = textSurface.get_rect(center=(self.width // 2, self.height // 2))
            self.boardDisplay.blit(textSurface, textRect)

        pygame.display.update()