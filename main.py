from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import mapTools
import music
import os
import atexit
import json
import click
import logging
from ursina.shaders import lit_with_shadows_shader
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
logging.basicConfig(level=logging.ERROR)
os.system('cls')
action = inquirer.select(
        message="Welcome to PyWorlds",
        choices=[
            "Play",
            "Exit"
        ],
        default="Play",
    ).execute()
if action == "Exit":
    exit()
action2 = inquirer.select(
        message="Choose a map size",
        choices=[
            "Very Small",
            "Small",
            "Medium",
            "Large",
            "Very Large",
            "Extremely Large (not recommended)"
        ],
        default="Medium",
    )
action3 = inquirer.select(
        message="Choose a map type",
        choices=[
            "Normal",
            "Amplified (not recommended)"
        ],
        default="Normal",
    )
action4 = inquirer.select(
        message="Would you like to enable shaders?",
        choices=[
            "Yes",
            "No"
        ],
        default="No",
    )
os.system('cls')
if action == "Play":
    while True:
        mapData = "./worlds/" + click.prompt("Enter your world name", type=str, default="New World") + ".json"
        if mapData == "./worlds/READ.txt.json":
            print("PyWorlds.Error.114: Invalid World Name")
        else:
            break
LOADED_BLOCKS = []
RANGE_OUT = []
BLOCKS_PLACED = []
BLOCKS_PLACED2 = []
UNLOADED_BLOCKS = []
UNLOADED_BLOCKS_TEX = []
REMOVED_MAP_BLOCKS = []
HEALTH = 100
CUR_GAME_VERSION = "0.3.0"
WORLD_PERLIN = None
if os.path.isfile(mapData):
    oneMapFile = open(mapData)
    oneMapData = json.load(oneMapFile)
    RENDER_DISTANCE = oneMapData['renderDistance']
    MAP_SIZE = oneMapData['mapSize']
else:
    RENDER_DISTANCE = click.prompt("Enter a render distance (10 recommended for highest performance on low end devices, 15-30 on high end devices)", type=int, default=10)
    os.system('cls')
    result1 = action2.execute()
    if result1 == "Very Small":
        MAP_SIZE = 5
    elif result1 == "Small":
        MAP_SIZE = 10
    elif result1 == "Medium":
        MAP_SIZE = 20
    elif result1 == "Large":
        MAP_SIZE = 35
    elif result1 == "Very Large":
        MAP_SIZE = 50
    elif result1 == "Extremely Large (not recommended)":
        MAP_SIZE = 105
    os.system("cls")
    result2 = action3.execute()
    if result2 == "Amplified (not recommended)":
        WORLD_PERLIN = 7
    else:
        WORLD_PERLIN = 4
os.system('cls')
if action4.execute() == "Yes":
    SHADOWS = True
else:
    SHADOWS = False
os.system('cls')
otherClientPos = None
otherClientBlocks = []
isMoving = False
window.borderless = False
window.title = "PyWorlds"
playerSpawn = Vec3(0,0,0)
app = Ursina(development_mode=False)
scene.fog_density = 0.05
scene.fog_color = color.white
class Block(Entity):
    def __init__(self, position=(0, 0, 0), texture='', scale=1,shader=lit_with_shadows_shader):
        super().__init__(
            position=position,
            parent=scene,
            model='cube',
            origin_y=.5,
            texture=texture,
            scale=scale,
            collider='box',
            cull_face=True,
            shader=shader
        )
chat_input = InputField(placeholder='Type here...', multiline=False)
chat_input.enabled = False
def on_enter():
    global playerSpawn
    if chat_input.text:
        if chat_input.text == "/toSpawn":
            player.enabled = True
            player.position = playerSpawn
        if "/setSpawn" in chat_input.text:
            if chat_input.text == "/setSpawn":
                playerSpawn = player.position
            else:
                listOfChars = []
                for char in chat_input.text.partition("(")[2].partition(")")[0].split(","):
                    listOfChars.append(char)
                if listOfChars[0] == "~":
                    listOfChars[0] = player.position.x
                if listOfChars[1] == "~":
                    listOfChars[1] = player.position.y
                if listOfChars[2] == "~":
                    listOfChars[2] = player.position.z
                try:
                    playerSpawn = Vec3(int(listOfChars[0]),int(listOfChars[1]),int(listOfChars[2]))
                except:
                    print("Error")
        if "/tp " in chat_input.text or "/setpos" in chat_input.text or "/teleport" in chat_input.text:
            listOfChars = []
            for char in chat_input.text.partition("(")[2].partition(")")[0].split(","):
                listOfChars.append(char)
            if listOfChars[0] == "~":
                listOfChars[0] = player.position.x
            if listOfChars[1] == "~":
                listOfChars[1] = player.position.y
            if listOfChars[2] == "~":
                listOfChars[2] = player.position.z
            try:
                player.position = Vec3(int(listOfChars[0]),int(listOfChars[1]),int(listOfChars[2]))
            except:
                print("Error")
        if "/execute (" in chat_input.text:
            try:
                print(eval(chat_input.text.partition("(")[2].partition(")")[0]))
            except:
                print(f"Error in executing '{chat_input.text.partition('(')[2].partition(')')[0]}'.")
        if chat_input.text == "/seed":
            print("World seed is " + str(initMap[1]))
        
        

        chat_input.text = ''
        chat_input.enabled = False
        player.enabled = True

# Set the on_key_down and on_enter functions
chat_input.on_submit = on_enter
if SHADOWS == True:
    SHADER_TEMP = lit_with_shadows_shader
    pivot = Entity()
    DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 45))
else:
    SHADER_TEMP = None
current_game_version = Text(CUR_GAME_VERSION,scale=1,x=-.1,y=.47)
player = FirstPersonController()

if os.path.isfile(mapData):
    initMap = mapTools.initMap('./assets/buildpiece.PNG',MAP_SIZE,mapData,CUR_GAME_VERSION,SHADER_TEMP,PERLIN_OCTAVE=None)
else:
    initMap = mapTools.initMap('./assets/buildpiece.PNG',MAP_SIZE,None,CUR_GAME_VERSION,SHADER_TEMP,PERLIN_OCTAVE=WORLD_PERLIN)
if initMap == "Could not load":
    os.system('cls')
    print("PyWorlds.Error.144: World was made in different game version. This world is not compatible with version " + CUR_GAME_VERSION + ".")
    print("This means that this world is unusable if you do not have access to the version this world was created on. Consider removing the file from /worlds.")
    print("If absolutely necessary, you can change the game version specified in the json file for the world to the current game version, but this is not recommended. This can cause errors, corrupt your world file, or crash the game. Only use this as a last resort.")
    exit()
if initMap[8]:
    playerSpawn = eval(initMap[8])
def saveMap():
    global BLOCKS_PLACED
    global BLOCKS_PLACED2
    for item in mapTools.getPreLoadedBlocks():
        BLOCKS_PLACED.append(item)
    nameMap = mapData
    exportedJson = open(nameMap,'w')
    exportedJsonContents = "{"
    exportedJsonContents = exportedJsonContents + '\n  "renderDistance": ' + str(RENDER_DISTANCE) + ',\n'
    exportedJsonContents = exportedJsonContents + '\n  "mapSize": ' + str(MAP_SIZE) + ',\n'
    exportedJsonContents = exportedJsonContents + '\n  "perlinOctave": ' + str(initMap[2]) + ',\n'
    exportedJsonContents = exportedJsonContents + '\n  "perlinSeed": ' + str(initMap[1]) + ',\n'
    if len(BLOCKS_PLACED) > 0:
        exportedJsonContents = exportedJsonContents + '\n  "placedBlocks": ['
        for placedBlock in BLOCKS_PLACED:
            if BLOCKS_PLACED.index(placedBlock) == 0:
                exportedJsonContents = exportedJsonContents + '"' + str(placedBlock) + '"'
            else:
                exportedJsonContents = exportedJsonContents + ',"' + str(placedBlock) + '"'
        exportedJsonContents = exportedJsonContents + "],\n"
    else:
        exportedJsonContents = exportedJsonContents + '\n  "placedBlocks": [],\n'
    if len(BLOCKS_PLACED2) > 0:
        exportedJsonContents = exportedJsonContents + '\n  "placedBlockData": ['
        BLOCKS_PLACED2 = BLOCKS_PLACED2 + list(initMap[7])
        for placedBlock in BLOCKS_PLACED2:
            if BLOCKS_PLACED2.index(placedBlock) == 0:
                exportedJsonContents = exportedJsonContents + '"' + str(placedBlock) + '"'
            else:
                exportedJsonContents = exportedJsonContents + ',"' + str(placedBlock) + '"'
        exportedJsonContents = exportedJsonContents + "],\n"
    else:
        exportedJsonContents = exportedJsonContents + '\n  "placedBlockData": ['
        for placedBlock in range(0,len(list(initMap[7]))):
            if placedBlock == 0:
                exportedJsonContents = exportedJsonContents + '"' + str(list(initMap[7])[placedBlock]) + '"'
            else:
                exportedJsonContents = exportedJsonContents + ',"' + str(list(initMap[7])[placedBlock]) + '"'
        exportedJsonContents = exportedJsonContents + "],\n"
    if len(initMap[5]) > 0:
        exportedJsonContents = exportedJsonContents + '\n  "treeData": ['
        for placedBlock in list(initMap[5]):
            if list(initMap[5]).index(placedBlock) == 0:
                exportedJsonContents = exportedJsonContents + '"' + str(placedBlock) + '"'
            else:
                exportedJsonContents = exportedJsonContents + ',"' + str(placedBlock) + '"'
        exportedJsonContents = exportedJsonContents + "],\n"
    else:
        if len(list(initMap[6])) > 0:
            exportedJsonContents = exportedJsonContents + '\n  "treeData": ['
            for placedBlock in list(initMap[6]):
                if list(initMap[6]).index(placedBlock) == 0:
                    exportedJsonContents = exportedJsonContents + '"' + str(placedBlock) + '"'
                else:
                    exportedJsonContents = exportedJsonContents + ',"' + str(placedBlock) + '"'
            exportedJsonContents = exportedJsonContents + "],\n"
    exportedJsonContents = exportedJsonContents + f'\n  "gameVersion": "{CUR_GAME_VERSION}",\n'
    exportedJsonContents = exportedJsonContents + f'\n  "playerSpawnLocation": "{playerSpawn}"\n'
    exportedJsonContents = exportedJsonContents + '}'
    exportedJson.writelines(exportedJsonContents)
    exportedJson.close()
music.startMusic()
VALID_BLOCKS = []
VALID_BLOCKS = VALID_BLOCKS + mapTools.getValidBlocks()
selected_block = 'stone'
def input(key):
    global selected_block
    global isMoving
    global selected_texture
    if key == 't':
        if chat_input.enabled == True:
            print("Already in chat")
        else:
            chat_input.text = ""
            chat_input.enabled = not chat_input.enabled
            player.enabled = False
    if key == "enter":
        if chat_input.enabled == True:
            on_enter()
    if key == "escape":
        exit()
    if key == "1":
        selected_block = 'stone'
    if key == "2":
        selected_block = 'grass'
    if key == "3":
        selected_block = 'wood'
    if selected_block == 'grass':
        selected_texture = './assets/buildpiece.PNG'
    elif selected_block == 'wood':
        selected_texture = './assets/plank.png'
    elif selected_block == 'stone':
        selected_texture = './assets/cobbler.png'
    if key == 'right mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=10)
        if hit_info.hit:
            if mouse.hovered_entity:
                if mouse.hovered_entity.texture != './assets/water.png':
                    placedBlock = Block(position=hit_info.entity.position + hit_info.normal,texture=selected_texture,shader=SHADER_TEMP)
                    Audio('./assets/new.wav')
                    BLOCKS_PLACED.append(placedBlock.position)
                    BLOCKS_PLACED2.append(placedBlock.texture)
                    VALID_BLOCKS.append(placedBlock)
            else:
                placedBlock = Block(position=hit_info.entity.position + hit_info.normal,texture=selected_texture,shader=SHADER_TEMP)
                Audio('./assets/new.wav')
                BLOCKS_PLACED.append(placedBlock.position)
                BLOCKS_PLACED2.append(placedBlock.texture)
                VALID_BLOCKS.append(placedBlock)
    if key == 'left mouse down' and mouse.hovered_entity:
        if mouse.hovered_entity.position in BLOCKS_PLACED:
            BLOCKS_PLACED2.remove(mouse.hovered_entity.texture)
            BLOCKS_PLACED.remove(mouse.hovered_entity.position)
            VALID_BLOCKS.remove(mouse.hovered_entity)
            destroy(mouse.hovered_entity)
            Audio('./assets/new.wav')
        else:
            print("PyWorlds.Error.142: Block cannot be deleted from save.")
def update():
    for block in VALID_BLOCKS:
        if len(VALID_BLOCKS) > 0:
            if block:
                if distance(player.position,block.position) > RENDER_DISTANCE:
                    UNLOADED_BLOCKS.append(block.position)
                    UNLOADED_BLOCKS_TEX.append(block.texture)
                    destroy(block)
    for block in UNLOADED_BLOCKS:
        if block != None:
            if distance(player.position,block) < RENDER_DISTANCE:
                newBlock = Block(position=block,texture=UNLOADED_BLOCKS_TEX[UNLOADED_BLOCKS.index(block)],shader=SHADER_TEMP)
                UNLOADED_BLOCKS_TEX.remove(UNLOADED_BLOCKS_TEX[UNLOADED_BLOCKS.index(block)])
                UNLOADED_BLOCKS.remove(block)
                VALID_BLOCKS.append(newBlock)
atexit.register(saveMap)
app.run()