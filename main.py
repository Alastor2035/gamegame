import random
import pygame
from draw import *

class Game():
    """ Главный класс приложения. """
    
    def __init__(self, width, height):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("bat_cave")
        self.clock = pygame.time.Clock()
        
        # Баланс
        self.score = 0      
        self.cave_hp = 100
        self.live = 3
        self.bat_timer = 0
        self.stal_timer = 0

        # cannot
        self.cannot = Cannot(1000, 800)

        # Списки
        self.bats_list = pygame.sprite.Group()
        self.stalagtites_list = pygame.sprite.Group()
        self.fall_stal_list = pygame.sprite.Group()
        self.fallen_stal_list = pygame.sprite.Group()
        self.cannots_list = pygame.sprite.Group()
        self.balls_list = pygame.sprite.Group()

        self.cannots_list.add(self.cannot)


    def run(self): 
        a = self.update()
        self.on_draw()
        self.clock.tick(FPS)
        return a
            

    
    def on_draw(self):

        # очистить экран
        self.screen.fill((88, 83, 89))


        # отрисовать списки
        self.bats_list.draw(self.screen)
        self.stalagtites_list.draw(self.screen)
        self.fall_stal_list.draw(self.screen)
        self.fallen_stal_list.draw(self.screen)
        self.cannots_list.draw(self.screen)
        self.balls_list.draw(self.screen)

        # для проверки потом убрать
        drawText(self.screen, (255, 255, 255), str(self.cave_hp), pygame.Rect(700, 50+35, 300, 30), font_size=30)
        drawText(self.screen, (255, 255, 255), str(self.score), pygame.Rect(700, 50+35+ 35, 300, 30), font_size=30)
        drawText(self.screen, (255, 255, 255), str(self.live), pygame.Rect(700, 50+35+35+35, 300, 30), font_size=30)


        # отобразить
        pygame.display.flip()


    def update(self):

        if self.live <= 0:
            return 0

        # проверить взаимодействия
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return 0
            else:
                self.cannot.move(e)

        # обновить таймеры   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Сделать зависимости!!!!!!!!!!!!!!!!!!!!!
        self.bat_timer += 1
        self.stal_timer += 1
        if self.bat_timer == 100:
            self.generated_bat()
            self.bat_timer = 0
        if self.stal_timer >=  80 + self.cave_hp*0.05:
            self.generated_stal()
            self.stal_timer = 0

        
        # обновить списки
        self.bats_list.update()
        self.stalagtites_list.update()
        self.fall_stal_list.update()
        self.fallen_stal_list.update()
        self.cannots_list.update()
        self.balls_list.update()

        # kill killed bat
        pygame.sprite.groupcollide(self.bats_list, self.stalagtites_list, 1, 0, pygame.sprite.collide_mask)
        pygame.sprite.groupcollide(self.bats_list, self.fall_stal_list, 1, 0, pygame.sprite.collide_mask)
        pygame.sprite.groupcollide(self.bats_list, self.fallen_stal_list, 1, 0, pygame.sprite.collide_mask)

        # collapse gan/fallen stalagtites
        q = len(self.fallen_stal_list)
        pygame.sprite.groupcollide(self.cannots_list, self.fallen_stal_list, 0, 1, pygame.sprite.collide_mask)
        self.live -= q - len(self.fallen_stal_list)

        # collapse ball/bat stalagtites
        q = len(self.bats_list)
        pygame.sprite.groupcollide(self.balls_list, self.bats_list, 0, 1, pygame.sprite.collide_mask)
        self.score += (q - len(self.bats_list)) * 10

        # collapse ball/fall stalagtite stalagtites
        q = len(self.bats_list)
        pygame.sprite.groupcollide(self.balls_list, self.fall_stal_list, 1, 1, pygame.sprite.collide_mask)



        return 1
    
    def generated_bat(self):
        x = random.randint(0, 1)
        y = 1000 - random.randint(300, 900)
        if x == 0:
            bat = Bat(-100, y, 0)
        else:
            bat = Bat(2100, y, 1)
        self.bats_list.add(bat)

    def generated_stal(self):
        x = random.randint(0, 2000)
        stal = Stalagtite(x, -20)
        self.stalagtites_list.add(stal)

    def set_fall_stal(self, x, y, size):
        self.fall_stal_list.add(Stalagtite_fall(x, y, size))

    def set_fallen_stal(self, x, y, size):
        self.fallen_stal_list.add(Stalagtite_fallen(x, y, size))

    def shot(self, stx, sty, fnx, fny):
        if len(self.balls_list) <= 3:
            dx = fnx - stx
            dy = fny - sty
            self.balls_list.add(Ball(stx, sty, 40*dx/(dx*dx+dy*dy)**0.5, 40*dy/(dx*dx+dy*dy)**0.5))


    
class Bat(pygame.sprite.Sprite):
    def __init__(self, x, y, tol):
        super().__init__()
        self.height = 100
        self.width = 100
        self.images = []
        for i in range(19):
            self.images.append(pygame.transform.scale(pygame.image.load("pics/bat/"+ str(i) +".gif"), (self.width, self.height)).convert_alpha())
        if tol == 0:
            for i in range(len(self.images)):
                self.images[i] = pygame.transform.flip(self.images[i], True, False)
        self.img_index = 0
        self.image = self.images[self.img_index]
        self.tol = tol
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.rect.x = x
        self.rect.y = y

    
    def update(self):
        super().update()

        # движение
        if self.tol == 0:
            self.rect.x += 5
        else:
            self.rect.x -= 5

        # самовыпил
        if self.rect.x < -110 or self.rect.x > 2110:
            self.kill()

        # обновление картинки
        self.img_index += 1
        if self.img_index >= len(self.images):
            self.img_index = 0
        self.image = self.images[self.img_index]


class Stalagtite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.height = 1
        self.width = 1
        self.time_to_die = 1000
        self.preimage = pygame.image.load('pics/stalagtite.png').convert_alpha()
        self.image = pygame.transform.scale(self.preimage, (self.width, self.height))
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.rect.x = x
        self.rect.y = y

    
    def update(self):
        super().update()
        self.time_to_die -= 1


        # самовыпил
        if self.time_to_die <= 0:
            game.set_fall_stal(self.rect.x, self.rect.y, self.height)
            self.kill()

        # обновление картинки
        self.height += 0.1
        self.width += 0.1
        self.image = pygame.transform.scale(self.preimage, (self.width, self.height))
        self.rect = pygame.Rect(self.rect.x+0.5, self.rect.y, self.width, self.height)

class Stalagtite_fall(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.height = size
        self.width = size
        self.v = 0
        self.preimage = pygame.image.load('pics/stalagtite.png').convert_alpha()
        self.image = pygame.transform.scale(self.preimage, (self.width, self.height))
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.rect.x = x
        self.rect.y = y

    
    def update(self):
        super().update()

        # moving
        self.v += 1
        self.rect.y += self.v


        # самовыпил
        if self.rect.y + self.height > 1000:
            game.set_fallen_stal(self.rect.x, self.rect.y, self.height)
            game.cave_hp -= 5
            self.kill()

class Stalagtite_fallen(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.height = size
        self.width = size
        self.time_to_die = 100
        self.preimage = pygame.image.load('pics/stalagtite.png').convert_alpha()
        self.image = pygame.transform.scale(self.preimage, (self.width, self.height))
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.rect.x = x
        self.rect.y = y

    
    def update(self):
        super().update()

        self.time_to_die -= 1


        # самовыпил
        if self.time_to_die <= 0:
            self.kill()

class Cannot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.height = 200
        self.width = 400
        self.v = 0
        self.a = 0
        self.preimage = pygame.image.load('pics/cannot.png').convert_alpha()
        self.image = pygame.transform.scale(self.preimage, (self.width, self.height))
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        super().update()


        if abs(self.v) < 20 and self.a != 0:
            self.v += self.a
            if abs(self.v) > 20:
                self.v = 20 * self.v / abs(self.v)
        if self.a == 0:
            self.v *= 0.95
        
        self.rect.x += self.v

        if self.rect.x < -100 or self.rect.x > 1700:
            self.v = -self.v * 0.4
            self.rect.x += 5.1 * self.v


    def move(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_a:
                self.a = -0.3
            if e.key == pygame.K_d:
                self.a = 0.3
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_a or e.key == pygame.K_d:
                self.a = 0
        if e.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            game.shot(self.rect.x+70, self.rect.y, x, y)

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy):
        super().__init__()
        self.height = 50
        self.width = 50
        self.vx = vx
        self.vy = vy
        self.preimage = pygame.image.load('pics/ball.png').convert_alpha()
        self.image = pygame.transform.scale(self.preimage, (self.width, self.height))
        self.rect = pygame.Rect(x+ self.width/2, y+self.height/2, self.width/2, self.height/2)

    def update(self):
        super().update()

        self.rect.x += self.vx
        self.vy += 1
        self.rect.y += self.vy

        # самовыпил
        if self.rect.y > 1100:
            self.kill()

        
    







#куча констант
SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 1000
FPS = 60



def main():
    global game
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    a = 1
    while a:
        a = game.run()
    print(game.score)


if __name__ == "__main__":
    main() 