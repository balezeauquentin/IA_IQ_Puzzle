import jeu
import threading
import time

lock = threading.Lock()

def case_isolee(plateau, ligne, colonne):
    """
    Determine if a cell (specified by its line and column) is isolated in the grid 'plateau'.
    An isolated cell is defined as one that has no adjacent cells with a value of 0.
    
    Parameters:
    - plateau: A 2D list representing the grid.
    - ligne: The row index of the cell.
    - colonne: The column index of the cell.
    
    Returns:
    - Boolean: True if the cell is isolated, False otherwise.
    """
    voisins = [(ligne - 1, colonne), (ligne + 1, colonne), (ligne, colonne - 1), (ligne, colonne + 1)]
    for voisin_ligne, voisin_colonne in voisins:
        if len(plateau) > voisin_ligne >= 0 and 0 <= voisin_colonne < len(plateau[0]):
            if plateau[voisin_ligne][voisin_colonne] == 0:
                return False
    return True

def verife_case_isolee(table):
    """
    Check if any cell in a 2D list 'table' is isolated. 
    It utilizes the 'case_isolee' function to check each cell.
    
    Parameters:
    - table: A 2D list representing the grid.
    
    Returns:
    - Boolean: False if any cell is isolated, True otherwise.
    """
    for ligne in range(len(table)):
        for colone in range(len(table[0])):
            if table[ligne][colone] == 0:
                if case_isolee(table, ligne, colone):
                    return False
    return True

def avancer_case_vide(table, position):
    """
    Finds the next position in the 'table' starting from 'position' that contains a zero (empty cell).
    This function iteratively moves through the table until it finds an empty cell.

    Parameters:
    - table: A 2D list representing the grid.
    - position: A tuple (i, j) representing the starting position in the grid.

    Returns:
    - Tuple: The position (i, j) of the next empty cell in the table.
    """
    i, j = position
    while i < len(table):
        if table[i][j] != 0:
            next_position = (i + 1, j)
            if next_position[0] == len(table):
                next_position = (0, j + 1)
            i, j = next_position
        else:
            break
    return i,

def brutforcefct(affichage, used_pieces, table, position=(0, 0)):
    """
    Implements a brute force algorithm to solve a puzzle represented by 'table'.
    It tries placing different pieces on the table, checking for a complete solution.

    Parameters:
    - affichage: An object to manage the display of the board.
    - used_pieces: A list indicating which pieces have been used.
    - table: A 2D list representing the grid of the puzzle.
    - position: The starting position for trying to place a piece.

    Returns:
    - Boolean: True if a solution is found, False otherwise.
    """
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

def launch_brutforce(a):
    """
    Launches the brute force algorithm in a separate thread.
    This function sets up the puzzle board and the list of used pieces,
    then starts the brute force search in a new thread.

    Parameters:
    - a: An object representing the puzzle board.

    Notes:
    - The function also measures and prints the execution time of the algorithm.
    """
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