import interface
import brutforce


<<<<<<< Updated upstream
pieces = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # Liste des pièces de 1 à 12
affichage=interface.Interface()
brutforce.brutforce(affichage, [0 for _ in range(12)])
=======

table = jeu.Board(5, 11)
pieces = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # Liste des pièces de 1 à 12
affichage=interface.Interface()
brutforce.brutforce(affichage, pieces, [0 for _ in range(12)])
>>>>>>> Stashed changes
