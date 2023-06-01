import pygame
from pygame.locals import *
import random

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
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        # direção x e y
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False

    # Crescimento da cobra
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

        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)

class Apple:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE)
        self.spawn()

    def spawn(self):
        self.rect.x = int(random.randint(0, largura) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect.y = int(random.randint(0, altura) / BLOCK_SIZE) * BLOCK_SIZE

    def update(self):
        pygame.draw.rect(tela, VERMELHO, self.rect)

    def get_position(self):
        return self.rect.x, self.rect.y

# Função de avaliação heurística para a busca gulosa
def heuristic(position1, position2):
    x1, y1 = position1
    x2, y2 = position2
    return abs(x1 - x2) + abs(y1 - y2)

# Função para obter a posição da cabeça da cobra
def get_snake_head_position():
    return snake.head.x, snake.head.y

# Função para obter a posição da maçã
def get_apple_position():
    return apple.get_position()

# Função para obter a próxima direção da cobra usando a busca gulosa
def get_next_direction():
    snake_head_position = get_snake_head_position()
    apple_position = get_apple_position()
    possible_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    best_direction = None
    best_distance = float('inf')

    for direction in possible_directions:
        new_x = snake_head_position[0] + direction[0] * BLOCK_SIZE
        new_y = snake_head_position[1] + direction[1] * BLOCK_SIZE
        new_position = (new_x, new_y)
        distance = heuristic(new_position, apple_position)

        if distance < best_distance:
            best_distance = distance
            best_direction = direction

    return best_direction

# Grade de desenhos
def drawGrid():
    # Controla a posição x
    for x in range(0, largura, BLOCK_SIZE):
        # Controla a posição y
        for y in range(0, altura, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(tela, COR, rect, 1)

score = fonte.render('0', True, BRANCO)
score_rect = score.get_rect(center=(largura / 2, altura / 20))

drawGrid()
snake = Snake()
apple = Apple()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if snake.ydir != -1:
                snake.ydir = 1
                snake.xdir = 0
            elif snake.ydir != 1:
                snake.ydir = -1
                snake.xdir = 0
            elif snake.xdir != -1:
                snake.ydir = 0
                snake.xdir = 1
            elif snake.xdir != 1:
                snake.ydir = 0
                snake.xdir = -1

    snake.update()

    tela.fill(PRETO)
    drawGrid()

    score = fonte.render(f'{len(snake.body) - 2 + 1}', True, BRANCO)

    apple.update()

    pygame.draw.rect(tela, VERDE, snake.head)

    for square in snake.body:
        pygame.draw.rect(tela, VERDE, square)

    tela.blit(score, score_rect)

    if snake.head.x == apple.rect.x and snake.head.y == apple.rect.y:
        snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        apple.spawn()

    next_direction = get_next_direction()

    if next_direction:
        snake.xdir, snake.ydir = next_direction

    pygame.display.update()
    clock.tick(10)
