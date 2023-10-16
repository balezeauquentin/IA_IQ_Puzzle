import jeu

def brutforce(table, pieces, position=(0, 0), used_pieces=None):
    if 12 == len(used_pieces):
        # Toutes les pièces ont été utilisées, nous avons une solution.
        print("Solution trouvée:")
        plateau_solution = jeu.plateau(len(table), len(table[0]))
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

    for piece_id in range(1, 13):  # Mise à jour pour 12 pièces
        if piece_id not in used_pieces:
            current_piece = jeu.piece(piece_id)  # Renomme la variable pour éviter le conflit de noms
            for _ in range(4):
                if jeu.peut_placer_piece(table, current_piece.piece, (i, j)):
                    temp_table = [row[:] for row in table]
                    jeu.placer_piece(temp_table, current_piece, (i, j))
                    next_position = (i, j + 1)
                    if next_position[1] == len(table[0]):
                        next_position = (i + 1, 0)
                    updated_used_pieces = used_pieces + [piece_id]
                    brutforce(temp_table, pieces, next_position, updated_used_pieces)
                current_piece.piece = jeu.tourner_piece_horraire(current_piece)

table = jeu.plateau(5, 11)
pieces = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # Liste des pièces de 1 à 12

brutforce(table.plateau, pieces, used_pieces=[])