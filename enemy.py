import pygame
from constants import HERO_WIDTH, HERO_HEIGHT
import math


class Enemy:
    def __init__(self, imgs, screen, path, name, speed, lives, fine, reward):
        self.fine = fine
        self.reward = reward
        self.lives_start = lives
        self.lives = lives
        self.speed = speed
        self.doshel = False
        self.path = path
        self.name = name
        self.now_uron = 0
        self.x, self.y = path[0][0], path[0][1]
        self.imgs = imgs
        self.screen = screen
        self.counter = 0
        self.width = HERO_WIDTH
        self.height = HERO_HEIGHT
        self.pos = 0
        self.looking_left = False

    def get_pos(self, ticks):
        pos = self.pos
        x, y = self.x, self.y
        # ----------------------------------
        for _ in range(ticks):
            try:
                x1, y1 = self.path[pos]
                x2, y2 = self.path[pos + 1]
            except IndexError:
                return x, y
            dir_x, dir_y = x2 - x1, y2 - y1
            len_dir = math.sqrt(dir_x * dir_x + dir_y * dir_y)
            dir_x /= len_dir
            dir_y /= len_dir

            x += dir_x * self.speed
            y += dir_y * self.speed
            if dir_x >= 0 >= dir_y:
                if x >= x2 and y <= y2:
                    pos += 1
            if dir_x >= 0 and dir_y >= 0:
                if x >= x2 and y >= y2:
                    pos += 1
            if dir_x <= 0 and dir_y <= 0:
                if x <= x2 and y <= y2:
                    pos += 1
            if dir_x <= 0 <= dir_y:
                if x <= x2 and y >= y2:
                    pos += 1
        return x+self.width//2, y+self.height//2

    def draw(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.width, 10))
        pygame.draw.rect(self.screen, (255, 0, 0), (self.x + 1, self.y + 1, self.width - 2, 8))
        pygame.draw.rect(self.screen, (0, 255, 0), (self.x + 1, self.y + 1, (self.width - 2) * self.lives // self.lives_start, 8))
        if self.looking_left:
            self.screen.blit(pygame.transform.flip(self.imgs[self.counter], True, False),
                             (self.x, self.y))
        else:
            self.screen.blit(self.imgs[self.counter], (self.x, self.y))

    def move(self):  # или update
        x1, y1 = self.path[self.pos]
        try:
            x2, y2 = self.path[self.pos + 1]
        except IndexError:
            self.doshel = True
            return True if not self.doshel else None

        dir_x, dir_y = x2 - x1, y2 - y1
        len_dir = math.sqrt(dir_x * dir_x + dir_y * dir_y)
        dir_x /= len_dir
        dir_y /= len_dir

        self.x += dir_x * self.speed
        self.y += dir_y * self.speed
        if dir_x >= 0 >= dir_y:
            if self.x >= x2 and self.y <= y2:
                self.pos += 1
        if dir_x >= 0 and dir_y >= 0:
            if self.x >= x2 and self.y >= y2:
                self.pos += 1
        if dir_x <= 0 and dir_y <= 0:
            if self.x <= x2 and self.y <= y2:
                self.pos += 1
        if dir_x <= 0 <= dir_y:
            if self.x <= x2 and self.y >= y2:
                self.pos += 1

        if dir_x < 0:
            self.looking_left = True
        elif dir_x > 0:
            self.looking_left = False
        self.counter = (self.counter + 1) % len(self.imgs)
        if self.pos == len(self.path) - 2:
            doshel = self.doshel
            self.doshel = True
            return True if not doshel else None
