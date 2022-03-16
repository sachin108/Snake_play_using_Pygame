from asyncio import events
import pygame

if __name__ == "__main__":
    pygame.init()

    surface=pygame.display.set_mode((1000,500))
    surface.fill((31, 48, 45))
    pygame.display.flip()

    running = True
    while running:  
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:    #detects a key being pressed
                if event.key == pygame.K_ESCAPE:
                    running=False
                pass
            elif event.type == pygame.QUIT:
                running=False