import pygame
import pygame.freetype
from pygame.locals import *
import numpy as np

# INITIALIZE #
pygame.init()
pygame.font.init()

Font=pygame.freetype.Font('TextboxFont.ttf',  48)

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
        self.spriteList = {}
        self.fontList = {}

Window = WindowClass((1920, 1080), "Pokemon Game")

class LoadSprite:
    def __init__(self, image, size, type="sprite", name="test", x=0, y=0, resource=None):
        self.image = pygame.image.load(image).convert_alpha()
        self.size = size
        self.width, self.height = size
        self.shape = pygame.transform.scale(self.image, self.size)
        self.name = name
        self.rect = self.shape.get_rect()
        self.type = type
        if type == "character":
            self.rect.center = (0, 0)
            self.prev_x = 0
            self.prev_y = 0
            self.current_x = x
            self.current_y = y
            self.speed = [0, 0]
            self.movement = [-4, 4]
        elif type == "sprite" or type == "gui":
            self.x = x
            self.y = y
            self.rect.center = (self.x, self.y)
        elif type == "textbox":
            self.x = Window.width - self.width
            self.y = Window.height - self.height
            self.rect.center = (self.x, self.y)
            self.open = False
            self.eKey = False
        elif type == "vein":
            self.x = x
            self.y = y
            self.resource = resource
            self.resAmnt = 0
        else:
            self.x = x
            self.y = y
            
        Window.spriteList[self.name] = self

Ruby = LoadSprite("Ruby.png", (64, 64), "character", "Ruby")
Dad = LoadSprite("Dad.png", (64, 64), "sprite", "Dad", 300, 300)
textbox = LoadSprite("Textbox.png", (512, 320), "textbox", "textbox")

class GameClass:
    def __init__(self):
        self.running = True
        self.background = color["white"]
        self.fps = 0
        self.resources = {}
    
    def run(self):
        while self.running:
            if self.fps > 0:
                Ruby.prev_x, Ruby.prev_y = Ruby.current_x, Ruby.current_y

            self.fps = pygame.time.Clock().tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_UP:
                        Ruby.speed[1] = Ruby.movement[0]
                    if event.key == pygame.K_DOWN:
                        Ruby.speed[1] = Ruby.movement[1]
                    if event.key == pygame.K_LEFT:
                        Ruby.speed[0] = Ruby.movement[0]
                    if event.key == pygame.K_RIGHT:
                        Ruby.speed[0] = Ruby.movement[1]
                    if event.key == pygame.K_e:
                        textbox.open = not textbox.open
                elif event.type == KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        Ruby.speed[1] = 0
                    if event.key == pygame.K_DOWN:
                        Ruby.speed[1] = 0
                    if event.key == pygame.K_LEFT:
                        Ruby.speed[0] = 0
                    if event.key == pygame.K_RIGHT:
                        Ruby.speed[0] = 0

            Ruby.rect = Ruby.rect.move(Ruby.speed)
            Ruby.current_x, Ruby.current_y = Ruby.rect.center

            Window.screen.fill(self.background)

            for i in Window.spriteList:
                i = Window.spriteList[i]
                if i.type == "character":
                    if abs(i.current_x - Dad.x) < 64 and abs(i.current_y - Dad.y) < 64:
                        i.rect = i.rect.move([-x for x in i.speed])
                    if abs(i.current_x - Dad.x) <128 and abs(i.current_y - Dad.y) < 128 and textbox.open:
                        self.interact("Hello, I'm " + Dad.name + ".")
                if i.type != "textbox":
                    pygame.draw.rect(Window.screen, color["black"], i.rect, -1)
                    Window.screen.blit(i.shape, i.rect)
            pygame.display.update()
    
    def interact(self, text):
        pygame.draw.rect(Window.screen, color["red"], textbox.rect, -1)
        Window.screen.blit(textbox.shape, textbox.rect)

        Font.antialiased = False
        print(textbox.rect)
        Font.render_to(Window.screen, (textbox.x - 200, textbox.y - 100), text, color["black"])

Game = GameClass()
Game.run()

pygame.quit()
quit()

class Tilemap:
    def __init__(self, tileset, size=(64, 64), rect=None):
        self.size = size
        self.tileset = tileset
        self.map = np.zeros(size, dtype=int)

        h, w = self.size
        self.image = pygame.Surface(*32*w, 32*h)
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()
    
    def render(self):
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                self.image.blit(tile, (j*32, i*32))

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        print(self.map)
        print(self.map.shape)
        self.render()

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        print(self.map)
        self.render()

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'

# tilemap = Tilemap(Ruby.image, Ruby.size, Ruby.rect)

