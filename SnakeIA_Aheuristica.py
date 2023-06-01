import pygame
from pygame.locals import *
import random
import heapq

COR = (60, 60, 59)
VERDE = (21, 133, 45)
PRETO = (0, 0, 0)
VERMELHO = (230, 14, 14)
BRANCO = (255, 255, 255)

pygame.init()

largura = 700
altura = 700
BLOCK_SIZE = 50

fonte = pygame.font.SysFont('arial', BLOCK_SIZE*2)
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False

    def update(self):
        global apple

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
                self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
                self.dead = False

        self.body.append(self.head)
        for i in range(len(self.body)-1):
            self.body[i].x, self.body[i].y = self.body[i+1].x, self.body[i+1].y

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

class Node:
    def __init__(self, position, parent=None, g=0, h=0):
        self.position = position
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.position == other.position

def get_snake_head_position():
    return snake.head.x, snake.head.y

def get_apple_position():
    return apple.rect.x, apple.rect.y

def heuristic(position, target):
    return abs(position[0] - target[0]) + abs(position[1] - target[1])

def get_neighbors(position):
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    for direction in directions:
        neighbor = (position[0] + direction[0] * BLOCK_SIZE, position[1] + direction[1] * BLOCK_SIZE)
        if neighbor[0] in range(0, largura) and neighbor[1] in range(0, altura):
            neighbors.append(neighbor)
    return neighbors

def astar_search():
    start = Node(get_snake_head_position())
    target = get_apple_position()

    open_list = []
    closed_set = set()

    heapq.heappush(open_list, start)
    while open_list:
        current_node = heapq.heappop(open_list)
        closed_set.add(current_node.position)

        if current_node.position == target:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        for neighbor_position in get_neighbors(current_node.position):
            if neighbor_position in closed_set:
                continue

            neighbor = Node(neighbor_position, current_node)
            neighbor.g = current_node.g + BLOCK_SIZE
            neighbor.h = heuristic(neighbor.position, target)
            neighbor.f = neighbor.g + neighbor.h

            heapq.heappush(open_list, neighbor)

    return []

def update_snake_direction():
    path = astar_search()
    if path:
        next_position = path[1]
        if next_position[0] < snake.head.x:
            snake.xdir = -1
            snake.ydir = 0
        elif next_position[0] > snake.head.x:
            snake.xdir = 1
            snake.ydir = 0
        elif next_position[1] < snake.head.y:
            snake.xdir = 0
            snake.ydir = -1
        elif next_position[1] > snake.head.y:
            snake.xdir = 0
            snake.ydir = 1

# Grade de desenhos
def drawGrid():
    for x in range(0, largura, BLOCK_SIZE):
        for y in range(0, altura, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(tela, COR, rect, 1)

score = fonte.render('0', True, BRANCO)
score_rect = score.get_rect(center=(largura/2, altura/20))

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

    score = fonte.render(f'{len(snake.body)-2+1}', True, BRANCO)

    apple.update()

    pygame.draw.rect(tela, VERDE, snake.head)
    for square in snake.body:
        pygame.draw.rect(tela, VERDE, square)

    tela.blit(score, score_rect)

    if snake.head.x == apple.rect.x and snake.head.y == apple.rect.y:
        snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        apple.spawn()

    update_snake_direction()

    pygame.display.update()
    clock.tick(10)
