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
        self.bat_list = pygame.sprite.Group()


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
        self.bat_list.draw(self.screen)

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
        
        # обновить списки
        self.bat_list.update()
        
        return 1
    
    def generated_bat(self):
        x = random.randint(0, 1)
        y = 1000 - random.randint(300, 900)
        if x == 0:
            bat = Bat(-100, y, 0)
        else:
            bat = Bat(2100, y, 1)
        self.bat_list.add(bat)

    
class Bat(pygame.sprite.Sprite):
    def __init__(self, x, y, tol):
        super().__init__()
        self.height = 100
        self.width = 100
        self.images = []
        self.images.append(pygame.transform.scale(pygame.image.load('pics/bat/bat.png'), (self.width, self.height)))
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





#куча констант
SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 1000
FPS = 60



def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    a = 1
    while a:
        a = game.run()


if __name__ == "__main__":
    main() 