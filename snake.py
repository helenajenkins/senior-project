import pygame, sys, time, random
from pygame.locals import *

FPS = 10
pygame.init()
fpsClock = pygame.time.Clock()

GREEN = (106, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

WINDOWWIDTH = 400
WINDOWHEIGHT = 400
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Snake!')

surface = pygame.Surface(screen.get_size())
surface = surface.convert()
surface.fill(BLACK)
clock = pygame.time.Clock()

pygame.key.set_repeat(1, 40)

GRIDSIZE = 10
GRIDWIDTH = WINDOWWIDTH / GRIDSIZE
GRIDHEIGHT = WINDOWHEIGHT / GRIDSIZE
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
    
screen.blit(surface, (0, 0))

def drawBox(surf, color, pos):
    r = pygame.Rect((pos[0], pos[1]), (GRIDSIZE, GRIDSIZE))
    pygame.draw.rect(surf, color, r)

class Snake(object):
    def __init__(self):
        self.lose()
        self.color = GREEN

    def getHeadPosition(self):
        return self.positions[0]

    def lose(self):
        self.length = 1
        self.positions =  [((WINDOWWIDTH / 2), (WINDOWHEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def point(self, pt):
        if self.length > 1 and (pt[0] * -1, pt[1] * -1) == self.direction:
            return
        else:
            self.direction = pt

    def move(self):
        cur = self.positions[0]
        x, y = self.direction
        new = (((cur[0] + (x * GRIDSIZE)) % WINDOWWIDTH), (cur[1] + (y * GRIDSIZE)) % WINDOWHEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.lose()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
    
    def draw(self, surf):
        for p in self.positions:
            drawBox(surf, self.color, p)

class Apple(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize()

    def randomize(self):
        self.position = (random.randint(0, GRIDWIDTH - 1) * GRIDSIZE, random.randint(0, GRIDHEIGHT - 1) * GRIDSIZE)

    def draw(self, surf):
        drawBox(surf, self.color, self.position)

def checkEat(snake, apple):
    if snake.getHeadPosition() == apple.position:
        snake.length += 3
        apple.randomize()

if __name__ == '__main__':
    snake = Snake()
    apple = Apple()
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    snake.point(UP)
                elif event.key == K_DOWN:
                    snake.point(DOWN)
                elif event.key == K_LEFT:
                    snake.point(LEFT)
                elif event.key == K_RIGHT:
                    snake.point(RIGHT)


        surface.fill(BLACK)
        snake.move()
        checkEat(snake, apple)
        snake.draw(surface)
        apple.draw(surface)
        font = pygame.font.Font(None, 36)
        text = font.render(str(snake.length), 1, (106, 255, 0))
        textpos = text.get_rect()
        textpos.centerx = 20
        surface.blit(text, textpos)
        screen.blit(surface, (0, 0))

        pygame.display.flip()
        pygame.display.update()
        fpsClock.tick(FPS + snake.length/3)
