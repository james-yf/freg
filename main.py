import pygame
import time
import random
import sys

WIN_WIDTH = 800
WIN_HEIGHT = 800
FRUIT_SIZE = 64
FALL_SPEED = 250
BG = (0,0,0)

class GameState:
    def handle_input(self, event):
        pass
    def update(self, dt):
        pass
    def draw(self, screen):
        pass

class Fruit(pygame.sprite.Sprite):
    def __init__(self, pos, fruit_img, fall_speed):
        super().__init__()
        self.image = fruit_img
        self.rect = self.image.get_rect()
        self.rect.topleft = pos 
        self.fall_speed = fall_speed

    def update(self, dt):
        self.rect.y += self.fall_speed * dt 

class PlayState(GameState):
    _FRUIT_IMGS_CACHE = {}
    _FRUIT_NAMES = ["apple", "grapes", "tomato", "melon", "bananas"]

    def __init__(self):
        if not PlayState._FRUIT_IMGS_CACHE:
            self._load_fruit_imgs()

        self.fruits = pygame.sprite.Group()

        self.SPAWN_EVENT = pygame.event.custom_type()
        pygame.time.set_timer(self.SPAWN_EVENT, 1000)

        self.font = pygame.font.Font(None, 75)
        self.score = 0
        self.update_score_surface()

        self.click_sound = pygame.mixer.Sound("assets/audio/pop.wav")
        self.click_sound.set_volume(0.5)

    def _load_fruit_imgs(self):
        for name in PlayState._FRUIT_NAMES:
            img = pygame.image.load(f"assets/imgs/{name}.png").convert()
            scaled_img = pygame.transform.scale(img, (FRUIT_SIZE, FRUIT_SIZE))
            # Gets the color of pixel (0,0) and makes any pixels of that color in the img
            # transparent. This works great atm, since none of the assets i've drawn contain
            # white except in the background, which we want to remove. 
            scaled_img.set_colorkey(img.get_at((0,0)))
            PlayState._FRUIT_IMGS_CACHE[name] = scaled_img

    def spawn_fruit(self):
        x_for_fruits_at_top = [fruit.rect.x for fruit in self.fruits if fruit.rect.y == FRUIT_SIZE] 
        while True:
            x = random.randint(1, WIN_WIDTH // FRUIT_SIZE - 1) * FRUIT_SIZE 
            if x in x_for_fruits_at_top: continue 
            fruit_type = random.choice(PlayState._FRUIT_NAMES)
            self.fruits.add(Fruit((x, FRUIT_SIZE), PlayState._FRUIT_IMGS_CACHE[fruit_type], FALL_SPEED))
            break
            
    def handle_input(self, event):
        if event.type == self.SPAWN_EVENT:
            for i in range(5):
                self.spawn_fruit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for fruit in self.fruits:
                if fruit.rect.collidepoint(event.pos):
                    fruit.kill()
                    self.score += 1
                    self.update_score_surface()
                    self.click_sound.play()


    def update(self, dt):
        self.fruits.update(dt)
        for fruit in self.fruits:
            if fruit.rect.bottom >= WIN_HEIGHT:
                fruit.kill()

    def update_score_surface(self):
        self.score_surface = self.font.render(f"Score: {self.score}", True, (255,255,255))

    def draw(self, screen):
        screen.fill(BG)
        screen.blit(self.score_surface, (100, 0)) 
        self.fruits.draw(screen)

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.update_icon()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("freg")

        pygame.mixer.init()
        pygame.mixer.music.load("assets/audio/bg.ogg")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        self.running=True
        self.state = PlayState()

    def update_icon(self):
        unscaled_icon = pygame.image.load("logo.png")
        scale_size = (32, 32)
        scaled_icon = pygame.transform.scale(unscaled_icon, scale_size)
        pygame.display.set_icon(scaled_icon)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                    break
                self.state.handle_input(e)
            self.state.update(dt)
            self.state.draw(self.screen)
            pygame.display.flip()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
