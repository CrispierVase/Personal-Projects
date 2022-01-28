import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Movement test')
FPSCLOCK = pygame.time.Clock()

def main():
    done = False
    x = 0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        x += 3
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 0, 255), (x, 300, 70, 80))
        pygame.display.flip()
        FPSCLOCK.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()