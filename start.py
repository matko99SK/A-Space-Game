from ursina import *
import time
import game
import sys
import vlc

app = Ursina()
def menu():
    play = Button('Play', position = (0,0), color = 'red', collider = 'box')
    play.on_click = game.game_start()
menu()

app.run()