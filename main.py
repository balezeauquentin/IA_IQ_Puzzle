import interface
import pygame as pg

if __name__ == "__main__" :
    pg.init()
    inte = interface.Interface()
    #Limits max fps to 60
    pg.time.Clock().tick(160)
    while inte.isRunning:
        inte.update_events()
        inte.draw()
