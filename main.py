import pygame
import sys

WIN_WIDTH = 800
WIN_HEIGHT = 800

def main():
    pygame.init()

    original_icon = pygame.image.load("logo.png")
    icon_size = (32, 32)
    icon = pygame.transform.scale(original_icon, icon_size)
    pygame.display.set_icon(icon)

    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("freg")

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                break
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
