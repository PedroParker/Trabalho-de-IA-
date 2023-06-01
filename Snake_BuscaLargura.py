import pygame
from pygame.locals import *
import random
from collections import deque

COR = (60, 60, 59)
VERDE = (21, 133, 45)
PRETO = (0, 0, 0)
VERMELHO = (230, 14, 14)
BRANCO = (255, 255, 255)
pygame.init()

largura = 700
altura = 700
BLOCK_SIZE = 50
fonte = pygame.font.SysFont('arial', BLOCK_SIZE * 2)
pontos = 0
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False

    def update(self):
        global apple, pontos

        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
            if self.head.x not in range(0, largura) or self.head.y not in range(0, altura):
                self.dead = True

            if self.dead:
                self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
                self.xdir = 1
                self.ydir = 0
                self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
                self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
                self.dead = False

        self.body.append(self.head)
        for i in range(len(self.body) - 1):
            self.body[i].x, self.body[i].y = self.body[i + 1].x, self.body[i + 1].y
            pontos += 1
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)


class Apple:
    def __init__(self):
        self.x = int(random.randint(0, largura) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, altura) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def update(self):
        pygame.draw.rect(tela, VERMELHO, self.rect)


def drawGrid():
    for x in range(0, largura, BLOCK_SIZE):
        for y in range(0, altura, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(tela, COR, rect, 1)


def BFS (snake):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up
    queue = deque([(snake.head.x, snake.head.y, snake.xdir, snake.ydir, [])])
    visited = set()

    while queue:
        x, y, xdir, ydir, path = queue.popleft()
        if (x, y) == (apple.x, apple.y):
            return path
        if (x, y) in visited:
            continue
        visited.add((x, y))

        for dx, dy in directions:
            new_x = x + dx * BLOCK_SIZE
            new_y = y + dy * BLOCK_SIZE
            if (new_x, new_y) in snake.body:
                continue
            if new_x not in range(0, largura) or new_y not in range(0, altura):
                continue
            new_path = path + [(dx, dy)]
            queue.append((new_x, new_y, dx, dy, new_path))

    return []


drawGrid()
snake = Snake()
apple = Apple()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    path = BFS(snake)

    if path:
        dx, dy = path[0]
        snake.xdir = dx
        snake.ydir = dy

    snake.update()

    tela.fill(PRETO)
    drawGrid()

    score = fonte.render(f'{len(snake.body) - 2 + 1}', True, BRANCO)
    score_rect = score.get_rect(center=(largura / 2, altura / 20))

    apple.update()

    pygame.draw.rect(tela, VERDE, snake.head)

    for square in snake.body:
        pygame.draw.rect(tela, VERDE, square)

    tela.blit(score, score_rect)

    if snake.head.x == apple.x and snake.head.y == apple.y:
        snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        apple = Apple()

    pygame.display.update()
    clock.tick(10)
