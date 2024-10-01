import pygame
import json


class AssetManager:
    pygame.mixer.init()
    moveSound = pygame.mixer.Sound('SoundAssets/moveSound.mp3')
    captureSound = pygame.mixer.Sound('SoundAssets/captureSound.mp3')

    def __init__(self, gridSize, themeName):
        self.themeName = themeName
        with open("themes.json", "r") as file:
            themes = json.load(file)
            selectedTheme = themes.get(themeName, themes[themeName])
        self.themeExtension = selectedTheme["IMAGE_EXTENSION"]
        self.scaleImages(gridSize) # (and initialize)

    def initializeImages(self):
        pygame.init()
            # Miscellaneous
        self.icon = pygame.image.load(f"ImageAssets/knight.png")
        self.circle = pygame.image.load(f"ImageAssets/circle.png")

            # white pieces
        self.whitePawn = pygame.image.load(f"ImageAssets/{self.themeName}/wP.{self.themeExtension}")
        self.whiteKnight = pygame.image.load(f"ImageAssets/{self.themeName}/wN.{self.themeExtension}")
        self.whiteBishop = pygame.image.load(f"ImageAssets/{self.themeName}/wB.{self.themeExtension}")
        self.whiteRook = pygame.image.load(f"ImageAssets/{self.themeName}/wR.{self.themeExtension}")
        self.whiteQueen = pygame.image.load(f"ImageAssets/{self.themeName}/wQ.{self.themeExtension}")
        self.whiteKing = pygame.image.load(f"ImageAssets/{self.themeName}/wK.{self.themeExtension}")

            # black pieces
        self.blackPawn = pygame.image.load(f"ImageAssets/{self.themeName}/bP.{self.themeExtension}")
        self.blackKnight = pygame.image.load(f"ImageAssets/{self.themeName}/bN.{self.themeExtension}")
        self.blackBishop = pygame.image.load(f"ImageAssets/{self.themeName}/bB.{self.themeExtension}")
        self.blackRook = pygame.image.load(f"ImageAssets/{self.themeName}/bR.{self.themeExtension}")
        self.blackQueen = pygame.image.load(f"ImageAssets/{self.themeName}/bQ.{self.themeExtension}")
        self.blackKing = pygame.image.load(f"ImageAssets/{self.themeName}/bK.{self.themeExtension}")

    def scaleImages(self, gridSize):
        self.initializeImages()
        # Scale all images
            # Miscellaneous
        self.circle = pygame.transform.smoothscale(self.circle, (gridSize, gridSize))

            # white pieces
        self.whitePawn = pygame.transform.smoothscale(self.whitePawn, (gridSize, gridSize))
        self.whiteKnight = pygame.transform.smoothscale(self.whiteKnight, (gridSize, gridSize))
        self.whiteBishop = pygame.transform.smoothscale(self.whiteBishop, (gridSize, gridSize))
        self.whiteRook = pygame.transform.smoothscale(self.whiteRook, (gridSize, gridSize))
        self.whiteQueen = pygame.transform.smoothscale(self.whiteQueen, (gridSize, gridSize))
        self.whiteKing = pygame.transform.smoothscale(self.whiteKing, (gridSize, gridSize))

            # black pieces
        self.blackPawn = pygame.transform.smoothscale(self.blackPawn, (gridSize, gridSize))
        self.blackKnight = pygame.transform.smoothscale(self.blackKnight, (gridSize, gridSize))
        self.blackBishop = pygame.transform.smoothscale(self.blackBishop, (gridSize, gridSize))
        self.blackRook = pygame.transform.smoothscale(self.blackRook, (gridSize, gridSize))
        self.blackQueen = pygame.transform.smoothscale(self.blackQueen, (gridSize, gridSize))
        self.blackKing = pygame.transform.smoothscale(self.blackKing, (gridSize, gridSize))

    

    def handlePromotionImages(self, size):
        # Load Images
        self.whiteKnightPromotion = pygame.image.load(f"ImageAssets/{self.themeName}/ForPromotion/wN.{self.themeExtension}")
        self.whiteBishopPromotion = pygame.image.load(f"ImageAssets/{self.themeName}/ForPromotion/wB.{self.themeExtension}")
        self.whiteRookPromotion = pygame.image.load(f"ImageAssets/{self.themeName}/ForPromotion/wR.{self.themeExtension}")
        self.whiteQueenPromotion = pygame.image.load(f"ImageAssets/{self.themeName}/ForPromotion/wQ.{self.themeExtension}")

        self.blackKnightPromotion = pygame.image.load(f"ImageAssets/{self.themeName}/ForPromotion/bN.{self.themeExtension}")
        self.blackBishopPromotion = pygame.image.load(f"ImageAssets/{self.themeName}/ForPromotion/bB.{self.themeExtension}")
        self.blackRookPromotion = pygame.image.load(f"ImageAssets/{self.themeName}/ForPromotion/bR.{self.themeExtension}")
        self.blackQueenPromotion = pygame.image.load(f"ImageAssets/{self.themeName}/ForPromotion/bQ.{self.themeExtension}")

        # Scale Images
        self.whiteKnightPromotion = pygame.transform.smoothscale(self.whiteKnightPromotion, (size, size))
        self.whiteBishopPromotion = pygame.transform.smoothscale(self.whiteBishopPromotion, (size, size))
        self.whiteRookPromotion = pygame.transform.smoothscale(self.whiteRookPromotion, (size, size))
        self.whiteQueenPromotion = pygame.transform.smoothscale(self.whiteQueenPromotion, (size, size))

        self.blackKnightPromotion = pygame.transform.smoothscale(self.blackKnightPromotion, (size, size))
        self.blackBishopPromotion = pygame.transform.smoothscale(self.blackBishopPromotion, (size, size))
        self.blackRookPromotion = pygame.transform.smoothscale(self.blackRookPromotion, (size, size))
        self.blackQueenPromotion = pygame.transform.smoothscale(self.blackQueenPromotion, (size, size))
    
