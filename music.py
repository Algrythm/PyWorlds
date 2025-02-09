from ursina import *
from random import choice
musicSongs = ['./assets/jazz.mp3']
from time import sleep
def startMusic():
    chosenSong = choice(musicSongs)
    Audio(chosenSong,autoplay=True,loop=True)
