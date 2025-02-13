from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import json
from voxel import Block
from perlin_noise import PerlinNoise
validBlocks = []
autoPlacedBlocks = []
def initMap(TEX,MAP_SIZE,MAPDATA,CUR_GAME_VERSION,SHADER_TEMP,PERLIN_OCTAVE):
    preload = False
    if MAPDATA == None:
        mapFile = open('./data/mapData.json')
        mapData = json.load(mapFile)
    else:
        preload = True
        mapFile = open(MAPDATA)
        mapData = json.load(mapFile)
        if mapData['gameVersion']:
            if mapData["gameVersion"] != CUR_GAME_VERSION:
                return "Could not load"
    if mapData['perlinSeed'] == 0:
        seed = random.randint(0,9999999999999)
    else:
        seed = mapData['perlinSeed']
    sky = Sky()
    TREE_BLOCKS = []
    if preload == True:
        if "placedBlocks" in mapData:
            for item in list(mapData["placedBlocks"]):
                positionTemp = list(str(item.replace("Vec3","").replace("(","").replace(")","")).split(', '))
                position = Vec3(int(positionTemp[0]),int(positionTemp[1]),int(positionTemp[2]))
                newBlockPre = Block(position=position, texture=str(mapData["placedBlockData"][list(mapData["placedBlocks"]).index(item)]), scale=(1,1,1),shader=SHADER_TEMP)
                autoPlacedBlocks.append(newBlockPre.position)
                validBlocks.append(newBlockPre)
    TERRAIN = Entity(model=None,collider=None)
    for z in range(-10,-10+int(MAP_SIZE)):
        for x in range(-10,-10+int(MAP_SIZE)):
            if PERLIN_OCTAVE == None:
                noise = PerlinNoise(octaves=4,seed=seed)
            else:
                noise = PerlinNoise(octaves=PERLIN_OCTAVE,seed=seed)
            y = noise([x * .02,z * .02])
            y = math.floor(y * 7.5)
            if y < -4:
                newBlock = Block(position=(x,y,z), texture='./assets/water.png', scale=(1,1,1),shader=SHADER_TEMP)
                validBlocks.append(newBlock)
            if y == -4:
                newBlock = Block(position=(x,y,z), texture='./assets/water.png', scale=(1,1,1),shader=SHADER_TEMP)
                validBlocks.append(newBlock)
            elif y == -3:
                if random.randint(1,50) == 34:
                    newBlock = Block(position=(x,y,z), texture='./assets/Gold_ore.png', scale=(1,1,1),shader=SHADER_TEMP)
                    validBlocks.append(newBlock)
                else:
                    newBlock = Block(position=(x,y,z), texture='./assets/cobbler.png', scale=(1,1,1),shader=SHADER_TEMP)
                    validBlocks.append(newBlock)
            elif y == -2:
                newBlock = Block(position=(x,y,z), texture='./assets/dirt.png', scale=(1,1,1),shader=SHADER_TEMP)
                validBlocks.append(newBlock)
            elif y == -1:
                newBlock = Block(position=(x,y,z), texture='./assets/buildpiece.png', scale=(1,1,1),shader=SHADER_TEMP)
                validBlocks.append(newBlock)
            elif y == 2 or y == 1 or y == 0 or y == -1 or y == -2: # tree generation
                if mapData['perlinSeed'] == 0: # if world was NOT preloaded
                    newBlockOrig = Block(position=(x,y,z), texture=TEX, scale=(1,1,1),shader=SHADER_TEMP)
                    validBlocks.append(newBlockOrig)
                    if random.randint(1,35) == 7: # random number determines whether tree will be placed or not. this is not the most effective way, but it works.
                        TREE_BLOCKS.append(str(newBlockOrig.position))
                        newBlock = Block(position=(x,y+1,z), texture='./assets/log.jpg', scale=(1,1,1),shader=SHADER_TEMP)
                        validBlocks.append(newBlock)
                        newBlock = Block(position=(x,y+2,z), texture='./assets/log.jpg', scale=(1,1,1),shader=SHADER_TEMP)
                        validBlocks.append(newBlock)
                        newBlock = Block(position=(x,y+3,z), texture='./assets/log.jpg', scale=(1,1,1),shader=SHADER_TEMP)
                        validBlocks.append(newBlock)
                        newBlock = Block(position=(x,y+4,z), texture='./assets/leaves.jpg', scale=(1,1,1),shader=SHADER_TEMP)
                        validBlocks.append(newBlock)
                        newBlock = Block(position=(x+1,y+4,z), texture='./assets/leaves.jpg', scale=(1,1,1),shader=SHADER_TEMP)
                        validBlocks.append(newBlock)
                        newBlock = Block(position=(x-1,y+4,z), texture='./assets/leaves.jpg', scale=(1,1,1),shader=SHADER_TEMP)
                        validBlocks.append(newBlock)
                        newBlock = Block(position=(x,y+4,z+1), texture='./assets/leaves.jpg', scale=(1,1,1),shader=SHADER_TEMP)
                        validBlocks.append(newBlock)
                        newBlock = Block(position=(x,y+4,z-1), texture='./assets/leaves.jpg', scale=(1,1,1),shader=SHADER_TEMP)
                        validBlocks.append(newBlock)
                else: # if it was preloaded, load trees from json
                    newBlockPre = Block(position=(x,y,z), texture=TEX, scale=(1,1,1),shader=SHADER_TEMP)
                    validBlocks.append(newBlockPre)
                    for tree in mapData["treeData"]:
                        positionTemp2 = list(str(tree.replace("Vec3","").replace("(","").replace(")","")).split(', '))
                        position2 = Vec3(int(positionTemp2[0]),int(positionTemp2[1]),int(positionTemp2[2]))
                        if position2 == newBlockPre.position:
                            x = position2.x
                            y = position2.y
                            z = position2.z
                            newBlock = Block(position=(x,y+1,z), texture='./assets/log.jpg', scale=(1,1,1),shader=SHADER_TEMP)
                            validBlocks.append(newBlock)
                            newBlock = Block(position=(x,y+2,z), texture='./assets/log.jpg', scale=(1,1,1),shader=SHADER_TEMP)
                            validBlocks.append(newBlock)
                            newBlock = Block(position=(x,y+3,z), texture='./assets/log.jpg', scale=(1,1,1),shader=SHADER_TEMP)
                            validBlocks.append(newBlock)
                            newBlock = Block(position=(x,y+4,z), texture='./assets/leaves.jpg', scale=(1,1,1),shader=SHADER_TEMP)
                            validBlocks.append(newBlock)
                            newBlock = Block(position=(x+1,y+4,z), texture='./assets/leaves.jpg', scale=(1,1,1),shader=SHADER_TEMP)
                            validBlocks.append(newBlock)
                            newBlock = Block(position=(x-1,y+4,z), texture='./assets/leaves.jpg', scale=(1,1,1),shader=SHADER_TEMP)
                            validBlocks.append(newBlock)
                            newBlock = Block(position=(x,y+4,z+1), texture='./assets/leaves.jpg', scale=(1,1,1),shader=SHADER_TEMP)
                            validBlocks.append(newBlock)
                            newBlock = Block(position=(x,y+4,z-1), texture='./assets/leaves.jpg', scale=(1,1,1),shader=SHADER_TEMP)
                            validBlocks.append(newBlock)
                            TREE_BLOCKS.append(str(Vec3(x,y,z)))
            else:
                newBlock = Block(position=(x,y,z), texture=TEX, scale=(1,1,1),shader=SHADER_TEMP)
                validBlocks.append(newBlock)
    TERRAIN.collider = 'mesh'
    return TERRAIN,seed,mapData['perlinOctave'],mapData['mapSize'],mapData['renderDistance'],TREE_BLOCKS,mapData['treeData'],mapData['placedBlockData'],mapData['playerSpawnLocation']
def getValidBlocks():
    return validBlocks
def getPreLoadedBlocks():
    return autoPlacedBlocks
