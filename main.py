from asyncio import events
from ctypes.wintypes import SIZE
from logging import exception
import pygame
import time
import random

SIZE = 40
Background_Color = (31, 48, 45) 

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg")
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x=random.randint(0,20)*40
        self.y=random.randint(0,15)*40

class Snake:
    def __init__(self, parent_screen, length):
        self.length=length
        self.parent_screen=parent_screen
        self.block=pygame.image.load("resources/block.jpg").convert()
        # x and y axes
        self.x=[SIZE] * length
        self.y=[SIZE] * length

        self.direction='down'
    
    def draw(self):
        self.parent_screen.fill(Background_Color)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_up(self):
        self.direction = "up"

    def move_down(self):    
        self.direction = "down"

    def move_right(self):   
        self.direction = "right"

    def move_left(self):        
        self.direction = "left"

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction=='up':
            self.y[0] -= SIZE
        if self.direction=='down':
            self.y[0] += SIZE
        if self.direction=='right':
            self.x[0] += SIZE
        if self.direction=='left':
            self.x[0] -= SIZE
        self.draw()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self) :
        pygame.init()
        pygame.mixer.init()
        self.surface=pygame.display.set_mode((1200,700))
        self.surface.fill((31, 48, 45))
        
        self.snake=Snake(self.surface, 1)
        self.snake.draw()

        self.apple=Apple(self.surface)
        self.apple.draw()
    
    def play(self):
        self.snake.walk()
        self.apple.draw()   
        self.displayScore()
        pygame.display.flip()

        # if snake colloide with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            sound=pygame.mixer.Sound("resources/ding.mp3")
            pygame.mixer.Sound.play(sound)
            self.snake.increase_length()
            self.apple.move()

        # if snake colloide with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0], self.snake.x[i], self.snake.y[i] ):
                sound=pygame.mixer.Sound("resources/crash.mp3")
                pygame.mixer.Sound.play(sound)

                raise "Game Over"

    def run(self):
        running = True
        pause = False
        while running:  
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:    #detects a key being pressed
                    if event.key == pygame.K_ESCAPE:
                        running=False
                    if event.key == pygame.K_RETURN:
                        pause = False
                    if not pause:
                        if event.key == pygame.K_UP:
                            self.snake.move_up()
                            
                        if event.key == pygame.K_DOWN:
                            self.snake.move_down()

                        if event.key == pygame.K_RIGHT:
                            self.snake.move_right()

                        if event.key == pygame.K_LEFT:
                            self.snake.move_left()

                elif event.type == pygame.QUIT:
                    running=False

            try: 
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause=True
                self.reset()

            time.sleep(0.2)   

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 <= x2+SIZE:
            if y1 >= y2 and y1 <= y2+SIZE:
                return True
        return False
    
    def displayScore(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score : {self.snake.length} ", True, (255, 255, 255)) 
        self.surface.blit(score, (800, 10))

    def show_game_over(self):
        self.surface.fill(Background_Color)
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Game over! Your Score is : {self.snake.length} ", True, (255, 255, 255)) 
        self.surface.blit(score, (200, 300))
        line2 = font.render(f"To play again press Enter. To exit press Escape!", True, (255, 255, 255)) 
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()
    
    def reset(self):
        self.apple = Apple(self.surface)
        self.snake = Snake(self.surface, 1)

if __name__ == "__main__":
    game = Game()
    game.run()

