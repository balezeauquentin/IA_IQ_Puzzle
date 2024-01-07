import jeu
import interface
import threading
import time

lock = threading.Lock()

## @brief This function checks if a cell is isolated
# @param plateau The game board
# @param ligne The row of the cell
# @param colonne The column of the cell
# @return True if the cell is isolated, False otherwise
def case_isolee(plateau, ligne, colonne):
    voisins = [(ligne - 1, colonne), (ligne + 1, colonne), (ligne, colonne - 1), (ligne, colonne + 1)]
    for voisin_ligne, voisin_colonne in voisins:
        if len(plateau) > voisin_ligne >= 0 and 0 <= voisin_colonne < len(plateau[0]):
            if plateau[voisin_ligne][voisin_colonne] == 0:
                return False
    return True

## @brief This function checks if there is an isolated cell in the board
# @param table The game board
# @return True if there is no isolated cell, False otherwise
def verife_case_isolee(table):
    for ligne in range(len(table)):
        for colone in range(len(table[0])):
            if table[ligne][colone] == 0:
                if case_isolee(table, ligne, colone):
                    return False
    return True

## @brief This function advances to the next empty cell
# @param table The game board
# @param position The current position
# @return The position of the next empty cell
def avancer_case_vide(table, position):
    i, j = position
    while i < len(table):
        if table[i][j] != 0:
            next_position = (i + 1, j)
            if next_position[0] == len(table):
                next_position = (0, j + 1)
            i, j = next_position
        else:
            break
    return i, j

## @brief This function finds a solution to the game using brute force
# @param affichage The game interface
# @param used_pieces The list of used pieces
# @param table The game board
# @param position The current position
# @return True if a solution is found, False otherwise
def brutforcefct(affichage: interface.Interface, used_pieces, table, position=(0, 0)):
    if 0 not in used_pieces:
        print("Solution trouvée:")
        plateau_solution = jeu.Board(len(table), len(table[0]))
        plateau_solution.board = table
        plateau_solution.printBoard()
        return True
    if not verife_case_isolee(table):
        return False
    i, j = avancer_case_vide(table, position)
    temp_table = jeu.Board(len(table), len(table[0]))
    temp_table.board = [row[:] for row in table]
    for piece_id in range(1, 13):
        if used_pieces[piece_id - 1] == 0:
            current_piece = jeu.Piece(piece_id)
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

## @brief This function launches the brute force algorithm
# @param a The game interface
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
    thread_brute_force.start()
    end = time.time()
    print("The time of execution of above program is :", (end - start) * 10 ** 3, "ms")
    print("fin de recherche")

if __name__ == "__main__":
    a = interface.Interface()
    brutforcefct(a, [0 for _ in range(12)], a.board)