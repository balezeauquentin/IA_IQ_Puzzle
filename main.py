import jeu
import interface
import brutforce



pieces = range(1, 13) # Liste des pièces de 1 à 12
affichage=interface.Interface()
brutforce.brutforce(affichage, pieces, [0 for _ in range(12)])
