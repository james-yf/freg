import pygame
import sys

WIN_WIDTH = 800
WIN_HEIGHT = 800
FRUIT_SIZE = 64

def get_fruit_imgs():
    img_names = ["apple", "grapes", "tomato", "melon", "bananas"]
    imgs={}
    for name in img_names:
        img = pygame.image.load(f"assets/imgs/{name}.png").convert()
        scaled_img = pygame.transform.scale(img, (FRUIT_SIZE, FRUIT_SIZE))
        # Gets the color of pixel (0,0) and makes any pixels of that color in the img
        # transparent. This works great atm, since none of the assets i've drawn contain
        # white except in the background, which we want to remove. 
        scaled_img.set_colorkey(img.get_at((0,0)))
        imgs[name] = scaled_img
    return imgs

def main():
    pygame.init()

    clock = pygame.time.Clock()

    original_icon = pygame.image.load("logo.png")
    icon_size = (32, 32)
    icon = pygame.transform.scale(original_icon, icon_size)
    pygame.display.set_icon(icon)

    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("freg")

    fruit_imgs = get_fruit_imgs()

    x = FRUIT_SIZE
    for img in fruit_imgs.values():
        screen.blit(img, (x, FRUIT_SIZE))
        x += FRUIT_SIZE
    pygame.display.flip()

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                break
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
