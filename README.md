# Alchemy-Adventure-Battle
A battle / elemental combo

# How to run
### Follow these steps to fully ensure your gaming experience is flawless
#### Windows
1. Download Python : https://www.python.org/downloads/,  make sure to install it to PATH
2. run "start.bat". (this installs pip, pygame, and numpy, then runs the game)
#### Linux
1. Open the terminal and type the following commands:  
   `python -m ensurepip`
   `pip install pygame`
   `pip install numpy`
   (These are basic python libraries)
2. Then navigate to the game (inside the client folder) and run "main.py"

# How to play
- WASD / Arrow keys : Movement
- Q : Drop an element
  - Shift+Q : Drop all elements
- E : Open / Close Crafting Menu
- Esc : Close Crafting Menu / Exit Game  
Walk around and collect elements from spawners! Draw pictures using the elements in the Crafting menu

# Recent Update (v0.4 Prerelease 18.10:23.30):
#### Minor (v04:P3)
- Resizable / Fullscreen window!
- `Shift+q` removes all elements from inventory
---
- popup menu when 2 or more elements are in crafting menu
- main character updated to use ElementalPlayer's sprite
- crafting menu (wip)
- reorganized functions
- `esc` closes crafting before exiting game
- `q` now removes 1 element at the end of the list.
- `e` opens the crafting menu
- mouse is set to invisible and immovable until crafting is opened
- removed unnecessary code

#### Major (v3)
- New images: background image (Me), spawners (Me), character (friend from school)
- Loading (terminal / prompt)
- Randomly generated spawners
- Background tiling and scrolling
- reorganization of functions
- limited area due to no spawners past a certain point

### Release (v0)
- ...

### Planned Features
##### v0.4
- ~~bigger inventory~~
- crafting (wip)
##### v0.5
- server connection
- basic player interaction
- card game battle DEMO
##### TBD
- music
- animation
- polish
