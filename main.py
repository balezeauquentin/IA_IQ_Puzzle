import interface
import pygame as pg

if __name__ == "__main__" :
    pg.init()
    inte = interface.Interface()
    #Limits max fps to 60
    pg.time.Clock().tick(60)
    while inte.isRunning:
        inte.update_events()
        inte.draw()


# pieces = [i for i in range(1,13)] # Liste des pièces de 1 à 12
# brutforce.brutforce(affichage, pieces, [0 for _ in range(12)])
