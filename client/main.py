import pygame
from pygame.locals import *
import os
import numpy as np
import random
import copy

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

Window = WindowClass((1920, 1080), "Alchemy Adventure Battle!")

class LoadSprite:
    def __init__(self, image, size, x, y, type="sprite", name="test"):
        self.image = pygame.image.load(image).convert_alpha()
        self.size = size
        self.width, self.height = size
        self.shape = pygame.transform.scale(self.image, self.size)
        self.name = name
        self.rect = self.shape.get_rect()
        self.type = type
        if type == "character":
            self.rect.center = (x, y)
            self.speed = [0, 0]
            self.movement = [-4, 4]
            self.items = []
        elif type == "sprite" or type == "gui":
            self.rect.center = (x, y)
        elif type == "textbox":
            self.x = Window.width - self.width
            self.y = Window.height - self.height
            self.rect.center = (self.x, self.y)
            self.open = False
            self.eKey = False
        else:
            self.rect.center = (x, y)
        
        Window.spriteList.append(self)

Main = LoadSprite("Main.png", (64, 64), 64, 64, "character", "Placeholder")
# textbox = LoadSprite("Textbox.png", (512, 320), "textbox", "textbox")

resourceId = 0

class LoadResource:
    def __init__(self, image, size, x, y, type="element", name="test", pID=0, check=0, attack=0, defense=0):
        global resourceId
        self.size = size
        self.width, self.height = size
        self.name = name
        self.type = type
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
            
            self.rect.center = (x, y)
            self.x, self.y = self.rect.center
            self.attack = attack
            self.defense = defense
            self.parentId = pID

airSpawner = LoadResource("AirSpawn.png", (64, 64), 100, 100, "spawner", "Air Spawner")
airSpawner.child = LoadResource("Air.png", (64, 64), airSpawner.x + random.randint(-100, 100), airSpawner.y + random.randint(-100, 100), "element", "Air", airSpawner.id)

class GameClass:
    def __init__(self):
        self.running = True
        self.background = color["white"]
        self.prevFps = 0
        self.fps = 0
        self.resources = {}
    
    def run(self):
        while self.running:
            self.prevFps = self.fps
            self.fps = pygame.time.Clock().tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        Main.speed[1] = 0
                    if event.key == pygame.K_DOWN:
                        Main.speed[1] = 0
                    if event.key == pygame.K_LEFT:
                        Main.speed[0] = 0
                    if event.key == pygame.K_RIGHT:
                        Main.speed[0] = 0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_UP:
                        Main.speed[1] = Main.movement[0]
                    if event.key == pygame.K_DOWN:
                        Main.speed[1] = Main.movement[1]
                    if event.key == pygame.K_LEFT:
                        Main.speed[0] = Main.movement[0]
                    if event.key == pygame.K_RIGHT:
                        Main.speed[0] = Main.movement[1]
                    if event.key == pygame.K_e:
                        textbox.open = not textbox.open

            Main.rect = Main.rect.move(Main.speed)

            Window.screen.fill(self.background)

            self.reorder_rendering()

            for i in Window.spriteList:
                if i.type != "textbox":
                    if i.type == "spawner":
                        if self.prevFps != self.fps:
                            i.timer += 1
                        if i.timer == 20 and i.resProd < 10:
                            copyElem = LoadResource(i.child.image, i.child.size, i.child.x, i.child.y, "element", i.child.name, i.id, 1)
                            i.children.append(copyElem)
                            Window.spriteList.append(i.children[len(i.children) - 1])
                            i.child = LoadResource(i.child.image, i.child.size, i.x + random.randint(-100, 100), i.y + random.randint(-100, 100), "element", i.child.name, i.id, 1)
                            i.timer = 0
                            i.resProd += 1
                        elif i.resProd >= 10:
                            i.timer = 0
                        print(i.resProd)
                    if i.type == "element":
                        self.elem_interact(i)
                    
                    pygame.draw.rect(Window.screen, color["black"], i.rect, -1)
                    Window.screen.blit(i.shape, i.rect)
            
            print([i.name for i in Main.items])
            pygame.display.update()
    
    def elem_interact(self, element):
        px, py = Main.rect.center
        ex, ey = element.rect.center
        if abs(px - ex) < 64 and abs(py - ey) < 64:
            Main.items.append(element)
            Window.spriteList.remove(element)
            for j in Window.spriteList:
                try:
                    if j.id == element.parentId:
                        j.resProd -= 1
                except: continue


    def text_interact(self, text):
        pygame.draw.rect(Window.screen, color["red"], textbox.rect, -1)
        Window.screen.blit(textbox.shape, textbox.rect)

        Font.antialiased = False
        print(textbox.rect)
        Font.render_to(Window.screen, (textbox.x - 200, textbox.y - 100), text, color["black"])

    def reorder_rendering(self):
        dummy = []
        order = ["gui", "spawner", "element", "sprite", "character", "textbox"]
        for i in range(len(order)):
            for j in Window.spriteList:
                if j.type == order[i]:
                    dummy.append(j)
        print([i.type for i in dummy])
        Window.spriteList = dummy

Game = GameClass()
Game.run()

pygame.quit()
quit()
