import pygame
from pygame.locals import *
import os
import sys
import numpy as np
import random
import math
# import copy

# import socket, pickle

# INITIALIZE #
pygame.init()
pygame.font.init()

# LOAD #
color = {"white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "magenta": (255, 0, 255),
    "cyan": (0, 255, 255),
    "gray": (128, 128, 128),
    "darkgray": (64, 64, 64),
    "lightgray": (192, 192, 192),
}

# WINDOW CLASS #
class WindowClass:
    def __init__(self, size=(1366, 768), title="Window", icon=None, color=color["white"]):
        # size of the window
        self.size = size
        # set title
        self.title = pygame.display.set_caption(title)
        # title icon
        if icon:
            self.icon = pygame.display.set_icon(pygame.image.load(icon))
        # width and height specification
        self.width, self.height = size
        # set the screen size
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        # main window color
        self.color = color
        # center of window
        self.center = (self.width/2, self.height/2)
        # list of all things on screen, excluding inventory items
        self.spriteList = []
        # list of all text on screen
        self.fontList = []
        # list of all inventory items on screen
        self.guiList = []
        # fullscreen flag
        self.fullscreen = False

# Must be called "Window"
Window = WindowClass((1920 / 2, 1080 / 2), "Alchemy: to the Death!", "elements.png")

# position of top right corner of screen
screenX = 0
screenY = 0

# SPRITES EXCLUDING RESOURCES #
class LoadSprite:
    def __init__(self, image, size, x, y, type="sprite", name="test", lID=0, render=True):
        # if image is already defined, image is image
        # else, image is pygame
        try:
            self.image = pygame.image.load(image).convert_alpha()
        except: self.image = image
        # size of sprite
        self.size = size
        # width and height of sprite
        self.width, self.height = size
        # set shape of sprite
        self.shape = pygame.transform.scale(self.image, self.size)
        # name of sprite
        self.name = name
        # set rect of sprite
        self.rect = self.shape.get_rect()
        # type of sprite
        self.type = type
        # quick render flag
        self.render = True
        ### TYPES
        # character (Main character)
        if type == "character":
            # center of character
            self.rect.center = (x, y)
            # first frame x and y of character
            self.x, self.y = self.rect.center
            # directional speed
            self.speed = [0, 0]
            # how fast a character can move forward and backward
            self.movement = [-4, 4]
            # which direction is currently in motion
            self.movementFlags = [0, 0, 0, 0]
            # allow movement flag
            self.allowMovement = True
            # inventory
            self.items = []
            Window.spriteList.append(self)
        elif type == "gui" or type == "topGui":
            # center of gui
            self.rect.center = (x, y)
            # first frame x and y of gui
            self.x, self.y = self.rect.center
            # list of items within gui
            self.items = []
            self.render = render
            Window.spriteList.append(self)
        elif type == "textbox":
            # x and y are absolute
            self.x = Window.width - self.width
            self.y = Window.height - self.height
            self.rect.center = (self.x, self.y)
            # open flag
            self.open = False
            # e key is pressed flag
            self.eKey = False
            Window.spriteList.append(self)
        elif type == "topGuiElement" or type == "combo":
            # render flag set to false
            self.render = False
            # id for displaying
            self.id = lID
            # center
            self.rect.center = (x, y)
            self.x, self.y = self.rect.center
            # grabbable if crafting menu open
            self.clickable = False
            # check if drag
            self.draging = False
            # offsets
            self.offsetX = 0
            self.offsetY = 0
            Window.guiList.append(self)
        else:
            self.rect.center = (x, y)
            self.x, self.y = self.rect.center
            Window.spriteList.append(self)

# try:
#     # Create a TCP/IP socket
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 
#     # Connect the socket to the port where the server is listening
#     server_address = ('localhost', 8080)
#     print('connecting to {} port {}'.format(*server_address))
#     sock.connect(server_address)
# finally:
#     print('closing socket')
#     sock.close()

# MAIN CHARACTER MUST BE MAIN
Main = LoadSprite("Main.png", (64, 64), Window.width/2, Window.height/2, "character", "Player")
# MAIN GUI MUST BE GUI
Gui = LoadSprite("hotbar.png", (Window.width - 64, 64), Window.width / 2, Window.height - 32, "topGui", "hotbar")
Crafting = LoadSprite("inventory.png", (Window.width / 4, Window.height / 4), Window.width / 2, Window.height / 2, "gui", "inventory", render=False)
Crafting.bottomX = Window.width / 2 + Window.width / 8
Crafting.bottomY = Window.height / 2 + Window.height / 8

CraftingCombo = LoadSprite("combo.png", (Window.width / 8, Window.width / 8), Window.width / 5 * 4, Window.height / 2, "gui", "CraftingCombo", render=False)
# textbox = LoadSprite("Textbox.png", (512, 320), "textbox", "textbox")

resourceId = 0
gEvent = ""

# BACKGROUND #
class LoadBackground:
    def __init__(self, image, size, name="test"):
        # image
        self.image = pygame.image.load(image).convert_alpha()
        # size
        self.size = size

        # width / height
        self.width, self.height = self.size
        # display shape
        self.shape = pygame.transform.scale(self.image, self.size)
        # display rect
        self.rect = self.shape.get_rect()
        # center
        self.rect.center = (self.width / (self.width / 2), self.height / (self.height / 2))
        # name
        self.name = name
        # type
        self.type = "background"
        # render flag
        self.render = True
        # set to display
        Window.spriteList.append(self)

    # tile background
    def tile_background(self):
        index = -1
        nextwidth, nextheight = Window.screen.get_size()
        if nextwidth != Window.width or nextheight != Window.height:
            Window.width = nextwidth
            Window.height = nextheight

            Gui.size = (Window.width - 64, 64)
            Gui.shape = pygame.transform.scale(Gui.image, Gui.size)
            Gui.rect = Gui.shape.get_rect()
            Gui.rect.center = (Window.width / 2, Window.height - 32)

            Main.rect.center = (Window.width / 2, Window.height / 2)
            Main.x, Main.y = Main.rect.center

            Game.redraw_elements()

            Crafting.size = (Window.width / 4, Window.height / 4)
            Crafting.shape = pygame.transform.scale(Crafting.image, Crafting.size)
            Crafting.rect = Crafting.shape.get_rect()
            Crafting.rect.center = (Window.width / 2, Window.height / 2)
            Crafting.bottomX = Window.width / 2 + Window.width / 8
            Crafting.bottomY = Window.height / 2 + Window.height / 8

            try: Crafting.Font.placement = (Window.width / 2 - Window.width / 11, Window.height / 2 - Window.height / 12)
            except: pass

            CraftingCombo.size = (Window.width / 8, Window.width / 8)
            CraftingCombo.shape = pygame.transform.scale(CraftingCombo.image, CraftingCombo.size)
            CraftingCombo.rect = CraftingCombo.shape.get_rect()
            CraftingCombo.rect.center = (Window.width / 5 * 4, Window.height / 2)
        # for every x value a background is able to fill + 2
        for i in range(math.ceil(Window.width / self.width) + 2):
            # for every y value a background is able to fill + 2
            for j in range(math.ceil(Window.height / self.height) + 2):
                # blit to the screen
                Window.screen.blit(self.shape, self.rect)
                # set new center (the middle of the background * x/y value * 2 + screen offset)
                self.rect.center = ((self.width / 2) * (i * 2) + (screenX % self.width) - self.width, (self.height / 2) * (j * 2) + (screenY % self.height) - self.height)

# BACKGROUND, multiple backgrounds can exist
Background = LoadBackground("background.png", (128, 128), "mainBg")

class LoadFont:
    def __init__(self, location, size, text, color, placement, aaFlag=True, boldFlag=False, italicFlag=False):
        # file location
        self.location = location
        # font size
        self.size = size
        # placement on the screen
        self.placement = placement
        # font text
        self.text = text
        # font color
        self.color = color
        # font display
        self.font = pygame.font.Font(self.location, self.size)
        # render
        self.render = True
        # font image
        self.image = self.font.render(self.text, aaFlag, self.color)
        # font rect
        self.rect = pygame.draw.rect(self.image, self.color, self.image.get_rect(), -1)
        # bold flag
        self.font.bold = boldFlag
        # italic flag
        self.font.italic = italicFlag
        Window.fontList.append(self)

class LoadResource:
    def __init__(self, image, size, x, y, type="element", name="test", pID=0, check=0, attack=0, defense=0):
        global resourceId
        self.size = size
        self.width, self.height = size
        self.name = name
        self.type = type
        self.render = True
        if type == "spawner":
            self.image = pygame.image.load(image).convert_alpha()
            self.shape = pygame.transform.scale(self.image, self.size)
            self.rect = self.shape.get_rect()

            self.rect.center = (x, y)
            self.x, self.y = self.rect.center
            self.resProd = 0
            self.timer = 0
            self.children = []
            self.id = resourceId
            resourceId += 1
            Window.spriteList.append(self)
        elif type == "element":
            if check:
                self.image = image
            else:
                self.image = pygame.image.load(image).convert_alpha()
            self.shape = pygame.transform.scale(self.image, self.size)
            self.rect = self.shape.get_rect()
            self.render = False
            
            self.rect.center = (x, y)
            self.x, self.y = self.rect.center
            self.attack = attack
            self.defense = defense
            self.parentId = pID

class GameClass:
    def __init__(self):
        # run while
        self.running = True
        # check fps
        self.prevFps = 0
        # fps
        self.fps = 0
        # random number for seed
        self.generation_number = 0
        # chunks
        self.chunkX, self.chunkY = (2048, 2048)
        # stored elements
        self.elements = {
            "Air": {
                "name": "Air",
                "recipe": [],
                "image": "air.png"
            },
            "Earth": {
                "name": "Earth",
                "recipe": [],
                "image": "earth.png"
            },
            "Fire": {
                "name": "Fire",
                "recipe": [],
                "image": "fire.png"
            },
            "Water": {
                "name": "Water",
                "recipe": [],
                "image": "water.png"
            },
        }
    
    def run(self):
        global screenX, screenY

        random.seed(random.randint(0, 65535))
        # TODO: get seed from server

        print("Loading: 0%")
        self.generate_spawners(0, 0)
        print("Loading: 11%")
        self.generate_spawners(0, self.chunkY)
        print("Loading: 22%")
        self.generate_spawners(-self.chunkX, self.chunkY * 2)
        print("Loading: 33%")
        self.generate_spawners(self.chunkX, 0)
        print("Loading: 44%")
        self.generate_spawners(self.chunkX, self.chunkY)
        print("Loading: 55%")
        self.generate_spawners(self.chunkX, self.chunkY * 2)
        print("Loading: 66%")
        self.generate_spawners(self.chunkX * 2, -self.chunkY)
        print("Loading: 77%")
        self.generate_spawners(self.chunkX * 2, self.chunkY)
        print("Loading: 88%")
        self.generate_spawners(self.chunkX * 2, self.chunkY * 2)
        print("Loading: 100%")

        while self.running:
            self.prevFps = self.fps
            self.fps = pygame.time.Clock().tick(60)

            # check for player movemet before rendering
            self.player_movement()

            # print(Main.x, Main.y)

            # set movement
            Main.rect = Main.rect.move(Main.speed)

            self.reorder_rendering()
            self.render_sprite()
            self.render_gui()
            self.render_text()

            pygame.display.update()

    def generate_new_num(self, minN, maxN):
        self.generation_number = random.randint(minN, maxN)
        return self.generation_number

    def generate_spawners(self, x, y):
        global screenX, screenY
        i = 0
        n = 0
        while i < 20:
            xN = self.generate_new_num(x - self.chunkX, x - 1)
            yN = self.generate_new_num(y - self.chunkY, y - 1)
            self.generate_new_num(1, 65536)
            if self.generation_number <= 10:
                i += 1
                airSpawner = LoadResource("spawner.png", (64, 64), xN, yN, "spawner", "Air Spawner")
                airSpawner.child = LoadResource("air.png", (32, 32), airSpawner.x + random.randint(-100, 100), airSpawner.y + random.randint(-100, 100), "element", "Air", airSpawner.id)
            elif self.generation_number >= 100 and self.generation_number <= 110:
                i += 1
                earthSpawner = LoadResource("spawner.png", (64, 64), xN, yN, "spawner", "Earth Spawner")
                earthSpawner.child = LoadResource("earth.png", (32, 32), earthSpawner.x + random.randint(-100, 100), earthSpawner.y + random.randint(-100, 100), "element", "Earth", earthSpawner.id)
            elif self.generation_number >= 1000 and self.generation_number <= 1010:
                i += 1
                fireSpawner = LoadResource("spawner.png", (64, 64), xN, yN, "spawner", "Fire Spawner")
                fireSpawner.child = LoadResource("fire.png", (32, 32), fireSpawner.x + random.randint(-100, 100), fireSpawner.y + random.randint(-100, 100), "element", "Fire", fireSpawner.id)
            elif self.generation_number >= 10000 and self.generation_number <= 10010:
                i += 1
                waterSpawner = LoadResource("spawner.png", (64, 64), xN, yN, "spawner", "Water Spawner")
                waterSpawner.child = LoadResource("water.png", (32, 32), waterSpawner.x + random.randint(-100, 100), waterSpawner.y + random.randint(-100, 100), "element", "Water", waterSpawner.id)

    def player_movement(self):
        global screenX, screenY, gEvent
        for event in pygame.event.get():
            gEvent = event
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == KEYUP and Main.allowMovement:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    Main.movementFlags[0] = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    Main.movementFlags[1] = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    Main.movementFlags[2] = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    Main.movementFlags[3] = 0
            elif event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if Crafting.render:
                        Crafting.render = False
                        Main.allowMovement = True
                        self.redraw_elements()
                        Crafting.Font.render = False
                        CraftingCombo.render = False
                    else:
                        self.running = False
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and Main.y > -2148 and Main.allowMovement:
                    Main.movementFlags[0] = 1
                if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and Main.y < 4196 and Main.allowMovement:
                    Main.movementFlags[1] = 1
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and Main.x > -2148 and Main.allowMovement:
                    Main.movementFlags[2] = 1
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and Main.x < 4196 and Main.allowMovement:
                    Main.movementFlags[3] = 1
                # Crafting menu
                if event.key == pygame.K_e:
                    Crafting.render = not Crafting.render
                    Main.allowMovement = not Main.allowMovement

                    if Crafting.render == False:
                        self.redraw_elements()
                        CraftingCombo.render = False
                    
                    Main.movementFlags = [0, 0, 0, 0]
                    Main.speed = [0, 0]
                    try:
                        Crafting.Font.render = not Crafting.Font.render
                    except:
                        Crafting.Font = LoadFont("gabs_pixel.ttf", 48, "Crafting", color["black"], (Window.width / 2 - Window.width / 11, Window.height / 2 - Window.height / 12), False)
                # drop an item
                if event.key == pygame.K_q:
                    try:
                        Main.items.pop()
                    except: pass
                    self.redraw_elements()
                if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    Main.items = []
                    self.redraw_elements()
        if Main.allowMovement:
            if Main.rect.x < Window.width / 2 - 50 and Main.movementFlags[2] and Main.x > -2148:
                screenX += 5
                Main.speed[0] += .3
                if Main.rect.x < Window.width / 2 - 60 and not Main.movementFlags[3]:
                    Main.speed[0] = 0
            elif Main.speed[0] != Main.movement[0] and Main.movementFlags[2] and Main.x > -2148:
                Main.speed[0] = Main.movement[0]
            elif (not Main.movementFlags[2] and not Main.movementFlags[3]) or Main.x < -2148:
                Main.speed[0] = 0

            if Main.rect.y < Window.height / 2 - 50 and Main.movementFlags[0] and Main.y > -2148:
                screenY += 5
                Main.speed[1] += .3
                if Main.rect.y < Window.height / 2 - 60 and not Main.movementFlags[1] and Main.movementFlags[0]:
                    Main.speed[1] = 0
            elif Main.speed[1] != Main.movement[0] and Main.movementFlags[0] and Main.y > -2148:
                Main.speed[1] = Main.movement[0]
            elif (not Main.movementFlags[0] and not Main.movementFlags[1]) or Main.y < -2148:
                Main.speed[1] = 0

            if Main.rect.x > Window.width / 2 + 20 and Main.movementFlags[3] and Main.x < 4196:
                screenX -= 5
                Main.speed[0] -= .3
                if Main.rect.x > Window.width / 2 + 30 and not Main.movementFlags[2] and Main.movementFlags[3]:
                    Main.speed[0] = 0
            elif Main.speed[0] != Main.movement[1] and Main.movementFlags[3] and Main.x < 4196:
                Main.movementFlags[2] = 0
                Main.speed[0] = Main.movement[1]
            elif (not Main.movementFlags[2] and not Main.movementFlags[3]):
                Main.speed[0] = 0

            if Main.rect.y > Window.height / 2 + 20 and Main.movementFlags[1] and Main.y < 4196:
                screenY -= 5
                Main.speed[1] -= .3
                if Main.rect.y > Window.height / 2 + 30 and not Main.movementFlags[0] and Main.movementFlags[1]:
                    Main.speed[1] = 0
            elif Main.speed[1] != Main.movement[1] and Main.movementFlags[1] and Main.y < 4196:
                Main.speed[1] = Main.movement[1]
            elif (not Main.movementFlags[0] and not Main.movementFlags[1]):
                Main.speed[1] = 0

    def reorder_rendering(self):
        dummy = []
        order = ["background", "spawner", "element", "sprite", "character", "textbox", "gui", "topGui", "combo"]
        for i in range(len(order)):
            for j in Window.spriteList:
                if j.type == order[i]:
                    dummy.append(j)
        # print([i.type for i in dummy])
        Window.spriteList = dummy

    def render_sprite(self):
        for i in Window.spriteList:
            if i.type != "textbox" and i.type != "background":
                if i.type == "spawner":
                    if self.prevFps != self.fps:
                        i.timer += 1
                    if (i.timer == 30 + random.randint(-6, 6) or i.timer == 40) and i.resProd < 10:
                        copyElem = LoadResource(i.child.image, i.child.size, i.child.x, i.child.y, "element", i.child.name, i.id, 1)
                        i.children.append(copyElem)
                        Window.spriteList.append(i.children[len(i.children) - 1])
                        i.child = LoadResource(i.child.image, i.child.size, i.x + random.randint(-100, 100), i.y + random.randint(-100, 100), "element", i.child.name, i.id, 1)
                        i.timer = 0
                        i.resProd += 1
                    elif i.resProd >= 10:
                        i.timer = 0
                    # print(i.resProd)
                elif i.type == "element":
                    self.elem_interact(i)
                if i.type != "character" and i.type != "topGui" and i.type != "gui" and i.type != "topGuiElement":
                    i.rect.center = (i.x + screenX, i.y + screenY)
                elif i.type == "character":
                    i.x = i.rect.x - screenX
                    i.y = i.rect.y - screenY
                if i.render == True:
                    pygame.draw.rect(Window.screen, color["black"], i.rect, -1)
                    Window.screen.blit(i.shape, i.rect)
                else:
                    if i.type != "gui":
                        i.render = True
            elif i.type == "background":
                i.tile_background()

    def render_gui(self):
        element_count = {"count": 0, "elements": []}
        for i in Window.guiList:
            self.elem_interact(i)
            pygame.draw.rect(Window.screen, color["black"], i.rect, -1)
            Window.screen.blit(i.shape, i.rect)
            if Crafting.render:
                i.clickable = True
                self.check_for_drag(i, element_count)
            if element_count["count"] > 1:
                CraftingCombo.render = True
            #    for j in self.elements.values():
            #        if j["recipe"] == element_count["elements"]:
            #            CraftedElement = LoadSprite("fire.png", (32, 32), CraftingCombo.rect.x, CraftingCombo.rect.y, "combo", j["name"], 65536)
            #            break
            # figure this out. please
            else:
                CraftingCombo.render = False
    
    def check_for_drag(self, element, count):
        global gEvent
        if gEvent.type == MOUSEBUTTONDOWN:
            if gEvent.button == 1 and element.rect.collidepoint(gEvent.pos):
                element.draging = True
                mx, my = gEvent.pos
                element.offsetX = element.rect.x - mx
                element.offsetY = element.rect.y - my
        elif gEvent.type == MOUSEBUTTONUP:
            if gEvent.button == 1:
                element.draging = False
        elif gEvent.type == MOUSEMOTION:
            if element.draging:
                mx, my = gEvent.pos
                element.rect.x = mx + element.offsetX
                element.rect.y = my + element.offsetY
        if not (element.rect.x < Crafting.rect.x or element.rect.x > Crafting.bottomX or element.rect.y < Crafting.rect.y or element.rect.y > Crafting.bottomY):
            count["count"] += 1
            count["elements"].append(element.name.replace(".gui", ""))

    def elem_interact(self, element):
        global Gui
        px, py = Main.rect.center
        ex, ey = element.rect.center
        if abs(px - ex) < 48 and abs(py - ey) < 48 and len(Main.items) < 100 and Main.allowMovement:
            Main.items.append(element)
            Window.spriteList.remove(element)
            for j in Window.spriteList:
                try:
                    if j.id == element.parentId:
                        j.resProd -= 1
                except: continue
            
            self.elemsort(Main)
            self.redraw_elements()

            pop = pygame.mixer.Sound('pop.mp3')
            pygame.mixer.Sound.set_volume(pop, 1.0)
            pygame.mixer.Sound.play(pop)
            pygame.mixer.Sound.fadeout(pop, 75)

    def elemsort(self, inventory):
        order = ["Air", "Earth", "Fire", "Water"]
        dummy = []
        for i in range(len(order)):
            for j in inventory.items:
                if j.name == order[i]:
                    dummy.append(j)
        inventory.items = dummy

    def redraw_elements(self):
        incX = 0
        incY = 0
        lID = 0
        x = []
        for i in Window.guiList:
            if i.type == "combo":
                x = LoadSprite(i.image, (20, 20), CraftingCombo.rect.x, CraftingCombo.rect.y, "combo", i.name, 65536)
            
        Window.guiList = []
        if x != []:
            Window.guiList.append(x)

        for j in Main.items:
            offset = len(Main.items) * 7.5
            if offset > 50 * 7.5: offset = 50 * 7.5
            x = LoadSprite(j.image, (20, 20), Window.width / 2 + incX - offset, Window.height - 40 + incY, "topGuiElement", j.name + ".gui", lID)

            incX += 16
            if incX >= 50 * 16:
                incX = 0
                incY += 16
        
        # print([i.name for i in Window.guiList], [i.name for i in Main.items])


    def render_text(self):
        for i in Window.fontList:
            if i.render:
                Window.screen.blit(i.image, i.placement)

Game = GameClass()
Game.run()

pygame.quit()
quit()
