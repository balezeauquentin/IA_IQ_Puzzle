import jeu
import interface
import threading


# def find_isoalte_celle(table: jeu.Board):
#     for i in range(len(table.board)):
#         for j in range(len(table.board[0])):
#             if table.board[i][j]==0:
#                 if i==0 or table.board[i-1][j]!=0 and i==
#
def case_isolee(plateau, ligne, colonne):
    # Les coordonnées des cases voisines
    voisins = [(ligne - 1, colonne), (ligne + 1, colonne), (ligne, colonne - 1), (ligne, colonne + 1)]

    # Vérifie si **toutes** les cases voisines sont différentes de zéro
    for voisin_ligne, voisin_colonne in voisins:
        if (
                len(plateau) > voisin_ligne >= 0 == plateau[voisin_ligne][voisin_colonne] and  # Vérifie si les coordonnées sont dans les limites du plateau
                0 <= voisin_colonne < len(plateau[0])
        ):
            return False  # Il y a au moins une case vide à proximité, la case n'est pas isolée

    return True  # Toutes les cases voisines sont différentes de zéro, la case est isolée


def table_a_des_cases_isolees(plateau):
    return True


def brutforce(affichage: interface.Interface, used_pieces, table, position=(0, 0)):
    #affichage.draw()

    if 0 not in used_pieces:
        # Toutes les pièces ont été utilisées, nous avons une solution.
        print("Solution trouvée:")
        plateau_solution = jeu.Board(len(table), len(table[0]))
        plateau_solution.board = table
        plateau_solution.printBoard()

        return
    a = 0
    b = 0
    while a != len(table):
        if table[b][a] == 0 and case_isolee(table, b, a):
            return False
        b = b + 1
        if b == len(table):
            b = 0
            a = a + 1
    a = 0
    b = 0
    while b != position[0] or a != position[1]:
        if table[b][a] == 0:
            for idpiece in range(1, 13):
                for _ in range(2):
                    for _ in range(4):
                        if table.canPlaceShape(jeu.Piece(idpiece), (b, a)):
                            table.placeShape(jeu.Piece(idpiece), (b, a))
                            used_pieces[idpiece - 1] = 1
                            return True
                    jeu.Piece(idpiece).turnClockwise()
                jeu.Piece(idpiece).mirror()
            return False
        b = b + 1
        if b == len(table):
            b = 0
            a = a + 1

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

    if j == len(table[0]):
        # Toutes les cases ont été remplies, mais nous n'avons pas encore de solution.
        print("Pas de solution trouvée.")
        return

    temp_table = jeu.Board(len(table), len(table[0]))
    temp_table.board = [row[:] for row in table]
    for piece_id in range(1, 13):  # Mise à jour pour 12 pièces
        if used_pieces[piece_id - 1] == 0:
            current_piece = jeu.Piece(piece_id)  # Renomme la variable pour éviter le conflit de noms

            for _ in range(2):

                if piece_id == 7:
                    t = 2
                else:
                    t = 4
                for _ in range(t):
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
                        # threade=threading.Thread(target=brutforce,args=(affichage,updated_used_pieces,temp_table,next_position))
                        brutforce(affichage, updated_used_pieces, temp_table, next_position)
                        # threade.run()
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
    petitpeton=threading.Thread(target=brutforce,args=(a, used_pieces, b))
    petitpeton.daemon=True
    petitpeton.start()


    #brutforce(a, used_pieces, b)


if __name__ == "__main__":
    a = interface.Interface()
    brutforce(a, [0 for _ in range(12)], a.board)
