import pygame
from sys import exit
from pygame.locals import *
import os

pygame.init()

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
        self.img_dinossauro = []
        for i in range(3):
            img = sprite_sheet.subsurface((i * 32, 0, 32,32))
            img = pygame.transform.scale(img, (32*2,32*2))
            self.img_dinossauro.append(img)

        self.atual = 0
        self.image = self.img_dinossauro[self.atual]
        self.rect =  self.image.get_rect()
        self.rect.topleft = (150,230)

    def update(self):
        if self.atual >=2:
            self.atual = 0
        self.atual += 0.25
        self.image = self.img_dinossauro[int(self.atual)]
    


       
todas_sprites = pygame.sprite.Group()
dino = Dino()
todas_sprites.add(dino)

relogio = pygame.time.Clock()

while True:
    relogio.tick(20)
    tela.fill(BRANCO)
    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            exit()

    todas_sprites.draw(tela)
    todas_sprites.update()
    
    pygame.display.flip()
