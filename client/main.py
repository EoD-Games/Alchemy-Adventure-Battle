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

# Font=pygame.freetype.Font('font.ttf',  48)

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
    def __init__(self, size=(1920, 1080), title="Window", color=color["white"]):
        # size of the window
        self.size = size
        # set title
        self.title = pygame.display.set_caption(title)
        # width and height specification
        self.width, self.height = size
        # set the screen size
        self.screen = pygame.display.set_mode(self.size)
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

# Must be called "Window"
Window = WindowClass((1920 / 2, 1080 / 2), "Alchemy Adventure Battle!")

# position of top right corner of screen
screenX = 0
screenY = 0

# SPRITES EXCLUDING RESOURCES #
class LoadSprite:
    def __init__(self, image, size, x, y, type="sprite", name="test", lID=0):
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
        # render flag
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
            # inventory
            self.items = []
        elif type == "gui" or type == "topGui":
            # center of gui
            self.rect.center = (x, y)
            # first frame x and y of gui
            self.x, self.y = self.rect.center
            # list of items within gui
            self.items = []
        elif type == "textbox":
            # x and y are absolute
            self.x = Window.width - self.width
            self.y = Window.height - self.height
            self.rect.center = (self.x, self.y)
            # open flag
            self.open = False
            # e key is pressed flag
            self.eKey = False
        elif type == "topGuiElement":
            # render flag set to false
            self.render = False
            # id for displaying
            self.id = lID
            # center
            self.rect.center = (x, y)
            self.x, self.y = self.rect.center
        else:
            self.rect.center = (x, y)
            self.x, self.y = self.rect.center
        
        # put into display list
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
Main = LoadSprite("Main.png", (64, 64), 256, 256, "character", "Player")
# MAIN GUI MUST BE GUI
Gui = LoadSprite("hotbar.png", (Window.width - 64, 64), Window.width / 2, Window.height - 32, "topGui", "hotbar")

# textbox = LoadSprite("Textbox.png", (512, 320), "textbox", "textbox")

resourceId = 0

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

keydown = True

class GameClass:
    def __init__(self):
        self.running = True
        self.background = color["white"]
        self.prevFps = 0
        self.fps = 0
        self.resources = {}
        self.generation_number = 0
        self.generateNewChunk = False
        self.chunkX, self.chunkY = (2048, 2048)
        self.generated_area = []
    
    def run(self):
        global screenX, screenY
        random.seed(random.randint(0, 65535))
        # TODO: get seed from server

        print("Loading: 0%")
        self.generate_spawners(self.chunkX, self.chunkY)
        self.generated_area.append([0, 0])
        self.generate_spawners(0, 0)
        self.generated_area.append([-1, -1])
        print("Loading: 25%")
        self.generate_spawners(self.chunkX * 2, self.chunkY)
        self.generated_area.append([1, 0])
        self.generate_spawners(0, self.chunkY)
        self.generated_area.append([-1, 0])
        print("Loading: 50%")
        self.generate_spawners(self.chunkX, self.chunkY * 2)
        self.generated_area.append([0, 1])
        self.generate_spawners(self.chunkX, 0)
        self.generated_area.append([0, -1])
        print("Loading: 75%")
        self.generate_spawners(self.chunkX * 2, self.chunkY * 2)
        self.generated_area.append([1, 1])
        print("Loading: 100%")

        while self.running:

            self.prevFps = self.fps
            self.fps = pygame.time.Clock().tick(60)

            self.player_movement()

            Main.rect = Main.rect.move(Main.speed)

            self.reorder_rendering()

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
                        i.render = True
                elif i.type == "background":
                    i.tile_background()

            
            for i in Window.guiList:
                self.elem_interact(i)
                pygame.draw.rect(Window.screen, color["black"], i.rect, -1)
                Window.screen.blit(i.shape, i.rect)

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
        global screenX, screenY, keydown
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == KEYUP:
                keydown = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    Main.speed[1] = 0
                    Main.movementFlags[0] = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    Main.speed[1] = 0
                    Main.movementFlags[1] = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    Main.speed[0] = 0
                    Main.movementFlags[2] = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    Main.speed[0] = 0
                    Main.movementFlags[3] = 0
            elif event.type == pygame.KEYDOWN:
                keydown = True
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and Main.y > -2148:
                    Main.speed[1] = Main.movement[0]
                    Main.movementFlags[0] = 1
                if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and Main.y < 4196:
                    Main.speed[1] = Main.movement[1]
                    Main.movementFlags[1] = 1
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and Main.x > -2148:
                    Main.speed[0] = Main.movement[0]
                    Main.movementFlags[2] = 1
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and Main.x < 4196:
                    Main.speed[0] = Main.movement[1]
                    Main.movementFlags[3] = 1
                if event.key == pygame.K_e:
                    # textbox.open = not textbox.open
                    print("text")
                if event.key == pygame.K_q:
                    Main.items = []
                    self.redraw_elements()

        if Main.rect.x < 48 and Main.movementFlags[2] and Main.x > -2148:
            screenX += 1 * (1 + (1 / Main.rect.x) * 120)
            Main.speed[0] += .3 * (1 + 1 / Main.rect.x)
            if Main.rect.x < 30 and not Main.movementFlags[3]:
                Main.speed[0] = 0
        elif Main.speed[0] != Main.movement[0] and Main.movementFlags[2] and Main.x > -2148:
            Main.speed[0] = Main.movement[0]
        elif not (Main.movementFlags[2] or Main.movementFlags[3]) or Main.x < -2048:
            Main.speed[0] = 0

        if Main.rect.y < 48 and Main.movementFlags[0] and Main.y > -2148:
            screenY += 1 * (1 + (1 / Main.rect.y) * 120)
            Main.speed[1] += .3 * (1 + 1 / Main.rect.y)
            if Main.rect.y < 30 and not Main.movementFlags[1] and Main.movementFlags[0]:
                Main.speed[1] = 0
        elif Main.speed[1] != Main.movement[0] and Main.movementFlags[0] and Main.y > -2148:
            Main.speed[1] = Main.movement[0]
        elif not (Main.movementFlags[0] or Main.movementFlags[1]) or Main.y < -2148:
            Main.speed[1] = 0

        if Main.rect.x > Window.width - 40 - 64 and Main.movementFlags[3] and Main.x < 4196:
            screenX -= 1 * (1 + (Window.width / Main.rect.x) * 3)
            Main.speed[0] -= .3 * (1 + Window.width / Main.rect.x)
            if Main.rect.x > Window.width - 32 - 64 and not Main.movementFlags[2] and Main.movementFlags[3]:
                Main.speed[0] = 0
        elif Main.speed[0] != Main.movement[1] and Main.movementFlags[3] and Main.x < 4196:
            Main.speed[0] = Main.movement[1]
        elif not (Main.movementFlags[3] or Main.movementFlags[2]) or Main.x > 4196:
            Main.speed[0] = 0

        if Main.rect.y > Window.height - 48 - 64 - 32 and Main.movementFlags[1] and Main.y < 4196:
            screenY -= 1 * (1 + (Window.height / Main.rect.y) * 3)
            Main.speed[1] -= .3 * (1 + Window.height / Main.rect.y)
            if Main.rect.y > Window.height - 42 - 64 - 32 and not Main.movementFlags[0] and Main.movementFlags[1]:
                Main.speed[1] = 0
        elif Main.speed[1] != Main.movement[1] and Main.movementFlags[1] and Main.y < 4196:
            Main.speed[1] = Main.movement[1]
        elif not (Main.movementFlags[1] or Main.movementFlags[0]) or Main.y > 4196:
            Main.speed[1] = 0

    def elem_interact(self, element):
        global Gui
        px, py = Main.rect.center
        ex, ey = element.rect.center
        if abs(px - ex) < 48 and abs(py - ey) < 48 and len(Main.items) < 40:
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

    def text_interact(self, text):
        pygame.draw.rect(Window.screen, color["red"], textbox.rect, -1)
        Window.screen.blit(textbox.shape, textbox.rect)

        Font.antialiased = False
        # print(textbox.rect)
        Font.render_to(Window.screen, (textbox.x - 200, textbox.y - 100), text, color["black"])

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
        Window.guiList = []

        for j in Main.items:
            x = LoadSprite(j.image, (20, 20), Gui.x + incX - (Gui.size[0] / 2 - 35), Gui.y + incY, "topGuiElement", j.name + ".gui", lID)

            incX += 16
            if incX > 50 * 16:
                incX = 0
                incY += 16
        
        # print([i.name for i in Window.guiList], [i.name for i in Main.items])

    def reorder_rendering(self):
        dummy = []
        order = ["background", "gui", "spawner", "element", "sprite", "character", "textbox", "topGui"]
        for i in range(len(order)):
            for j in Window.spriteList:
                if j.type == order[i]:
                    dummy.append(j)
        # print([i.type for i in dummy])
        Window.spriteList = dummy

Game = GameClass()
Game.run()

pygame.quit()
quit()
