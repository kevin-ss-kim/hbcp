import sys
'''
Written by Seong Soo (Kevin) Kim
'''


class ChessBoard:
    '''
    I have represented the chessboard as a dictionary where 
    the key is a length-2 string representing coordinate and 
    the value is a ChessPiece class. The coordinate uses algebraic notation:
    http://www.chess-poster.com/english/learn_chess/notation/images/coordinates_2.gif
    I assumed that white pawns move up and black pawns move down 
    '''
    pieceMap = {}
    pieceCount = 0
    pieceLetterMap = {"k":"KING","q":"QUEEN","n":"KNIGHT","p":"PAWN","b":"BISHOP","r":"ROOK"}
    colorMap = {"b":"Black","w":"White"}
    
    def addChessPiece(self, piece, coordinate, color):
        if self.canInsertPiece(piece, coordinate) and self.hasValidNumber(piece, color):
            ChessBoard.pieceMap[coordinate] = ChessPiece(piece, coordinate, color)
            ChessBoard.pieceCount += 1
        else:
            print("\033[93mCannot insert this piece according to the chess rule\033[0m")
    
    def hasValidNumber(self, piece, color):
        if (color == 'b' or color == 'w') and piece in ChessBoard.pieceLetterMap:
            return True
        return False

    def isValidCoordinate(self, coordinate):
        if len(coordinate) == 2 and coordinate[0] >= 'a' and coordinate[0] <= 'h' and coordinate[1] >= '1' and coordinate[1] <= '8':
            return True
        return False

    def canInsertPiece(self, piece, coordinate):
        if self.isValidCoordinate(coordinate) and coordinate not in ChessBoard.pieceMap:
            return True
        return False

    def getPossibleMoves(self, color):
        if color in ChessBoard.colorMap:
            for key, value in ChessBoard.pieceMap.items():
                if value.color == color:
                    possiblePieceMoves = self.getPossiblePieceMoves(value)
                    if len(possiblePieceMoves) > 0:
                        print(str(len(possiblePieceMoves)) + " Possible Move(s) for " + ChessBoard.colorMap[value.color] + " " + ChessBoard.pieceLetterMap[value.piece] + " @ " + value.coordinate + ":")
                        print(possiblePieceMoves)
        else:
            print("\033[93mInvalid Color!\033[0m")

    # Returns an array for a particular piece
    def getPossiblePieceMoves(self, piece):
        '''
        For king and knights, add to possibleMoves if the coordinate is valid and 
        if a piece does not exist at the coordinate or 
        if a piece exists and is of a different color
        For rooks, bishops, and queen, the same rule applies but they can't go beyond a piece that is in the way
        '''
        x, y = piece.coordinate[0], piece.coordinate[1]
        possibleMoves = []
        if piece.piece == "k":
            moves = [
                chr(ord(x) + 1) + y,
                chr(ord(x) + 1) + chr(ord(y) + 1),
                x + chr(ord(y) + 1),
                chr(ord(x) - 1) + chr(ord(y) + 1),
                chr(ord(x) - 1) + y,
                chr(ord(x) - 1) + chr(ord(y) - 1),
                x + chr(ord(y) - 1),
                chr(ord(x) + 1) + chr(ord(y) - 1)
            ]
            for move in moves:
                if self.canInsertPiece(piece, move) or (self.isValidCoordinate(move) and ChessBoard.pieceMap[move].color != piece.color):
                    possibleMoves.append(move)
        elif piece.piece == "n":
            moves = [
                chr(ord(x) + 2) + chr(ord(y) + 1),
                chr(ord(x) + 1) + chr(ord(y) + 2),
                chr(ord(x) - 1) + chr(ord(y) + 2),
                chr(ord(x) - 2) + chr(ord(y) + 1),
                chr(ord(x) - 2) + chr(ord(y) - 1),
                chr(ord(x) - 1) + chr(ord(y) - 2),
                chr(ord(x) + 1) + chr(ord(y) - 2),
                chr(ord(x) + 2) + chr(ord(y) - 1)
            ]
            for move in moves:
                if self.canInsertPiece(piece, move) or (self.isValidCoordinate(move) and ChessBoard.pieceMap[move].color != piece.color):
                    possibleMoves.append(move)
        elif piece.piece == "r":
            possibleMoves = self.getRookMoves(piece)
        elif piece.piece == "b":
            possibleMoves = self.getBishopMoves(piece)
        elif piece.piece == "q":
            possibleMoves = self.getRookMoves(piece) + self.getBishopMoves(piece)
        elif piece.piece == "p":
            possibleMoves = self.getPawnMoves(piece)
        return possibleMoves

    def getRookMoves(self, piece):
        moves = []
        x, y = piece.coordinate[0], piece.coordinate[1]
        # Check top
        y = chr(ord(y) + 1)
        while y <= '8':
            if x + y in ChessBoard.pieceMap:
                if ChessBoard.pieceMap[x + y].color != piece.color:
                    moves.append(x + y)
                break
            else:
                moves.append(x + y)
            y = chr(ord(y) + 1)
        x, y = piece.coordinate[0], piece.coordinate[1]
        # Check left
        x = chr(ord(x) - 1)
        while x >= 'a':
            if x + y in ChessBoard.pieceMap:
                if ChessBoard.pieceMap[x + y].color != piece.color:
                    moves.append(x + y)
                break
            else:
                moves.append(x + y)
            x = chr(ord(x) - 1)
        x, y = piece.coordinate[0], piece.coordinate[1]
        # Check bottom
        y = chr(ord(y) - 1)
        while y >= '1':
            if x + y in ChessBoard.pieceMap:
                if ChessBoard.pieceMap[x + y].color != piece.color:
                    moves.append(x + y)
                break
            else:
                moves.append(x + y)
            y = chr(ord(y) - 1)
        x, y = piece.coordinate[0], piece.coordinate[1]
        # Check right
        x = chr(ord(x) + 1)
        while x <= 'h':
            if x + y in ChessBoard.pieceMap:
                if ChessBoard.pieceMap[x + y].color != piece.color:
                    moves.append(x + y)
                break
            else:
                moves.append(x + y)
            x = chr(ord(x) + 1)
        return moves

    def getBishopMoves(self, piece):
        moves = []
        x, y = piece.coordinate[0], piece.coordinate[1]
        # Check northeast
        x, y  = chr(ord(x) + 1), chr(ord(y) + 1)
        while x <= 'h' and y <= '8':
            if x + y in ChessBoard.pieceMap:
                if ChessBoard.pieceMap[x + y].color != piece.color:
                    moves.append(x + y)
                break
            else:
                moves.append(x + y)
            x, y = chr(ord(x) + 1), chr(ord(y) + 1)
        x, y = piece.coordinate[0], piece.coordinate[1]
        # Check northwest
        x, y = chr(ord(x) - 1), chr(ord(y) + 1)
        while x >= 'a' and y <= '8':
            if x + y in ChessBoard.pieceMap:
                if ChessBoard.pieceMap[x + y].color != piece.color:
                    moves.append(x + y)
                break
            else:
                moves.append(x + y)
            x, y = chr(ord(x) - 1), chr(ord(y) + 1)
        x, y = piece.coordinate[0], piece.coordinate[1]
        # Check southwest
        x, y = chr(ord(x) - 1), chr(ord(y) - 1)
        while x >= 'a' and y >= '1':
            if x + y in ChessBoard.pieceMap:
                if ChessBoard.pieceMap[x + y].color != piece.color:
                    moves.append(x + y)
                break
            else:
                moves.append(x + y)
            x, y = chr(ord(x) - 1), chr(ord(y) - 1)
        x, y = piece.coordinate[0], piece.coordinate[1]
        # Check southeast
        x, y = chr(ord(x) + 1), chr(ord(y) - 1)
        while x <= 'h' and y >= '1':
            if x + y in ChessBoard.pieceMap:
                if ChessBoard.pieceMap[x + y].color != piece.color:
                    moves.append(x + y)
                break
            else:
                moves.append(x + y)
            x, y = chr(ord(x) + 1), chr(ord(y) - 1)
        return moves

    def getPawnMoves(self, piece):
        moves = []
        x, y = piece.coordinate[0], piece.coordinate[1]
        if piece.color == "w":
            move1, move2, move3, move4 = x + chr(ord(y) + 1), x + chr(ord(y) + 2), chr(ord(x) + 1) + chr(ord(y) + 1), chr(ord(x) - 1) + chr(ord(y) + 1)
            if self.canInsertPiece(piece, move1):
                moves.append(move1)
            if y == "2" and self.canInsertPiece(piece, move2):
                moves.append(move2)
            if self.isValidCoordinate(move3) and move3 in ChessBoard.pieceMap and ChessBoard.pieceMap[move3].color != piece.color:
                moves.append(move3)
            if self.isValidCoordinate(move4) and move4 in ChessBoard.pieceMap and ChessBoard.pieceMap[move4].color != piece.color:
                moves.append(move4)
        else:
            move1, move2, move3, move4 = x + chr(ord(y) - 1), x + chr(ord(y) - 2), chr(ord(x) - 1) + chr(ord(y) - 1), chr(ord(x) + 1) + chr(ord(y) - 1)
            if self.canInsertPiece(piece, move1):
                moves.append(move1)
            if y == "7" and self.canInsertPiece(piece, move2):
                moves.append(move2)
            if self.isValidCoordinate(move3) and move3 in ChessBoard.pieceMap and ChessBoard.pieceMap[move3].color != piece.color:
                moves.append(move3)
            if self.isValidCoordinate(move4) and move4 in ChessBoard.pieceMap and ChessBoard.pieceMap[move4].color != piece.color:
                moves.append(move4)
        return moves


class ChessPiece:
    
    def __init__(self, piece, coordinate, color):
        self.piece = piece
        self.color = color
        self.coordinate = coordinate


def main():
    global input
    cb = ChessBoard()
    if len(sys.argv) == 1:
        print("\033[94mPlease enter in ChessPiece input\n\033[92mThe input format for ChessPiece is \nPIECE,COORDINATE,COLOR\nwhere PIECE = [k, q, n, r, b, p] and COORDINATE = [a1, a2, a3,..., h6, h7, h8] and COLOR = [w, b]\033[0m")
        while True:
            ChessPieceInfo = input('Piece:  ')
            if ChessPieceInfo == "done":
                break
            else:
                ChessPieceInfo = ChessPieceInfo.replace(" ", "").split(",")
                if len(ChessPieceInfo) != 3:
                    print("Make sure your input has 3 arguments")
                else:
                    cb.addChessPiece(ChessPieceInfo[0], ChessPieceInfo[1], ChessPieceInfo[2])
    elif len(sys.argv) == 2:
        with open(sys.argv[1]) as fp:
            for line in fp:
                ChessPieceInfo = line.rstrip().replace(" ", "").split(",")
                print("Inserting " + ChessBoard.colorMap[ChessPieceInfo[2]] + " " + ChessBoard.pieceLetterMap[ChessPieceInfo[0]] + " @ " + ChessPieceInfo[1])
                cb.addChessPiece(ChessPieceInfo[0], ChessPieceInfo[1], ChessPieceInfo[2])
    color = input("\033[92mChoose whose turn it is (w, b):  \033[0m")
    cb.getPossibleMoves(color)
        
main()