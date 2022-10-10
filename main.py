import pygame
import os

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
        self.spriteList = {}
        self.fontList = {}

Window = WindowClass((1920, 1080), "Alchemy Adventure Battle!")

class LoadSprite:
    def __init__(self, image, size, type="sprite", name="test", x=0, y=0, resource=None, defense=None, amount=0):
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
            self.items = {}
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
        elif type == "element":
            self.x = x
            self.y = y
            self.attack = resource
            self.defense = defense
            self.amount = amount
        else:
            self.x = x
            self.y = y
            
        Window.spriteList[self.name] = self

Main = LoadSprite("Main.png", (64, 64), "character", "Placeholder")
textbox = LoadSprite("Textbox.png", (512, 320), "textbox", "textbox")

class GameClass:
    def __init__(self):
        self.running = True
        self.background = color["white"]
        self.fps = 0
        self.resources = {}
    
    def run(self):
        while self.running:
            self.fps = pygame.time.Clock().tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_UP:
                        Ruby.speed[1] = Main.movement[0]
                    if event.key == pygame.K_DOWN:
                        Ruby.speed[1] = Main.movement[1]
                    if event.key == pygame.K_LEFT:
                        Ruby.speed[0] = Main.movement[0]
                    if event.key == pygame.K_RIGHT:
                        Ruby.speed[0] = Main.movement[1]
                    if event.key == pygame.K_e:
                        textbox.open = not textbox.open
                elif event.type == KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        Main.speed[1] = 0
                    if event.key == pygame.K_DOWN:
                        Main.speed[1] = 0
                    if event.key == pygame.K_LEFT:
                        Main.speed[0] = 0
                    if event.key == pygame.K_RIGHT:
                        Main.speed[0] = 0

            Main.rect = Main.rect.move(Main.speed)
            Main.current_x, Main.current_y = Main.rect.center

            Window.screen.fill(self.background)

            for i in Window.spriteList:
                i = Window.spriteList[i]

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
