# Création du plateau
class Board:
    used_shapes = []
    def __init__(self, height, width):
        """
        Initializes a new Board instance with a specified height and width.
        The board is represented as a 2D list filled with zeros.

        Parameters:
        - height: The number of rows in the board.
        - width: The number of columns in the board.
        """
        self.height = height
        self.width = width
        self.board = [[0 for _ in range(width)] for _ in range(height)]

    def __copy__(self):
        """
        Creates a copy of the current Board instance.

        Returns:
        - A new Board instance with the same height and width.
        """
        return Board(self.height, self.width)

    def __len__(self):
        """
        Returns the height of the board.

        Returns:
        - Integer: The height of the board.
        """
        return self.height
    
    def __getitem__(self, i):
        """
        Allows access to a row of the board using subscript notation.

        Parameters:
        - i: The index of the row.

        Returns:
        - List: The row at index 'i'.
        """
        return self.board[i]
    
    def __setitem__(self, i, val):
        """
        Allows setting a row of the board using subscript notation.

        Parameters:
        - i: The index of the row.
        - val: The new value for the row.
        """
        self.board[i] = val

    def printBoard(self):
        """
        Prints the board to the console. 
        Empty cells are represented by '.', and filled cells are represented by letters.
        """
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 0:
                    print(" . ", end="")
                else:
                    print(" " + chr(ord('A') + self.board[i][j] - 1) + " ", end="")
            print("\n", end="")

    # Fonction pour placer une pièce sur le plateau
    def placeShape(self, piece, position):
        """
        Prints the board to the console. 
        Empty cells are represented by '.', and filled cells are represented by letters.
        """
        if self.canPlaceShape(piece, position):
            self.used_shapes.append(piece.id)
            for i in range(len(piece.piece)):
                for j in range(len(piece.piece[0])):
                    if piece.piece[i][j] != 0:
                        self[position[0] + i][position[1] + j] = piece.piece[i][j]
            # afficher_plateau(plateau)
            return True
        else:
            # print("Impossible de placer la pièce ici", position)
            return False

    # Fonction pour vérifier si une pièce peut être placée à un certain endroit
    def canPlaceShape(self, piece, position):
        """
        Checks if a given piece can be placed on the board at a specified position.

        Parameters:
        - piece: The piece to check.
        - position: The top-left position to check for placement.

        Returns:
        - Boolean: True if the piece can be placed, False otherwise.
        """
        if piece.id in self.used_shapes:
            return False
        for i in range(len(piece.piece)):
            for j in range(len(piece.piece[0])):
                if (
                        position[0] + i < 0  # si la position est en dehors du plateau dans le nega
                        or position[1] + j < 0  # si la position est en dehors du plateau dans le nega
                        or position[0] + i >= len(self)  # si la position est en dehors du plateau dans le pos
                        or position[1] + j >= len(self[0])  # si la position est en dehors du plateau dans le pos
                        or (piece.piece[i][j] != 0 and self[position[0] + i][position[1] + j] != 0)
                        # si la case est deja prise
                ):
                    return False
        return True
    
    def isFinished(self):
        for line in self:
            for cell in line:
                if cell == 0:
                    return False
        return True


# Création d'une pièce (exemple avec une pièce en forme de L)
class Piece:
    def __init__(self, id):
        """
        Initializes a new Piece instance with a specified ID.
        Each ID corresponds to a different shape.

        Parameters:
        - id: The ID of the piece, determining its shape.
        """
        self.id = id

        # Liste des pièces
        if id == 1:
            # 1 = L
            self.piece = [
                [1, 0],
                [1, 0],
                [1, 1]
            ]
            self.can_miror=True
            self.rotation = 4
            
        elif id == 2:
            # 2 = L2
            self.piece = [
                [2, 0],
                [2, 0],
                [2, 0],
                [2, 2]
            ]
            self.can_miror=True
            self.rotation = 4
            
        elif id == 3:
            # 3 = L3
            self.piece = [
                [3, 0],
                [3, 3],
            ]
            self.can_miror=False
            self.rotation = 4
        elif id == 4:
            # 4 = L4
            self.piece = [
                [4, 0, 0],
                [4, 0, 0],
                [4, 4, 4]
            ]
            self.can_miror=False
            self.rotation = 4
        elif id == 5:
            # 5 = U
            self.piece = [
                [5, 5],
                [5, 0],
                [5, 5]
            ]
            self.can_miror=False
            self.rotation = 4
            
        elif id == 6:
            # 6 = T
            self.piece = [
                [6, 6, 6],
                [0, 6, 0]
            ]
            self.can_miror=False
            self.rotation = 4
            
        elif id == 7:
            # 7 = Z
            self.piece = [
                [7, 7, 0],
                [0, 7, 7],
            ]
            self.can_miror=True
            self.rotation = 2
        elif id == 8:
            # 8 = Z2
            self.piece = [
                [8, 8, 8, 8],
                [0, 8, 0, 0]
            ]
            self.can_miror=True
            self.rotation = 4
            
        elif id == 9:
            # 9 = truc
            self.piece = [
                [0, 0, 9],
                [9, 9, 9],
                [0, 9, 0]
            ]
            self.can_miror=True
            self.rotation = 4
        elif id == 10:
            # 10 = C
            self.piece = [
                [10, 0],
                [10, 10],
                [10, 10]
            ]
            self.can_miror=True
            self.rotation = 4

        elif id == 11:
            # 11 = Z2
            self.piece = [
                [11, 11, 11, 0],
                [0, 0, 11, 11],
            ]
            self.can_miror=True
            self.rotation = 4
            
        elif id ==12:
            self.piece = [
                [12,12,0],
                [0,12,12],
                [0,0,12]
            ]
            self.can_miror=False
            self.rotation = 4
    def __len__(self):
        """
        Returns the number of rows in the piece.

        Returns:
        - Integer: The number of rows in the piece.
        """
        return len(self.piece)
    def __getitem__(self, item):
        """
        Allows access to an element of the piece using subscript notation.

        Parameters:
        - item: The index of the element.

        Returns:
        - The element of the piece at the specified index.
        """
        return self.piece[item]
    
    def __eq__(self, __value: object) -> bool:
        for y in range(self):
            for x in range(self[y]):
                if x != y: return False
        return True
            
    def turnClockwise(self):
        """
        Rotates the piece clockwise.
        """
        self.piece = [list(reversed(col)) for col in zip(*self.piece)]

    def mirror(self):
        """
        Reverse the piece. 
        """
        for line in self.piece:
            line.reverse()





# table = plateau(5, 11)
# position = (2, 0)
# forme1 = piece(1)
# forme2 = piece(1)
# placer_piece(table, forme1, position)
# placer_piece(table, forme2, (0, 0))

# table.afficher_tableau_console()
