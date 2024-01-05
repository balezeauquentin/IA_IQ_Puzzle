import jeu
import interface
import threading
import time

lock = threading.Lock()


def case_isolee(plateau, ligne, colonne):
    # Les coordonnées des cases voisines
    voisins = [(ligne - 1, colonne), (ligne + 1, colonne), (ligne, colonne - 1), (ligne, colonne + 1)]

    # Vérifie si **toutes** les cases voisines sont différentes de zéro
    for voisin_ligne, voisin_colonne in voisins:

        if len(plateau) > voisin_ligne >= 0 and 0 <= voisin_colonne < len(plateau[0]):
            if plateau[voisin_ligne][voisin_colonne] == 0:
                return False
            # Il y a au moins une case vide à proximité, la case n'est pas isolée

    return True  # Toutes les cases voisines sont différentes de zéro, la case est isolée


def verife_case_isolee(table):
    for ligne in range(len(table)):
        for colone in range(len(table[0])):
            if table[ligne][colone] == 0:
                if case_isolee(table, ligne, colone):
                    return False
    return True


def avancer_case_vide(table, position):
    i, j = position
    while i < len(table):
        if table[i][j] != 0:
            # Cette case est déjà occupée, passons à la suivante.
            next_position = (i + 1, j)
            if next_position[0] == len(table):
                next_position = (0, j + 1)
            i, j = next_position
        else:
            break
    return i, j


def brutforcefct(affichage: interface.Interface, used_pieces, table, position=(0, 0)):
    # quand une solution est trouver
    if 0 not in used_pieces:
        # Toutes les pièces ont été utilisées, nous avons une solution.
        print("Solution trouvée:")
        plateau_solution = jeu.Board(len(table), len(table[0]))
        plateau_solution.board = table
        plateau_solution.printBoard()
        return True

    # on verifie si il y a pas une case isolé presente sur le tableau
    if not verife_case_isolee(table):
        return False
    # avance de la position jusqu'a la prochaine case vide
    i, j = avancer_case_vide(table, position)
    # placement des piece


    temp_table = jeu.Board(len(table), len(table[0]))
    temp_table.board = [row[:] for row in table]
    for piece_id in range(1, 13):  # Mise à jour pour 12 pièces
        if used_pieces[piece_id - 1] == 0:
            current_piece = jeu.Piece(piece_id)  # Renomme la variable pour éviter le conflit de noms
            for _ in range(2):
                for _ in range(current_piece.rotation):
                    position = i, j
                    m = 0
                    while current_piece[m][0] == 0:
                        m = m + 1
                    position = position[0] - m, position[1]

                    if table.canPlaceShape(current_piece, position):

                        temp_table.placeShape(current_piece, position)
                        next_position = (i + 1, j)
                        if next_position[0] == len(table):
                            next_position = (0, j + 1)
                        updated_used_pieces = used_pieces[:]
                        updated_used_pieces[piece_id - 1] = 1
                        affichage.board.board = temp_table.board
                        t = threading.Thread(target=brutforcefct,
                                             args=(affichage, updated_used_pieces, temp_table, next_position))
                        t.start()
                        t.join()
                        affichage.remove_shape(piece_id)
                        used_pieces[piece_id - 1] = 0
                        temp_table.board = [row[:] for row in table]
                    current_piece.turnClockwise()
                if current_piece.can_miror:
                    current_piece.mirror()
                else:
                    break


def launch_brutforce(a: interface.Interface):
    b = a.board
    used_pieces = [0 for _ in range(12)]
    for ligne in b:
        for val in ligne:
            if val != 0:
                used_pieces[val - 1] = 1
    thread_brute_force = threading.Thread(target=brutforcefct, args=(a, used_pieces, b))
    thread_brute_force.daemon = True
    start = time.time()
    # print the difference between start 
    # and end time in milli. secs
    thread_brute_force.start()
    # record end time
    end = time.time()
    print("The time of execution of above program is :", (end - start) * 10 ** 3, "ms")
    print("fin de recherche")


if __name__ == "__main__":
    a = interface.Interface()
    brutforcefct(a, [0 for _ in range(12)], a.board)
