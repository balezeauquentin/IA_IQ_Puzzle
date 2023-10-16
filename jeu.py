# Création du plateau
hauteur = 5
largeur = 11
plateau = [[0 for _ in range(largeur)] for _ in range(hauteur)]

# Création d'une pièce (exemple avec une pièce en forme de L)
piece_L = [
    [1, 0],
    [1, 0],
    [1, 1]
]

piece_L2 = [
    [2, 0],
    [2, 0],
    [2, 0],
    [2, 2]
]

piece_L3 = [
    [3, 0],
    [3, 3],
]

piece_L4 = [
    [4, 0, 0],
    [4, 0, 0],
    [4, 4, 4]
]

piece_U = [
    [5, 5, 5],
    [5, 0, 0],
    [5, 5, 5]
]

piece_T = [
    [6, 6, 6],
    [0, 6, 0],
    [0, 6, 0]
]  

piece_Z = [
    [7, 7, 0],
    [0, 7, 7],
]

piece_TM = [
    [8, 8, 8, 8],
    [0, 8, 0, 0]
]

piece_truc = [
    [0,0,9],
    [9,9,9],
    [0,9,0]
]

piece_C = [
    [10, 0],
    [10, 10],
    [10, 10]
]

piece_Z2 = [
    [11, 11, 11, 0],
    [0, 0, 11, 11],
]
    

# Fonction pour placer une pièce sur le plateau
def placer_piece(plateau, piece, position):
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if piece[i][j] != 0:
                plateau[position[0] + i][position[1] + j] = piece[i][j]
# Fonction pour vérifier si une pièce peut être placée à un certain endroit
def peut_placer_piece(plateau, piece, position):
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if (
                position[0] + i < 0
                or position[1] + j < 0
                or position[0] + i >= len(plateau)
                or position[1] + j >= len(plateau[0])
                or (piece[i][j] == 1 and plateau[position[0] + i][position[1] + j] == 1)
            ):
                return False
    return True

def tourner_piece_horraire(piece):
    return [list(reversed(col)) for col in zip(*piece)]


# Fonction pour afficher le plateau
def afficher_plateau(plateau):
    for ligne in plateau:
        ligne_affichee = ""
        for case in ligne:
            if case == 0:
                ligne_affichee += " . "
            else:
                ligne_affichee += " " + chr(ord('A') + case - 1) + " "

        print(ligne_affichee)


piece_L = tourner_piece_horraire(piece_L)
placer_piece(plateau, piece_L, (1, 1))
afficher_plateau(plateau)