from Utilities import Utils
from Position import Position
from AssetManager import AssetManager


class MoveHandling:

    def updateCastleAvailability(move, position):
        oldCastleAvailability = position.canCastle
        if move.piece == 'k':
            position.canCastle = position.canCastle.translate(str.maketrans('', '', 'kq')) # removes k and q
        elif move.piece == 'K':
            position.canCastle = position.canCastle.translate(str.maketrans('', '', 'KQ')) # remove K and Q
        elif move.piece == 'r' and move.start == [0,0]:
            position.canCastle = position.canCastle.translate(str.maketrans('', '', 'q')) # removes q
        elif move.piece == 'r' and move.start == [0,7]:
            position.canCastle = position.canCastle.translate(str.maketrans('', '', 'k')) # removes k
        elif move.piece == 'R' and move.start == [7,0]:
            position.canCastle = position.canCastle.translate(str.maketrans('', '', 'Q')) # removes Q
        elif move.piece == 'R' and move.start == [7,7]:
            position.canCastle = position.canCastle.translate(str.maketrans('', '', 'K')) # removes K
        if position.canCastle != oldCastleAvailability:
            move.changesCastleAvailability = oldCastleAvailability
        return position
    
    def castleUpdateRookLocation(move, position):
        if move.castleSide == "queenside":
            if Utils.isWhite(move.piece):
                position.board[7][0] = '.'
                position.board[7][3] = 'R'
            else: # piece is black
                position.board[0][0] = '.'
                position.board[0][3] = 'r'
        elif move.castleSide == "kingside":
            if Utils.isWhite(move.piece):
                position.board[7][7] = '.'
                position.board[7][5] = 'R'
            else: # piece is black
                position.board[0][7] = '.'
                position.board[0][5] = 'r'
        return position

    def castleRevertRookLocation(move, position):
        if move.castleSide == "queenside":
            if Utils.isWhite(move.piece):
                position.board[7][0] = 'R'
                position.board[7][3] = '.'
            else: # piece is black
                position.board[0][0] = 'r'
                position.board[0][3] = '.'
        elif move.castleSide == "kingside":
            if Utils.isWhite(move.piece):
                position.board[7][7] = 'R'
                position.board[7][5] = '.'
            else: # piece is black
                position.board[0][7] = 'r'
                position.board[0][5] = '.'
        return position

    def updateEnPassantSquare(move, position):
        position.enPassantSquare = []
        if move.piece.lower() == 'p' and abs(move.start[0]-move.end[0]) == 2:
            position.enPassantSquare = [max(move.start[0],move.end[0])-1, move.end[1]]
        return position
                                        

    def performMove(move, position, moveLog, sound = True):
        moveLog.append(move)
        position.currentTurn = Utils.switchTurns(position.currentTurn)

        # In all cases
        position.board[move.start[0]][move.start[1]] = "."
        position.board[move.end[0]][move.end[1]] = move.promotionPiece if move.promotionPiece else move.piece
        
        position = MoveHandling.updateCastleAvailability(move, position) # Prohibits future castling after rook/king moves
        position = MoveHandling.castleUpdateRookLocation(move, position) # Moves the rook if castle move
        position = MoveHandling.updateEnPassantSquare(move, position) # Updates the valid en passant square
        
        if move.isEnPassant:
            # Location of captured pawn
            position.board[move.start[0]][move.end[1]] = '.'

        position.getPieceLocations() 
        position.getPinsAndChecks()

        if sound: AssetManager.captureSound.play() if (move.capturedPiece or move.isEnPassant) else AssetManager.moveSound.play()
        return position, moveLog
    
    def undoMove(position, moveLog):
        if not moveLog: return position, moveLog # No previous move
        lastMove = moveLog.pop()
        position.board[lastMove.start[0]][lastMove.start[1]] = lastMove.piece
        if lastMove.capturedPiece: # Piece was captured at the last move end square
            position.board[lastMove.end[0]][lastMove.end[1]] = lastMove.capturedPiece
        else: # No piece was captured, therefore it was empty before
            position.board[lastMove.end[0]][lastMove.end[1]] = '.'
        if lastMove.isEnPassant: # We need to revert the en passant capture
            position.board[lastMove.start[0]][lastMove.end[1]] = Utils.opposeFirstPieceColor(lastMove.piece, 'p')
        
        if lastMove.changesCastleAvailability: # Last moved either the king or rook moved, therefore changed future castling rights
            position.canCastle = lastMove.changesCastleAvailability # We saved the old rights in the move.
        
        position = MoveHandling.castleRevertRookLocation(lastMove, position)

        # revert en passant square
        if moveLog: # a move before last
            moveBeforeLast = moveLog[-1]
            position = MoveHandling.updateEnPassantSquare(moveBeforeLast, position)

        position.getPieceLocations() 
        position.getPinsAndChecks()
        position.currentTurn = Utils.switchTurns(position.currentTurn)

        
        return position, moveLog
    
    def nullMove(position):
        position.currentTurn = Utils.switchTurns(position.currentTurn)
        return position