import pygame
import os
from random import choice
from copy import deepcopy

# я искренне прошу прощения за то, что написал такую хрень


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


WIDTH, HEIGHT = 870, 950

color = pygame.Color("black")
shapes = ["S", "Z", "T", "I", "L", "J", "O"]
signs = "sziojlt"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((0, 0, 0))

LEVEL = 1
LINES = 0

clock = pygame.time.Clock()
T = 0
V = 30
FPS = 60


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():

    global LEVEL, T

    fon = pygame.transform.scale(load_image('fon3.jpg'), (WIDTH, HEIGHT - 450))
    screen.blit(fon, (0, 450))
    font = pygame.font.Font(None, 200)

    pygame.draw.rect(screen, (150, 150, 150), (200, 120, 500, 200))
    pygame.draw.rect(screen, (100, 100, 100), (200, 120, 500, 200), 5)
    start_btn = font.render("Start", 1, (100, 100, 100))
    intro_rect = start_btn.get_rect()
    intro_rect.x = 300
    intro_rect.y = 155
    screen.blit(start_btn, intro_rect)

    right_arrow = load_image("arrow-png-icon.png")
    screen.blit(right_arrow, (500, 350, 100, 100))
    left_arrow = pygame.transform.rotate(right_arrow, 180)
    screen.blit(left_arrow, (300, 347, 100, 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] in range(200, 700) \
                    and event.pos[1] in range(120, 320):
                return  # начинаем игру
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] in range(500, 600) \
                    and event.pos[1] in range(350, 450) and LEVEL + 1 <= 5:
                LEVEL += 1
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] in range(300, 400) \
                    and event.pos[1] in range(350, 450) and LEVEL - 1 >= 1:
                LEVEL -= 1
        pygame.draw.rect(screen, (0, 0, 0), (400, 350, 100, 100))
        screen.blit(pygame.font.Font(None, 150).render(str(LEVEL), 1, (100, 100, 100)), (420, 350, 100, 100))
        pygame.display.flip()
        clock.tick(FPS)


start_screen()


class Board:
    # создание поля

    def __init__(self, width, height, shape_center_pos):
        self.width = width
        self.height = height
        self.board = [["."] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.end = False

        self.bgcolor = (0, 0, 0)
        self.border_color = (100, 80, 0)

        self.show_grid = True
        self.show_border = 0

        self.cur_shape = choice(shapes)
        self.next_shape = choice(shapes)
        self.rot_state = 0

        self.shape_center = shape_center_pos
        self.cur_shape_center = None
        self.create_shape()

        self.score = 0
        self.lines = 0

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def can_create_shape(self):
        x = self.shape_center[1]
        y = self.shape_center[0]
        if self.next_shape == "T":
            if self.board[y][x - 1] in signs or self.board[y][x] in signs or self.board[y][x + 1] in signs \
                    or self.board[y + 1][x] in signs:
                return False
        elif self.next_shape == "O":
            if self.board[y + 1][x + 1] in signs or self.board[y][x] in signs or self.board[y][x + 1] in signs \
                    or self.board[y + 1][x] in signs:
                return False
        elif self.next_shape == "I":
            if self.board[y][x - 1] in signs or self.board[y][x] in signs or self.board[y][x + 1] in signs \
                    or self.board[y + 2][x] in signs:
                return False
        elif self.next_shape == "Z":
            if self.board[y][x - 1] in signs or self.board[y][x] in signs or self.board[y + 1][x + 1] in signs \
                    or self.board[y + 1][x] in signs:
                return False
        elif self.next_shape == "S":
            if self.board[y + 1][x - 1] in signs or self.board[y][x] in signs or self.board[y][x + 1] in signs \
                    or self.board[y + 1][x] in signs:
                return False
        elif self.next_shape == "L":
            if self.board[y][x - 1] in signs or self.board[y][x] in signs or self.board[y][x + 1] in signs \
                    or self.board[y + 1][x - 1] in signs:
                return False
        elif self.next_shape == "J":
            if self.board[y][x - 1] in signs or self.board[y][x] in signs or self.board[y][x + 1] in signs \
                    or self.board[y + 1][x + 1] in signs:
                return False
        return True

    def create_shape(self):
        self.cur_shape = self.next_shape
        x = self.shape_center[1]
        y = self.shape_center[0]
        if not self.can_create_shape():
            self.end = True
        if self.cur_shape == "T":
            self.board[y][x - 1] = self.board[y][x] = self.board[y][x + 1] = self.board[y + 1][x] = "t'"
        elif self.cur_shape == "O":
            self.board[y][x] = self.board[y][x + 1] = self.board[y + 1][x] = self.board[y + 1][x + 1] = "o'"
        elif self.cur_shape == "I":
            self.board[y][x - 1] = self.board[y][x] = self.board[y][x + 1] = self.board[y][x + 2] = "i'"
        elif self.cur_shape == "Z":
            self.board[y][x - 1] = self.board[y][x] = self.board[y + 1][x] = self.board[y + 1][x + 1] = "z'"
        elif self.cur_shape == "S":
            self.board[y][x] = self.board[y][x + 1] = self.board[y + 1][x - 1] = self.board[y + 1][x] = "s'"
        elif self.cur_shape == "L":
            self.board[y][x - 1] = self.board[y][x] = self.board[y][x + 1] = self.board[y + 1][x - 1] = "l'"
        elif self.cur_shape == "J":
            self.board[y][x - 1] = self.board[y][x] = self.board[y][x + 1] = self.board[y + 1][x + 1] = "j'"

        self.rot_state = 0
        self.cur_shape_center = self.shape_center.copy()

        self.next_shape = choice(shapes)

    def render(self):
        pygame.draw.rect(screen, self.bgcolor,
                         (self.left, self.top, self.width * self.cell_size, self.height * self.cell_size))
        if self.show_grid:
            for x in range(self.left, self.width * self.cell_size + self.left, self.cell_size):
                for y in range(self.top, self.height * self.cell_size + self.top, self.cell_size):
                    a = self.board[int((y - self.top) / self.cell_size)][int((x - self.left) / self.cell_size)]
                    if "t" in a:
                        image = load_image("red_tile.png")
                        screen.blit(image, (x, y))
                    elif "o" in a:
                        image = load_image("green_tile.png")
                        screen.blit(image, (x, y))
                    elif "i" in a:
                        image = load_image("dark_blue_tile.png")
                        screen.blit(image, (x, y))
                    elif "z" in a:
                        image = load_image("yellow_tile.png")
                        screen.blit(image, (x, y))
                    elif "s" in a:
                        image = load_image("purple_tile.png")
                        screen.blit(image, (x, y))
                    elif "l" in a:
                        image = load_image("blue_tile.png")
                        screen.blit(image, (x, y))
                    elif "j" in a:
                        image = load_image("orange_tile.png")
                        screen.blit(image, (x, y))
                    pygame.draw.rect(screen, self.border_color, (x, y, self.cell_size, self.cell_size), 1)
            return

        if self.show_border:
            pygame.draw.rect(screen, self.border_color,
                             (self.left, self.top, self.width * self.cell_size, self.height * self.cell_size), 5)

    def down_motion(self):
        board_copy = deepcopy(self.board)
        for x in range(self.width):
            for y in range(self.height - 1, -1, -1):
                if "'" in self.board[y][x] and y + 1 in range(self.height) \
                        and self.board[y + 1][x] not in signs:
                    board_copy[y][x] = "."
                    board_copy[y + 1][x] = self.board[y][x]
                elif "'" not in self.board[y][x]:
                    pass
                else:
                    return self.collision()
        self.score += LEVEL
        self.cur_shape_center[0] += 1
        self.board = board_copy

    def horizontal_motion(self, direction):
        board_copy = deepcopy(self.board)
        if direction == "r":
            for x in range(self.width - 1, -1, -1):
                for y in range(self.height):
                    if "'" in self.board[y][x] and x + 1 in range(self.width)\
                            and self.board[y][x + 1] not in signs:
                        board_copy[y][x] = "."
                        board_copy[y][x + 1] = self.board[y][x]
                    elif "'" not in self.board[y][x]:
                        pass
                    else:
                        return
            self.cur_shape_center[1] += 1

        elif direction == "l":
            for x in range(self.width):
                for y in range(self.height):
                    if "'" in self.board[y][x] and x - 1 in range(self.width)\
                            and self.board[y][x - 1] not in signs:
                        board_copy[y][x] = "."
                        board_copy[y][x - 1] = self.board[y][x]
                    elif "'" not in self.board[y][x]:
                        pass
                    else:
                        return
            self.cur_shape_center[1] -= 1
        self.board = board_copy

    def rotation(self):
        x = self.cur_shape_center[1]
        y = self.cur_shape_center[0]
        if self.cur_shape == "T":
            if self.rot_state == 0:
                if y - 1 in range(self.height) and self.board[y - 1][x] not in signs:
                    self.board[y - 1][x] = "t'"
                    self.board[y][x + 1] = "."
                    self.rot_state = 1
            elif self.rot_state == 1:
                if x + 1 in range(self.width) and self.board[y][x + 1] not in signs:
                    self.board[y + 1][x] = "."
                    self.board[y][x + 1] = "t'"
                    self.rot_state = 2
            elif self.rot_state == 2:
                if y + 1 in range(self.height) and self.board[y + 1][x] not in signs:
                    self.board[y][x - 1] = "."
                    self.board[y + 1][x] = "t'"
                    self.rot_state = 3
            elif self.rot_state == 3:
                if x - 1 in range(self.width) and self.board[y][x - 1] not in signs:
                    self.board[y - 1][x] = "."
                    self.board[y][x - 1] = "t'"
                    self.rot_state = 0
        elif self.cur_shape == "I":
            if self.rot_state == 0:
                if y - 1 in range(self.height) and y + 2 in range(self.height) and \
                        self.board[y - 1][x] not in signs and self.board[y + 1][x] not in signs and \
                        self.board[y + 2][x] not in signs:
                    self.board[y][x - 1] = self.board[y][x + 1] = self.board[y][x + 2] = "."
                    self.board[y - 1][x] = self.board[y + 1][x] = self.board[y + 2][x] = "i'"
                    self.rot_state = 1
            elif self.rot_state == 1:
                if all([x - 1 in range(self.width), x + 2 in range(self.width)]) and \
                        self.board[y][x - 1] not in signs and self.board[y][x + 1] not in signs and \
                        self.board[y][x + 2] not in signs:
                    self.board[y - 1][x] = self.board[y + 1][x] = self.board[y + 2][x] = "."
                    self.board[y][x - 1] = self.board[y][x + 1] = self.board[y][x + 2] = "i'"
                    self.rot_state = 0
        elif self.cur_shape == "Z":
            if self.rot_state == 0:
                if y - 1 in range(self.height) and self.board[y][x + 1] not in signs and \
                        self.board[y - 1][x + 1] not in signs:
                    self.board[y + 1][x + 1] = self.board[y][x - 1] = "."
                    self.board[y][x + 1] = self.board[y - 1][x + 1] = "z'"
                    self.rot_state = 1
            elif self.rot_state == 1:
                if x - 1 in range(self.width) and self.board[y][x - 1] not in signs and \
                        self.board[y + 1][x + 1] not in signs:
                    self.board[y][x + 1] = self.board[y - 1][x + 1] = "."
                    self.board[y + 1][x + 1] = self.board[y][x - 1] = "z'"
                    self.rot_state = 0
        elif self.cur_shape == "S":
            if self.rot_state == 0:
                if y - 1 in range(self.height) and self.board[y][x - 1] not in signs and \
                        self.board[y - 1][x - 1] not in signs:
                    self.board[y][x + 1] = self.board[y + 1][x - 1] = "."
                    self.board[y][x - 1] = self.board[y - 1][x - 1] = "s'"
                    self.rot_state = 1
            elif self.rot_state == 1:
                if x + 1 in range(self.width) and self.board[y][x + 1] not in signs and \
                        self.board[y + 1][x - 1] not in signs:
                    self.board[y][x - 1] = self.board[y - 1][x - 1] = "."
                    self.board[y][x + 1] = self.board[y + 1][x - 1] = "s'"
                    self.rot_state = 0
        elif self.cur_shape == "L":
            if self.rot_state == 0:
                if y - 1 in range(self.height) and self.board[y + 1][x] not in signs and \
                        self.board[y - 1][x] not in signs and self.board[y - 1][x - 1] not in signs:
                    self.board[y][x - 1] = self.board[y][x + 1] = self.board[y + 1][x - 1] = "."
                    self.board[y - 1][x - 1] = self.board[y - 1][x] = self.board[y + 1][x] = "l'"
                    self.rot_state = 1
            elif self.rot_state == 1:
                if x + 1 in range(self.width) and self.board[y][x - 1] not in signs and \
                        self.board[y][x + 1] not in signs and self.board[y - 1][x + 1] not in signs:
                    self.board[y - 1][x - 1] = self.board[y - 1][x] = self.board[y + 1][x] = "."
                    self.board[y][x - 1] = self.board[y][x + 1] = self.board[y - 1][x + 1] = "l'"
                    self.rot_state = 2
            elif self.rot_state == 2:
                if y + 1 in range(self.height) and self.board[y - 1][x] not in signs and \
                        self.board[y + 1][x] not in signs and self.board[y + 1][x + 1] not in signs:
                    self.board[y][x - 1] = self.board[y][x + 1] = self.board[y - 1][x + 1] = "."
                    self.board[y - 1][x] = self.board[y + 1][x] = self.board[y + 1][x + 1] = "l'"
                    self.rot_state = 3
            elif self.rot_state == 3:
                if x - 1 in range(self.width) and self.board[y][x - 1] not in signs and \
                        self.board[y + 1][x - 1] not in signs and self.board[y][x + 1] not in signs:
                    self.board[y - 1][x] = self.board[y + 1][x] = self.board[y + 1][x + 1] = "."
                    self.board[y][x - 1] = self.board[y + 1][x - 1] = self.board[y][x + 1] = "l'"
                    self.rot_state = 0
        elif self.cur_shape == "J":
            if self.rot_state == 0:
                if y - 1 in range(self.height) and self.board[y - 1][x] not in signs and \
                        self.board[y + 1][x] not in signs and self.board[y + 1][x - 1] not in signs:
                    self.board[y][x - 1] = self.board[y][x + 1] = self.board[y + 1][x + 1] = "."
                    self.board[y - 1][x] = self.board[y + 1][x] = self.board[y + 1][x - 1] = "j'"
                    self.rot_state = 1
            elif self.rot_state == 1:
                if x + 1 in range(self.width) and self.board[y - 1][x - 1] not in signs and \
                        self.board[y][x - 1] not in signs and self.board[y][x + 1] not in signs:
                    self.board[y - 1][x] = self.board[y + 1][x] = self.board[y + 1][x - 1] = "."
                    self.board[y - 1][x - 1] = self.board[y][x + 1] = self.board[y][x - 1] = "j'"
                    self.rot_state = 2
            elif self.rot_state == 2:
                if y + 1 in range(self.height) and self.board[y - 1][x] not in signs and \
                        self.board[y - 1][x + 1] not in signs and self.board[y + 1][x] not in signs:
                    self.board[y - 1][x - 1] = self.board[y][x + 1] = self.board[y][x - 1] = "."
                    self.board[y - 1][x] = self.board[y + 1][x] = self.board[y - 1][x + 1] = "j'"
                    self.rot_state = 3
            elif self.rot_state == 3:
                if x - 1 in range(self.width) and self.board[y][x - 1] not in signs and \
                        self.board[y][x + 1] not in signs and self.board[y + 1][x + 1] not in signs:
                    self.board[y - 1][x] = self.board[y + 1][x] = self.board[y - 1][x + 1] = "."
                    self.board[y + 1][x + 1] = self.board[y][x + 1] = self.board[y][x - 1] = "j'"
                    self.rot_state = 0

    def collision(self):
        for x in range(self.width):
            for y in range(self.height):
                if "'" in self.board[y][x]:
                    self.board[y][x] = self.board[y][x][0]

        self.score += LEVEL * 10
        self.cleaning()
        self.create_shape()

    def cleaning(self):
        count_of_lines = 0
        for y in range(self.height):
            a = 0
            for x in range(self.width):
                if self.board[y][x] in signs:
                    a += 1
                else:
                    a += 0
                    break

                if a == self.width:
                    self.board[y] = ["."] * self.width
                    for i in range(y, -1, -1):
                        if i == 0:
                            self.board[i] = ["."] * self.width
                            self.lines += 1
                            count_of_lines += 1
                        else:
                            self.board[i] = self.board[i - 1]
        self.score += count_of_lines ** 2 * LEVEL * 25

    def clear(self):
        self.board = [["."] * self.width for _ in range(self.height)]


board = Board(10, 18, [0, 4])
board.set_view(30, 30, 50)

shape_table = Board(6, 4, [1, 2])
shape_table.set_view(550, 30, 50)
shape_table.clear()


def main():
    global T
    running = True
    font = pygame.font.Font(None, 100)
    level_txt = font.render(f"Level: {LEVEL}", 1, (255, 255, 255))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                board.horizontal_motion("r")
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                board.horizontal_motion("l")
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_w):
                board.rotation()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                board.down_motion()
                board.score += 1
        score = board.score
        lines = board.lines
        score_txt = font.render("Score:", 1, (255, 255, 255))
        lines_txt = font.render(f"Lines:{lines}", 1, (255, 255, 255))
        screen.fill(color)
        board.render()
        shape_table.next_shape = board.next_shape
        shape_table.clear()
        shape_table.create_shape()
        shape_table.render()
        screen.blit(level_txt, (570, 270, 300, 100))
        screen.blit(score_txt, (570, 390, 300, 100))
        screen.blit(font.render(str(score), 1, (255, 255, 255)), (570, 510, 300, 100))
        screen.blit(lines_txt, (570, 630, 300, 100))
        if board.end:
            return
        if LEVEL == 1 and round(T) == 12:
            board.down_motion()
            T = 0
        elif LEVEL == 2 and round(T) == 9:
            board.down_motion()
            T = 0
        elif LEVEL == 3 and round(T) == 7:
            board.down_motion()
            T = 0
        elif LEVEL == 4 and round(T) == 5:
            board.down_motion()
            T = 0
        elif LEVEL == 5 and round(T) == 4:
            board.down_motion()
            T = 0
        T += V / FPS
        clock.tick(FPS)
        pygame.display.flip()


main()


def ending():
    screen.fill((0, 0, 0))
    fon = pygame.transform.scale(load_image('fon3.jpg'), (WIDTH, HEIGHT - 450))
    screen.blit(fon, (0, 450))

    font = pygame.font.Font(None, 100)
    score = board.score
    lines = board.lines

    score_txt = font.render(f"Score: {score}", 1, (255, 255, 255))
    lines_txt = font.render(f"Lines: {lines}", 1, (255, 255, 255))
    level_txt = font.render(f"Level: {LEVEL}", 1, (255, 255, 255))

    screen.blit(score_txt, (300, 30, 300, 100))
    screen.blit(lines_txt, (300, 150, 300, 100))
    screen.blit(level_txt, (300, 270, 300, 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


ending()
pygame.quit()
