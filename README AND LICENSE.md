## CREATED BY MARS CANNON (Algrythm) :D


## PyWorlds License

## Copyright (c) [2025] Algrythm

All rights reserved.

Redistributions are prohibited, whether commercially or non-commercially. For permission to redistribute, whether you have modified PyWorlds or not, contact Algrythm.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## DESCRIPTION:

This game is a voxel game in the Ursina Engine! It works by generating a world based off of your parameters specified using perlin noise, storing the block data in a list, and when it is within your render distance range, moving the blocks out of the list and into the world. All modifications to the world are saved in the *.json file exported by the game into the /worlds directory, and are able to be reloaded by entering the name of the world in the console. Your worlds will not work in newer or older versions of the game (ex. you make a world in version 0.0.1. it will not work in 0.0.2 or vice versa). This feature is a precaution to prevent errors. Updates may cause game-breaking modifications to world *.json files.


Music by Algrythm / Mars Cannon


## WARNING: At this time, you are not able to destroy blocks that are part of the world. You can not destroy your own previously placed blocks after a reload of a save, since they are considered part of the world. This may be changed in a future update.


## HOW TO PLAY:

Execute **dependencies.bat** to install all required Python packages.
Execute **Run.bat** to start the game (in the bin folder).


## 0.3 (Beautiful Worlds Update) Notes:

Complete overhaul of game assets.
Major bug fixes.
Improved world generation.
Improved tree generation.
More user-friendly menu navigation.
More world generation options.
Added more world decoration.
Renamed "placedBlockTreeData" key in exported world json files to "treeData" for accuracy.


## 0.3A (0.3 PATCH #1):

Removed unnecessary variables.
Code cleanup.


## Controls:

T - Open command-line
1,2,3 - Switch Block Texture
Esc - Exit game

## Commands:

/tp /setpos /teleport (X,Y,Z) 
Change X, Y, Z to your own coordinates.

/toSpawn
Sends you back to the world spawn point (0,0,0 or your custom set spawn point).

/seed
Get world seed.

/execute ()
Execute Python Code.

/setSpawn
Set Player Spawn Point.