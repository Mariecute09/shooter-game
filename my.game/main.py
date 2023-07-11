#Create your own shooter
from time import time as timer
from pygame import *
from random import randint
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

shoot_sound = mixer.Sound('fire.ogg')

WIDTH = 700
HEIGHT = 500
FPS = 40

lives = 3
score = 0
lost = 0
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Shooter game")
clock = time.Clock()
background = transform.scale(image.load('galaxy.jpg'),(WIDTH,HEIGHT))

class Main(sprite.Sprite):
    def __init__(self,img, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(img),(w,h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

        
class Player(Main):
    def controls(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x < 15:
           self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x > WIDTH - 40:
           self.rect.x += self.speed
        
        if keys[K_UP] and self.rect.y > 0 :
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < HEIGHT - 100:
            self.rect.y += self.speed
    
    def shoot(self):
        bullet = Bullet('bullet.png', self.rect.x + 10, self.rect.y - 1, 20, 30, 30)
        bullets.add(bullet)

class UFO(Main):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > HEIGHT - 50:
            self.rect.x = randint(50,WIDTH-50)
            self.rect.y = 0
            lost += 1

class Bullet(Main):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

player = Player("rocket.png", 250, 420, 40, 70, 30)

bullets = sprite.Group()

monsters = sprite.Group()
for i in range(1,7):
    monster = UFO("ufo.png",randint(50,WIDTH-50),-50, 90,50, randint(2,7))
    monsters.add(monster)

font.init()
style = font.Font(None, 35)

asteroids = sprite.Group()


num_fire = 0
reload_time = False
run = True
end = False
while run:
    screen.blit(background,(0,0))

    for e in event.get():
        if e.type == QUIT:
            run = False
            
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 15 and reload_time == False:
                    num_fire += 1
                    player.shoot()
                    shoot_sound.play()

                if num_fire >= 15 and reload_time == False:
                    time_start = timer()
                    reload_time = True


    
    
    if not end:
        screen.blit(background,(0,0))
        
        score_text = style.render("Score: "+str(score), True, (255,255,255))
        screen.blit(score_text,(25,25))
        
        lose_text = style.render("Missed: "+str(lost), True , (255,255,255))
        screen.blit(lose_text,(25, 60))
        
        player.controls()
        player.reset()
        monsters.update()
        bullets.update()
        asteroids.update()
        bullets.draw(screen)
        monsters.draw(screen)
        asteroids.draw(screen)

        if reload_time:
            time_end = timer()
            if (time_end - time_start) < 3:
                reload_text = style.render("Wait, reloading...", True, (255,0,0))
                screen.blit(reload_text,(WIDTH//2 - 50, HEIGHT - 50))
            else:
                num_fire = 0
                reload_time = False
            

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for i in collides:
            score += 1
            monster = UFO("ufo.png",randint(50,WIDTH-50),-50, 90,50, randint(2,7))
            monsters.add(monster)
        
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)
            lives -= 1

        #Winning condition
        win = style.render("YOU WIN", True, (255, 0, 0))
        if score >= 21:
            end = True
            screen.blit(win, (300,250))
            

        #Losing condition
        lose = style.render("YOU LOSE", True, (255, 0, 0))
        if lives <= 0 or lost >= 5:
            end = True
            screen.blit(lose, (300,250))
        text_life = style.render(str(lives), 1, (250,250,250))
        screen.blit(text_life,(WIDTH-70, 25))
        display.update()
    
    else:
        end = False
        score = 0
        lost = 0
        for m in monsters:
            m.kill()
        for b in bullets:
            b.kill()
        time.delay(3000)
        for i in range(1,7):
            monster = UFO('ufo.png', randint(50,WIDTH-50),-50, 90,50,randint(2,7))
            monsters.add(monster)
        for i in range(1,3):
            asteroid = UFO("asteroid.png", randint(50,WIDTH-50), -50, 75, 75, randint(2,5))
            asteroids.add(asteroid)

        
    time.delay(50)


    
