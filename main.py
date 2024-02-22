from pygame import display, time, draw, QUIT, init, KEYDOWN, K_a, K_s, K_d, K_w
from random import randint
import pygame
from numpy import sqrt

init()
run = True
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
score = 0

cols = 25
rows = 25

width = 600
height = 600
# đồ họa game
backGround_img = pygame.image.load('bg.png')
backGround_img = pygame.transform.scale(backGround_img, (600, 600))
ball_img = pygame.image.load('apple.png')
ball_img = pygame.transform.scale(ball_img, (25, 25))
head_img = pygame.image.load('snake_head.png')
boom_img = pygame.image.load('bomb1.png')
head_img = pygame.transform.scale(head_img, (25, 25))
boom_img = pygame.transform.scale(boom_img, (25, 25))
body_img = pygame.image.load('snake_body4.png')
body_img = pygame.transform.scale(body_img, (25, 25))
rotated_body_img = pygame.transform.rotate(body_img, 90)
# Chieu rong, chieu cao moi o
wr = width / cols
hr = height / rows
direction = 1

screen = display.set_mode([width, height])
display.set_caption("snake_self")
clock = time.Clock()


# Khoi tao cac o trong matrix
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neis = []  # nei = neighbors
        self.parent = []  # danh sach cac o da di qua --> De truy vet duong di

        # Khoi tao bien obstrucle de danh dau cac o duoc xac dinh la chuong ngai vat
        self.obstrucle = False

        # Neu gia tri ngau nhien [1,100] < 3 thi o do duoc tinh la chuong ngai vat
        if randint(1, 100) < 3:
            self.obstrucle = True

    # def show(self, img):
    #     draw.rect(screen, img, [self.x*hr+2, self.y*wr+2, hr-4, wr-4])
    #     self.display.blit(img, pygame.Rect([self.x*hr+2, self.y*wr+2, hr-4, wr-4]))

    def _update_ui(self, screen, img, hr, wr):
        screen.blit(img, pygame.Rect([self.x * hr + 2, self.y * wr + 2, hr - 4, wr - 4]))

    def add_neighbors(self):
        if self.x > 0:
            self.neis.append(matrix[self.x - 1][self.y])  # Them o phia sau
        if self.y > 0:
            self.neis.append(matrix[self.x][self.y - 1])
        if self.x < rows - 1:
            self.neis.append(matrix[self.x + 1][self.y])
        if self.y < cols - 1:
            self.neis.append(matrix[self.x][self.y + 1])


def A_star(food1, snake1):
    food1.parent = []
    # Đặt danh sách trống cho tất cả các ô mà con rắn đã đi qua để đến được thức ăn.
    for s in snake1:
        s.parent = []
    openset = [snake1[-1]]
    closedset = []
    dir_array1 = []  # direction array
    while True:
        current1 = min(openset, key=lambda x: x.f)
        openset = [openset[i] for i in range(len(openset)) if not openset[i] == current1]
        closedset.append(current1)
        for neighbor in current1.neis:
            if neighbor not in closedset and not neighbor.obstrucle and neighbor not in snake1:
                temp_g = neighbor.g + 1
                if neighbor in openset:
                    if temp_g < neighbor.g:
                        neighbor.g = temp_g
                else:
                    neighbor.g = temp_g
                    openset.append(neighbor)
                neighbor.h = sqrt((neighbor.x - food1.x) ** 2 + (neighbor.y - food1.y) ** 2)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current1
        if current1 == food1:
            break
    # Truy vet
    while current1.parent:
        if current1.x == current1.parent.x and current1.y < current1.parent.y:
            dir_array1.append(2)  # di len
        elif current1.x == current1.parent.x and current1.y > current1.parent.y:
            dir_array1.append(0)  # di xuong
        elif current1.x < current1.parent.x and current1.y == current1.parent.y:
            dir_array1.append(3)  # trai
        elif current1.x > current1.parent.x and current1.y == current1.parent.y:
            dir_array1.append(1)  # phai
        current1 = current1.parent
    for i in range(rows):
        for j in range(cols):
            matrix[i][j].parent = []
            matrix[i][j].f = 0
            matrix[i][j].h = 0
            matrix[i][j].g = 0
    return dir_array1


matrix = [[Node(x, y) for y in range(cols)] for x in range(rows)]
for i in range(rows):
    for j in range(cols):
        matrix[i][j].add_neighbors()
snake = [matrix[round(rows / 2)][round(cols / 2)]]
food = matrix[randint(0, rows - 1)][randint(0, cols - 1)]
current = snake[-1]
path = A_star(food, snake)
food_array = [food]

while run:
    clock.tick(12)
    screen.fill(BLACK)
    direction = path.pop(-1)
    if direction == 0:  # xuong
        snake.append(matrix[current.x][current.y + 1])
    elif direction == 1:  # right
        snake.append(matrix[current.x + 1][current.y])
    elif direction == 2:
        snake.append(matrix[current.x][current.y - 1])
    elif direction == 3:
        snake.append(matrix[current.x - 1][current.y])
    current = snake[-1]  # Tinh kc tu diem cuoi dung

    # Xu ly khi con ran den duoc thuc an --> Chon vi tri thuc an moi
    if current.x == food.x and current.y == food.y:
        while True:
            food = matrix[randint(0, rows - 1)][randint(0, cols - 1)]
            print("Sinh thuc an")
            if not (food.obstrucle or food in snake):
                # neu vi tri thuc an khong phai chuong ngai vat VA khong nam trong con ran thi thoat vong while
                score += 1
                break
        food_array.append(food)
        path = A_star(food, snake)
    # Xử lý khi con rắn chưa đến được thức ăn:
    else:
        snake.pop(0)

    # vẽ
    screen.blit(backGround_img, (0, 0))
    for Node in snake:
        Node._update_ui(screen,body_img,25, 25)
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j].obstrucle:
                matrix[i][j]._update_ui(screen,boom_img,25, 25)

    food._update_ui(screen,ball_img,25, 25)
    snake[-1]._update_ui(screen,head_img,25, 25)

    # Display score on the screen
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, WHITE)

    screen.blit(text, (10, 10))
    display.flip()  # Cap nhat man hinh hien thi
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        elif event.type == KEYDOWN:
            if event.key == K_w and not direction == 0:
                direction = 2
            elif event.key == K_a and not direction == 1:
                direction = 3
            elif event.key == K_s and not direction == 2:
                direction = 0
            elif event.key == K_d and not direction == 3:
                direction = 1
