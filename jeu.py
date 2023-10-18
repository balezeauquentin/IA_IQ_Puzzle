# Création du plateau
class Board:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = [[0 for _ in range(width)] for _ in range(height)]

    def __copy__(self):
        return Board(self.height, self.width)

    def __len__(self):
        return self.height
    
    def __getitem__(self, i):
        return self.board[i]
    
    def __setitem__(self, i, val):
        self.board[i] = val

    def afficher_tableau_console(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 0:
                    print(" . ", end="")
                else:
                    print(" " + chr(ord('A') + self.board[i][j] - 1) + " ", end="")
            print("\n", end="")

# Création d'une pièce (exemple avec une pièce en forme de L)
class Piece:
    def __init__(self, id):
        self.id = id

        # Liste des pièces
        if id == 1:
            # 1 = L
            self.piece = [
                [1, 0],
                [1, 0],
                [1, 1]
            ]
            
        elif id == 2:
            # 2 = L2
            self.piece = [
                [2, 0],
                [2, 0],
                [2, 0],
                [2, 2]
            ]
            
        elif id == 3:
            # 3 = L3
            self.piece = [
                [3, 0],
                [3, 3],
            ]
            
        elif id == 4:
            # 4 = L4
            self.piece = [
                [4, 0, 0],
                [4, 0, 0],
                [4, 4, 4]
            ]
            
        elif id == 5:
            # 5 = U
            self.piece = [
                [5, 5],
                [5, 0],
                [5, 5]
            ]
            
        elif id == 6:
            # 6 = T
            self.piece = [
                [6, 6, 6],
                [0, 6, 0]
            ]
            
        elif id == 7:
            # 7 = Z
            self.piece = [
                [7, 7, 0],
                [0, 7, 7],
            ]
            
        elif id == 8:
            # 8 = Z2
            self.piece = [
                [8, 8, 8, 8],
                [0, 8, 0, 0]
            ]
            
        elif id == 9:
            # 9 = truc
            self.piece = [
                [0, 0, 9],
                [9, 9, 9],
                [0, 9, 0]
            ]
            
        elif id == 10:
            # 10 = C
            self.piece = [
                [10, 0],
                [10, 10],
                [10, 10]
            ]
            
        elif id == 11:
            # 11 = Z2
            self.piece = [
                [11, 11, 11, 0],
                [0, 0, 11, 11],
            ]
            
        elif id ==12:
            self.piece = [
                [12,12,0],
                [0,12,12],
                [0,0,12]
            ]
            
    def turnPiece(self):
        self.piece = [list(reversed(col)) for col in zip(*self.piece)]


# Fonction pour placer une pièce sur le plateau
def placePiece(board, piece, position):
    if verifPlacePiece(Board, piece.piece, position):
        for i in range(len(piece.piece)):
            for j in range(len(piece.piece[0])):
                if piece.piece[i][j] != 0:
                    board[position[0] + i][position[1] + j] = piece.piece[i][j]
        # afficher_plateau(plateau)
        return True
    else:
        print("Impossible de placer la pièce ici")
        return False

# Fonction pour vérifier si une pièce peut être placée à un certain endroit
def verifPlacePiece(board, piece, position):
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if (
                    position[0] + i < 0  # si la position est en dehors du plateau dans le nega
                    or position[1] + j < 0  # si la position est en dehors du plateau dans le nega
                    or position[0] + i >= len(board)  # si la position est en dehors du plateau dans le pos
                    or position[1] + j >= len(board[0])  # si la position est en dehors du plateau dans le pos
                    or (piece[i][j] != 0 and board[position[0] + i][position[1] + j] != 0)
                    # si la case est deja prise
            ):
                return False
    return True

# Fonction pour afficher le plateau
def showBoard(table):
    for ligne in table.plateau:
        showLine = ""
        for case in ligne:
            if case == 0:
                showLine += " . "
            else:
                showLine += " " + chr(ord('A') + case - 1) + " "

        print(showLine)


# table = plateau(5, 11)
# position = (2, 0)
# forme1 = piece(1)
# forme2 = piece(1)
# placer_piece(table, forme1, position)
# placer_piece(table, forme2, (0, 0))

# table.afficher_tableau_console()
