import jeu
import interface

# def find_isoalte_celle(table: jeu.Board):
#     for i in range(len(table.board)):
#         for j in range(len(table.board[0])):
#             if table.board[i][j]==0:
#                 if i==0 or table.board[i-1][j]!=0 and i==


def brutforce(affichage, used_pieces, position=(0, 0)):
    affichage.update()
    table = affichage.plateau
    if 0 not in used_pieces:
        # Toutes les pièces ont été utilisées, nous avons une solution.
        print("Solution trouvée:")
        plateau_solution = jeu.Board(len(table), len(table[0]))
        plateau_solution.board = table
        plateau_solution.printBoard()
        affichage.update()
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
    temp_table = jeu.Board(len(table), len(table[0]))
    temp_table.board = [row[:] for row in table]
    for piece_id in range(1, 13):  # Mise à jour pour 12 pièces
        if used_pieces[piece_id - 1] == 0:
            current_piece = jeu.Piece(piece_id)  # Renomme la variable pour éviter le conflit de noms
            for _ in range(4):

                if table.verifPlacePiece(current_piece.piece, (i, j)):

                    temp_table.placeShape(current_piece, (i, j))
                    next_position = (i, j + 1)
                    if next_position[1] == len(table[0]):
                        next_position = (i + 1, 0)
                    used_pieces[piece_id - 1] = 1
                    updated_used_pieces = used_pieces[:]

                    # temp_table.afficher_tableau_console()
                    affichage.plateau = temp_table
                    brutforce(affichage, updated_used_pieces, next_position)
                current_piece.turnPiece()  # Renomme la fonction pour éviter le conflit de noms

if __name__ == "__main__":
    a = interface.Interface()
    brutforce(a, [0 for _ in range(12)])
