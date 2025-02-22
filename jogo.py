import pygame
from sys import exit
from pygame.locals import *
import os
from random import randrange

pygame.init()

pygame.mixer.init()


diretorio_principal = os.path.dirname(__file__)
imagens = os.path.join(diretorio_principal, 'imagens')
sons = os.path.join(diretorio_principal, 'sons')

LARGURA = 640 
ALTURA = 480

PRETO = (0,0,0)
BRANCO = (255,255,255)

tela = pygame.display.set_mode((LARGURA,ALTURA))

pygame.display.set_caption('Dino')

sprite_sheet = pygame.image.load(os.path.join(imagens, 'dinoSpritesheet.png')).convert_alpha()

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(os.path.join(sons, 'jump_sound.wav'))
        self.som_pulo.set_volume(1)
        self.img_dinossauro = []
        for i in range(3):
            img = sprite_sheet.subsurface((i * 32, 0, 32,32))
            img = pygame.transform.scale(img, (32*3,32*3))
            self.img_dinossauro.append(img)

        self.atual = 0
        self.image = self.img_dinossauro[self.atual]
        self.rect =  self.image.get_rect()
        self.rect.center = (100,ALTURA-60)
        self.pulo = False
        self.pos_inicial_y = ALTURA - 60 - 96//2 #Pegando o centro da imagem pois o rect pega a parte superior esquerda
    def pular(self):
        self.pulo = True
        self.som_pulo.play()
    def update(self):
        if self.pulo == True:
            if self.rect.y <=260:
                self.pulo = False
            self.rect.y -=20
        else:
            if self.rect.y < self.pos_inicial_y:
                self.rect.y +=20

            else:
                self.rect.y = self.pos_inicial_y
        
        if self.atual >=2:
            self.atual = 0
        self.atual += 0.25
        self.image = self.img_dinossauro[int(self.atual)]

class Nuvem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7*32,0,32,32))
        self.image = pygame.transform.scale(self.image, (32*3,32*3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50,200,50)
        self.x = LARGURA - randrange(30,300,90)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
            self.rect.y = randrange(50,200,50)
            self.x = LARGURA - randrange(30,300,90)
        self.rect.x -=7

class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6*32, 0, 32,32))
        self.image = pygame.transform.scale(self.image, (32*2,32*2))
        self.rect = self.image.get_rect()
        self.rect.y = ALTURA-64
        self.rect.x = pos_x * 64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
        self.rect.x -=7

todas_sprites = pygame.sprite.Group()

dino = Dino()

todas_sprites.add(dino)

for i in range(4):
    nuvens = Nuvem()
    todas_sprites.add(nuvens)

for i in range(LARGURA*2//64):#Lagura da tela (640px) dividido por cada frame do objeto chão (64px).Obs; Fiz uma gambiarra pra que o chão não quebrasse
    chao = Chao(i)
    todas_sprites.add(chao)
relogio = pygame.time.Clock()

while True:
    relogio.tick(20)
    tela.fill(BRANCO)
    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            exit()
        if evento.type == KEYDOWN:
            if evento.key == K_SPACE:
                if dino.rect.y != dino.pos_inicial_y:
                    pass
                else:
                    dino.pular()
    todas_sprites.draw(tela)
    todas_sprites.update()
    
    pygame.display.flip()
