
from pygame import *
from random import randint
from time import time as timer
window = display.set_mode((1300,800))
display.set_caption('Сезон охоты')
background = transform.scale(image.load('voda.png'),(1300,800))

clock = time.Clock()
FPS = 60







class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_speed,player_x,player_y,w,h):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(w,h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed=key.get_pressed()        
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 350:
            self.rect.x += self.speed
        if keys_pressed[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < 720:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet('pulya.png',3, self.rect.centerx,self.rect.top,80,80)
        bullets.add(bullet)

lost=0
class Enemy(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        global lost
        if self.rect.x <=0:
            lost = lost +1
            self.rect.x =1250
            self.rect.y = randint(0,750)




class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x >=1350:
            self.kill()           


hero =Player('stelok_1_lvl.png',10,300,400,100,85)
monsters = sprite.Group()
for i in range(5):
    
    monster = Enemy('utka.png',randint(2,4),1250,randint(0,750),80,65)
    monsters.add(monster)
font.init()
font1 = font.SysFont('comicsansms',36)


bullets = sprite.Group()

rel_time= False
num_fire=0
finish =False
game =True
score = 0
while game:
    if finish != True:

        text_reload = font1.render('wait reload',1,(255,255,255))
        window.blit(background,(0,0))
        
        
        hero.reset()
        hero.update()

        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        win=font1.render('ТЫСЯЧА ЧЕРТЕЙ!!!',1,(0,255,0))
        lose=font1.render('АЙ КАРАМБА',1,(255,0,0))
        sprites_list = sprite.groupcollide(monsters,bullets,True,True)
        sprites_list1 = sprite.spritecollide(hero,monsters,False)
        if len(sprites_list1) >0:
            finish=True
            window.blit(lose,(550,300))
        


        if score >10:
            finish=True
            window.blit(win,(450,300))

        

        for s in sprites_list:
            score +=1
            monster = Enemy('utka.png',randint(2,4),1250,randint(0,750),80,65)
            monsters.add(monster)
        if rel_time == True:
            new_time=timer()
            if new_time-old_time>=1:
                num_fire=0
                rel_time=False
            else:
                window.blit(text_reload,(1100,700))

        
   

          
        
        
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire<1 and rel_time==False:
                    hero.fire()
                    num_fire+=1
                else:
                    rel_time = True
                    old_time = timer()

    display.update()
    clock.tick(FPS) 