import random
import pygame
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
        self.cave_hp = 200
        self.bat_timer = 0
        self.stal_timer = 0

        # Списки
        self.bats_list = pygame.sprite.Group()
        self.stalagtites_list = pygame.sprite.Group()
        self.fall_stal_list = pygame.sprite.Group()
        self.fallen_stal_list = pygame.sprite.Group()


    def run(self): 
        a = self.update()
        self.on_draw()
        self.clock.tick(FPS)
        return a
            
    def on_key_press(self, key):
        pass
    
    def on_mouse_press(self, key):
        pass
    
    def on_key_release(self, key):
        pass 

    
    def on_draw(self):

        # очистить экран
        self.screen.fill((88, 83, 89))

        # отрисовать списки
        self.bats_list.draw(self.screen)
        self.stalagtites_list.draw(self.screen)
        self.fall_stal_list.draw(self.screen)
        self.fallen_stal_list.draw(self.screen)

        # отобразить
        pygame.display.flip()


    def update(self):

        # проверить взаимодействия
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return 0
            if e.type == pygame.KEYDOWN:
                self.on_key_press(e)
                print(1)
            if e.type == pygame.MOUSEBUTTONDOWN:
                self.on_mouse_press(e)
                print(2)
            if e.type == pygame.KEYUP:
                self.on_key_release(e)
                print(3)

        # обновить таймеры   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Сделать зависимости!!!!!!!!!!!!!!!!!!!!!
        self.bat_timer += 1
        self.stal_timer += 1
        if self.bat_timer == 100:
            self.generated_bat()
            self.bat_timer = 0
        if self.stal_timer == 100:
            self.generated_stal()
            self.stal_timer = 0
        
        # обновить списки
        self.bats_list.update()
        self.stalagtites_list.update()
        self.fall_stal_list.update()
        self.fallen_stal_list.update()

        # kill killed bat
        pygame.sprite.groupcollide(self.bats_list, self.stalagtites_list, 1, 0)
        pygame.sprite.groupcollide(self.bats_list, self.fall_stal_list, 1, 0)
        pygame.sprite.groupcollide(self.bats_list, self.fallen_stal_list, 1, 0)

        
        return 1
    
    def generated_bat(self):
        x = random.randint(0, 1)
        y = 1000 - random.randint(100, 900)
        if x == 0:
            bat = Bat(-100, y, 0)
        else:
            bat = Bat(2100, y, 1)
        self.bats_list.add(bat)

    def generated_stal(self):
        x = random.randint(0, 2000)
        stal = Stalagtite(x, -20)
        self.stalagtites_list.add(stal)

    def sel_fall_stal(self, x, y, size):
        self.fall_stal_list.add(Stalagtite_fall(x, y, size))

    def sel_fallen_stal(self, x, y, size):
        self.fallen_stal_list.add(Stalagtite_fallen(x, y, size))


    
class Bat(pygame.sprite.Sprite):
    def __init__(self, x, y, tol):
        super().__init__()
        self.height = 100
        self.width = 100
        self.images = []
        self.images.append(pygame.transform.scale(pygame.image.load('pics/bat/bat1.png'), (self.width, self.height)))
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
            game.sel_fall_stal(self.rect.x, self.rect.y, self.height)
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
            game.sel_fallen_stal(self.rect.x, self.rect.y, self.height)
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


if __name__ == "__main__":
    main() 