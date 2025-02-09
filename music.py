from ursina import *
from mutagen.mp3 import MP3
from random import choice
musicSongs = ['./assets/jazz.mp3']
from time import sleep
def startMusic():
    chosenSong = choice(musicSongs)
    Audio(chosenSong,autoplay=True,loop=True)