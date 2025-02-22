import pygame
from sys import exit
from pygame.locals import *
import os
from random import randrange, choice

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
som_colisao = pygame.mixer.Sound(os.path.join(sons, 'death_sound.wav'))
som_colisao.set_volume(1)

colidiu = False

escolha_obstaculo = choice([0,1])


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
        self.mask = pygame.mask.from_surface(self.image)
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
        self.rect.x -=15

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
        self.rect.x -=15

class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5*32, 0, 32,32))
        self.image = pygame.transform.scale(self.image, (32*2,32*2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect.center = (LARGURA, ALTURA-60)
        self.rect.x = LARGURA
        
    def update(self):
        if self.escolha == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -=15
class DinoVoador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img_dinossauro = []
        for i in range(3,5):
            img = sprite_sheet.subsurface((i * 32, 0, 32,32))
            img = pygame.transform.scale(img,(32*3, 32*3))
            self.img_dinossauro.append(img)
        self.atual = 0
        self.image = self.img_dinossauro[self.atual]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA, 300)
        self.rect.x = LARGURA
        self.escolha = escolha_obstaculo

    def update(self):
        if self.escolha == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -=15
            if self.atual >=1:
                self.atual = 0
            self.atual += 0.25
            self.image = self.img_dinossauro[int(self.atual)]

todas_sprites = pygame.sprite.Group()

dino = Dino()

todas_sprites.add(dino)

for i in range(4):
    nuvens = Nuvem()
    todas_sprites.add(nuvens)

for i in range(LARGURA*2//64):#Lagura da tela (640px) dividido por cada frame do objeto chão (64px).Obs; Fiz uma gambiarra pra que o chão não quebrasse
    chao = Chao(i)
    todas_sprites.add(chao)

cacto = Cacto()

todas_sprites.add(cacto)

grupo_obstaculos = pygame.sprite.Group()

grupo_obstaculos.add(cacto)

dino_voador = DinoVoador()

todas_sprites.add(dino_voador)

grupo_obstaculos.add(dino_voador)


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
        
    colisoes = pygame.sprite.spritecollide(dino,grupo_obstaculos, False, pygame.sprite.collide_mask) #Lista que recebe os obstáculos que o dino colide
    todas_sprites.draw(tela)#Desenha na tela todas as sprites.

    if cacto.rect.topright[0] <= 0 or dino_voador.rect.topright[0] <= 0:
        escolha_obstaculo = choice([0,1])
        cacto.rect.x = LARGURA
        dino_voador.rect.x = LARGURA
        cacto.escolha = escolha_obstaculo
        dino_voador.escolha = escolha_obstaculo
    if colisoes and colidiu == False:
        som_colisao.play()
        colidiu = True

    if colidiu == True:
        pass

    else:
        todas_sprites.draw(tela)
        todas_sprites.update()#Atualiza o movimento das sprites.
    
    pygame.display.flip()
