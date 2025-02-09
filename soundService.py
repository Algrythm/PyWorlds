from ursina import *
isPlaying = False
footstepAudio = Audio('./assets/footsteps.mp3',loop=True)
def footSteps(isMoving):
    if isMoving == True:
        if isPlaying == False:
            footstepAudio.play()
            isPlaying = True
    else:
        footstepAudio.stop()
        isPlaying = False