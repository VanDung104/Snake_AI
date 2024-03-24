import sys
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

paused = False
menu_options = ["Start", "Quit"]
menu_options1 = ["Continue", "Quit"]
menu_text = pygame.font.Font(None, 30).render("Snake Game", True, WHITE)

cols = 25
rows = 25

width = 700
height = 700
# đồ họa game
backGround_img = pygame.image.load('bg.png')
backGround_img = pygame.transform.scale(backGround_img, (width, height))
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
wr = width/cols
hr = height/rows
direction = 1

screen = display.set_mode([width, height])
display.set_caption("snake_self")
clock = time.Clock()


def display_menu(screen, menu_text, options):
    background_img = pygame.image.load('menu_img-13302.png')  # Đường dẫn tới tệp ảnh nền
    background_img = pygame.transform.scale(background_img,(width, height))  # Đổi kích thước ảnh nền cho phù hợp với màn hình
    """Display the menu with given text and options."""
    font = pygame.font.Font(None, 36)
    menu_items = [font.render(text, True, WHITE) for text in options]
    menu_rects = [item.get_rect(center=(width // 2, (height // 2) + index * 50)) for index, item in enumerate(menu_items)]

    screen.blit(background_img, (0, 0))  # Vẽ ảnh nền lên màn hình
    screen.blit(menu_text, (width // 2 - menu_text.get_width() // 2, height // 4 - menu_text.get_height() // 2))
    for item, rect in zip(menu_items, menu_rects):
        screen.blit(item, rect)
    pygame.display.flip()

def menu(screen, menu_text, options):
    """Display menu and handle player input."""
    display_menu(screen, menu_text, options)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return options.index("Start")  # Start the game
                elif event.key == pygame.K_q:
                    pygame.quit()
                elif event.key == pygame.K_SPACE:
                    return options.index("Continue")  # Start the game
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

while True:
    menu_choice = menu(screen, menu_text, menu_options)
    if menu_options[menu_choice] == "Start":
        break
    elif menu_options[menu_choice] == "Quit":
        pygame.quit()
        sys.exit()

while run:
    if not paused:
        clock.tick(30)
        #screen.fill(BLACK)
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
                # Sinh ra một vị trí ngẫu nhiên cho thức ăn
                new_food_x = randint(0, rows - 1)
                new_food_y = randint(0, cols - 1)
                new_food = matrix[new_food_x][new_food_y]

                # Kiểm tra xem vị trí mới có phải là chướng ngại vật hoặc nằm trên cơ thể của con rắn không
                if not (new_food.obstrucle or new_food in snake):
                    # Kiểm tra khoảng cách từ vị trí mới của thức ăn đến mỗi phần của con rắn
                    too_close = False
                    for segment in snake:
                        distance = sqrt((new_food.x - segment.x) ** 2 + (new_food.y - segment.y) ** 2)
                        if distance < 3:  # Nếu vị trí mới quá gần với bất kỳ phần nào của con rắn
                            too_close = True
                            break

                    # Nếu vị trí mới đủ xa cả chướng ngại vật và cơ thể của con rắn
                    if not too_close:
                        score += 1
                        print(score)
                        food = new_food  # Cập nhật vị trí mới của thức ăn
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
    else:
        menu_choice = menu(screen, menu_text, menu_options1)
        if menu_options[menu_choice] == "Start":
                paused = False
        elif menu_options[menu_choice] == "Quit":
            pygame.quit()
            sys.exit()

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
            elif event.key == pygame.K_SPACE:
                paused = not paused
