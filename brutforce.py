import jeu
import interface


def brutforce(table: jeu.Plateau, pieces, used_pieces, position=(0, 0)):
    affichage = interface.Interface()
    if 0 not in used_pieces:
        # Toutes les pièces ont été utilisées, nous avons une solution.
        print("Solution trouvée:")
        plateau_solution = jeu.Plateau(len(table), len(table[0]))
        plateau_solution.plateau = table
        plateau_solution.afficher_tableau_console()
        return

    i, j = position

    while i < len(table):
        if table[i][j] != 0:
            # Cette case est déjà occupée, passons à la suivante.
            next_position = (i, j + 1)
            if next_position[1] == len(table[0]):
                next_position = (i + 1, 0)
            i, j = next_position
        else:
            break

    if i == len(table):
        # Toutes les cases ont été remplies, mais nous n'avons pas encore de solution.
        return
    temp_table = jeu.Plateau(len(table), len(table[0]))
    temp_table.plateau = [row[:] for row in table]
    for piece_id in range(1, 13):  # Mise à jour pour 12 pièces
        if used_pieces[piece_id - 1] == 0:
            current_piece = jeu.Piece(piece_id)  # Renomme la variable pour éviter le conflit de noms
            for _ in range(4):

                if jeu.peut_placer_piece(table, current_piece.piece, (i, j)):

                    jeu.placer_piece(temp_table, current_piece, (i, j))
                    next_position = (i, j + 1)
                    if next_position[1] == len(table[0]):
                        next_position = (i + 1, 0)
                    used_pieces[piece_id - 1] = 1
                    updated_used_pieces = used_pieces[:]

                    temp_table.afficher_tableau_console()
                    affichage.affichage_clase(temp_table)

                    brutforce(temp_table, pieces, updated_used_pieces, next_position)
                current_piece.tourner_piece_horraire()  # Renomme la fonction pour éviter le conflit de noms
