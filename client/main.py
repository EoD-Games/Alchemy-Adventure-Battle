import pygame
from pygame.locals import *
import os
import sys
import numpy as np
import random
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

class WindowClass:
    def __init__(self, size=(1920, 1080), title="Window", color=color["white"]):
        self.size = size
        self.title = pygame.display.set_caption(title)
        self.width, self.height = size
        self.screen = pygame.display.set_mode(self.size)
        self.color = color
        self.center = (self.width/2, self.height/2)
        self.spriteList = []
        self.fontList = []
        self.guiList = []

Window = WindowClass((1920 / 2, 1080 / 2), "Alchemy Adventure Battle!")

screenX = 0
screenY = 0

class LoadSprite:
    def __init__(self, image, size, x, y, type="sprite", name="test", lID=0):
        try:
            self.image = pygame.image.load(image).convert_alpha()
        except: self.image = image
        self.size = size
        self.width, self.height = size
        self.shape = pygame.transform.scale(self.image, self.size)
        self.name = name
        self.rect = self.shape.get_rect()
        self.type = type
        self.render = True
        if type == "character":
            self.rect.center = (x, y)
            self.x, self.y = self.rect.center
            self.speed = [0, 0]
            self.movement = [-4, 4]
            self.movementFlags = [0, 0, 0, 0]
            self.items = []
            Window.spriteList.append(self)
        elif type == "gui" or type == "topGui":
            self.rect.center = (x, y)
            self.x, self.y = self.rect.center
            self.items = []
            Window.spriteList.append(self)
        elif type == "textbox":
            self.x = Window.width - self.width
            self.y = Window.height - self.height
            self.rect.center = (self.x, self.y)
            self.x, self.y = self.rect.center
            self.open = False
            self.eKey = False
            Window.spriteList.append(self)
        elif type == "topGuiElement":
            self.render = False
            self.id = lID
            self.rect.center = (x, y)
            self.x, self.y = self.rect.center
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

Main = LoadSprite("Main.png", (64, 64), 256, 256, "character", "Player")
Gui = LoadSprite("hotbar.png", (Window.width - 64, 64), Window.width / 2, Window.height - 32, "topGui", "hotbar")
# textbox = LoadSprite("Textbox.png", (512, 320), "textbox", "textbox")

resourceId = 0

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

airSpawner = LoadResource("spawner.png", (64, 64), 500, 300, "spawner", "Air Spawner")
airSpawner.child = LoadResource("air.png", (32, 32), airSpawner.x + random.randint(-100, 100), airSpawner.y + random.randint(-100, 100), "element", "Air", airSpawner.id)
earthSpawner = LoadResource("spawner.png", (64, 64), 500, 600, "spawner", "Earth Spawner")
earthSpawner.child = LoadResource("earth.png", (32, 32), earthSpawner.x + random.randint(-100, 100), earthSpawner.y + random.randint(-100, 100), "element", "Earth", earthSpawner.id)
fireSpawner = LoadResource("spawner.png", (64, 64), 800, 300, "spawner", "Fire Spawner")
fireSpawner.child = LoadResource("fire.png", (32, 32), fireSpawner.x + random.randint(-100, 100), fireSpawner.y + random.randint(-100, 100), "element", "Fire", fireSpawner.id)
waterSpawner = LoadResource("spawner.png", (64, 64), 800, 600, "spawner", "Water Spawner")
waterSpawner.child = LoadResource("water.png", (32, 32), waterSpawner.x + random.randint(-100, 100), waterSpawner.y + random.randint(-100, 100), "element", "Water", waterSpawner.id)

keydown = True

class GameClass:
    def __init__(self):
        self.running = True
        self.background = color["white"]
        self.prevFps = 0
        self.fps = 0
        self.resources = {}
    
    def run(self):
        global screenX, screenY, keydown
        while self.running:
            self.prevFps = self.fps
            self.fps = pygame.time.Clock().tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == KEYUP:
                    keydown = False
                    if event.key == pygame.K_UP:
                        Main.speed[1] = 0
                        Main.movementFlags[0] = 0
                    if event.key == pygame.K_DOWN:
                        Main.speed[1] = 0
                        Main.movementFlags[1] = 0
                    if event.key == pygame.K_LEFT:
                        Main.speed[0] = 0
                        Main.movementFlags[2] = 0
                    if event.key == pygame.K_RIGHT:
                        Main.speed[0] = 0
                        Main.movementFlags[3] = 0
                elif event.type == pygame.KEYDOWN:
                    keydown = True
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_UP:
                        Main.speed[1] = Main.movement[0]
                        Main.movementFlags[0] = 1
                    if event.key == pygame.K_DOWN:
                        Main.speed[1] = Main.movement[1]
                        Main.movementFlags[1] = 1
                    if event.key == pygame.K_LEFT:
                        Main.speed[0] = Main.movement[0]
                        Main.movementFlags[2] = 1
                    if event.key == pygame.K_RIGHT:
                        Main.speed[0] = Main.movement[1]
                        Main.movementFlags[3] = 1
                    if event.key == pygame.K_e:
                        textbox.open = not textbox.open
                    if event.key == pygame.K_q:
                        Main.items = []
                        self.redraw_elements()

            if Main.rect.x < 48:
                screenX += 1 * (1 + (1 / Main.rect.x) * 120)
                Main.speed[0] += .3 * (1 + 1 / Main.rect.x)
                if Main.rect.x < 30 and not Main.movementFlags[3] and Main.movementFlags[2]:
                    Main.speed[0] = 0
            elif Main.speed[0] != Main.movement[0] and Main.movementFlags[2]:
                Main.speed[0] = Main.movement[0]
            elif not (Main.movementFlags[2] or Main.movementFlags[3]):
                Main.speed[0] = 0

            if Main.rect.y < 48:
                screenY += 1 * (1 + (1 / Main.rect.y) * 120)
                Main.speed[1] += .3 * (1 + 1 / Main.rect.y)
                if Main.rect.y < 30 and not Main.movementFlags[1] and Main.movementFlags[0]:
                    Main.speed[1] = 0
            elif Main.speed[1] != Main.movement[0] and Main.movementFlags[0]:
                Main.speed[1] = Main.movement[0]
            elif not (Main.movementFlags[0] or Main.movementFlags[1]):
                Main.speed[1] = 0

            if Main.rect.x > Window.width - 48 - 64:
                screenX -= 1 * (1 + (Window.width / Main.rect.x) * 5)
                Main.speed[0] -= .3 * (1 + Window.width / Main.rect.x)
                if Main.rect.x > Window.width - 40 - 64 and not Main.movementFlags[2] and Main.movementFlags[3]:
                    Main.speed[0] = 0
            elif Main.speed[0] != Main.movement[1] and Main.movementFlags[3]:
                Main.speed[0] = Main.movement[1]
            elif not (Main.movementFlags[3] or Main.movementFlags[2]):
                Main.speed[0] = 0

            if Main.rect.y > Window.height - 48 - 64 - 32:
                screenY -= 1 * (1 + (Window.height / Main.rect.y) * 5)
                Main.speed[1] -= .3 * (1 + Window.height / Main.rect.y)
                if Main.rect.y > Window.height - 40 - 64 - 32 and not Main.movementFlags[0] and Main.movementFlags[1]:
                    Main.speed[1] = 0
            elif Main.speed[1] != Main.movement[1] and Main.movementFlags[1]:
                Main.speed[1] = Main.movement[1]
            elif not (Main.movementFlags[1] or Main.movementFlags[0]):
                Main.speed[1] = 0
            
            Main.rect = Main.rect.move(Main.speed)

            Window.screen.fill(self.background)

            self.reorder_rendering()

            for i in Window.spriteList:
                if i.type != "textbox":
                    if i.type == "spawner":
                        if self.prevFps != self.fps:
                            i.timer += 1
                        if (i.timer == 20 + random.randint(-4, 4) or i.timer == 25) and i.resProd < 10:
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

                    if i.render == True:
                        pygame.draw.rect(Window.screen, color["black"], i.rect, -1)
                        Window.screen.blit(i.shape, i.rect)
                    else:
                        i.render = True
            
            for i in Window.guiList:
                self.elem_interact(i)
                pygame.draw.rect(Window.screen, color["black"], i.rect, -1)
                Window.screen.blit(i.shape, i.rect)

            pygame.display.update()
    
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
        
        print([i.name for i in Window.guiList], [i.name for i in Main.items])

    def reorder_rendering(self):
        dummy = []
        order = ["gui", "spawner", "element", "sprite", "character", "textbox", "topGui"]
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
