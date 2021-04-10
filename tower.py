from utils import *
import pygame

# from constants import SELL_IMG, UPGRADE_IMG - I commented this because, it throws the ImportError

UPGRADE_IMG = 'buttons', 'upgrade.png'
SELL_IMG = 'buttons', 'sell.png'
COST_IMG = 'buttons', 'cost.png'
PRICES = [[50, 20, 30, 25], [90, 30, 50, 45], [150, 50, 100, 75]]


class Tower:
    def __bool__(self):
        return True

    def __init__(self, x, y, imgs):
        self.x = x
        self.y = y
        self.level = 0
        self.imgs = imgs

    def draw(self, screen):
        pass

    def update(self):
        pass

    def upgrade(self):
        self.level += 1


class UnionElements:
    def __init__(self, *elements):
        self.elements = elements

    def draw(self, screen):
        for e in self.elements:
            e.draw(screen)


class StoneTower(Tower):
    def __init__(self, x, y, imgs_tower, stone_img, stone_imgs, range_, uron, speed, type_, do_try=True):  # imgs_stn):
        super().__init__(x, y, imgs_tower)
        if do_try:
            self.costs = PRICES[type_]
            self.range = range_
            self.type = type_
            self.speed = speed
            self.stone_imgs = stone_imgs
            self.uron = uron
            self.stone_img = stone_img
            self.pos = self.imgs[self.level][1].get_height() + 20
            self.isDowning = False
            self.ready = True
            self.stones = []
            self.width, self.height = self.imgs[self.level][2].get_size()
            self.upgradeButton = Button(
                pygame.transform.scale(load_img(*UPGRADE_IMG), (50, 50)),
                (range_ * 2 - self.width) // 2, range_ * 2 - (range_ * 2 - self.height) // 2, self.costs[1])
            self.sellButton = Button(pygame.transform.scale(load_img(*SELL_IMG), (50, 50)),
                                     range_ * 2 - (range_ * 2 - self.width) // 2 - 50,
                                     range_ * 2 - (range_ * 2 - self.height) // 2, self.costs[3])

    def attack(self, enemy):
        if self.ready:
            enemy.now_uron += self.uron
            new_x, new_y = enemy.get_pos(100)
            self.stones.append(
                Stone(self.x + 35, self.y + 43, new_x, new_y, self.stone_img,
                      self.stone_imgs, 95))
            self.stones[-1].enemy = enemy
            self.stones[-1].isOnTower = True
            self.ready = False
            return True
        return False

    def update(self):
        return_ = []
        for stone in self.stones[::-1]:
            if stone.isOnTower:
                stone.y -= self.speed
                if self.y >= stone.y:
                    stone.start_x_y = (self.x, self.y)
                    stone.isOnTower = False
                    stone.vx = (stone.goal_x - stone.x) / stone.tick_all
                    stone.vy = (stone.goal_y - stone.y - stone.ay * stone.tick_all * stone.tick_all / 2) / \
                               stone.tick_all
            else:
                if not stone.update():
                    return_.append(stone.enemy)
                    self.stones.remove(stone)
        if not self.ready:
            self.pos += self.speed if self.isDowning else -self.speed

        if self.pos <= 0:
            self.isDowning = True
        elif self.pos >= self.imgs[self.level][1].get_height() + 20:
            self.ready = True
            self.isDowning = False
        return return_
        # self.pos += TOWER_SPEED if self.isDowning else -TOWER_SPEED

    def draw(self, screen):
        screen.blit(self.imgs[self.level][0], (self.x, self.y + self.pos))
        for stn in self.stones:
            if stn.isOnTower:
                stn.draw(screen)
        screen.blit(self.imgs[self.level][2], (self.x, self.y))
        screen.blit(self.imgs[self.level][1], (self.x, self.y + self.pos + self.imgs[self.level][0].get_height() - 2))
        for stn in self.stones:
            if not stn.isOnTower:
                stn.draw(screen)

    def upgrade(self):
        super(StoneTower, self).upgrade()
        self.speed += 0.15
        self.uron += 10
        self.range += 30
        self.upgradeButton = Button(
            pygame.transform.scale(load_img(*UPGRADE_IMG), (50, 50)), (self.range * 2 - self.width) // 2,
            self.range * 2 - (self.range * 2 - self.height) // 2, self.costs[self.level + 1] if self.level < 2 else 0)
        self.sellButton = Button(pygame.transform.scale(load_img(*SELL_IMG), (50, 50)),
                                 self.range * 2 - (self.range * 2 - self.width) // 2 - 50,
                                 self.range * 2 - (self.range * 2 - self.height) // 2, self.costs[3])

    def draw_circle(self, screen):
        radius = self.range
        surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (80, 80, 80, 100), (radius, radius), radius, 0)
        self.draw_buttons(surface)
        screen.blit(surface, (self.x + self.width // 2 - radius, self.y + self.height // 2 - radius))

    def draw_buttons(self, screen):
        self.upgradeButton.draw(screen)
        self.sellButton.draw(screen)


class SupportTower(Tower):
    def __init__(self, x, y, imgs):
        super().__init__(x, y, imgs)


class Stone:
    def __init__(self, x, y, goal_x, goal_y, img, explosion_imgs, ticks):
        self.explosion_imgs = []
        for image_ in explosion_imgs:
            for _ in range(5):
                self.explosion_imgs.append(image_)
        # self.explosion_imgs = explosion_imgs
        self.vx, self.vy, self.ay, self.tick_all, self.tick = 0, 0, 0.02, ticks, 0
        self.img = img
        self.goal_y = goal_y
        self.goal_x = goal_x
        self.start_x_y = (x, y)
        self.y = y
        self.x = x
        self.frame = img
        self.is_moving = 0

    def draw(self, screen):
        pygame.draw.circle(screen, (222, 0, 0), (self.goal_x, self.goal_y), 3)
        screen.blit(self.frame, (self.x, self.y))

    def update(self):
        if self.tick < self.tick_all:
            self.vy += self.ay
            self.x += self.vx
            self.y += self.vy
            self.tick += 1
        else:
            try:
                self.is_moving += 1
                self.x += self.frame.get_width() / 2
                self.y += self.frame.get_height() / 2
                self.frame = self.explosion_imgs[self.is_moving - 1]
                self.x -= self.frame.get_width() / 2
                self.y -= self.frame.get_height() / 2

            except IndexError:
                return False
        return True


class Button:
    def __init__(self, img, x, y, cost: int = None):
        self.x, self.y, self.img = x, y, img
        self.width, self.height = self.img.get_size()
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        self.cost_img = pygame.transform.scale(load_img(*COST_IMG), (int(self.width // 1.4), int(self.height // 2.6)))
        self.cost = cost
        self.cost_rect = pygame.rect.Rect(self.x + self.width - self.width / 1.4 + 5,
                                          self.y + self.height - self.height / 2.6 + 3, self.width / 1.4,
                                          self.height / 2.6)

    def draw(self, screen):
        screen.blit(self.img, self.rect)
        if self.cost:
            font_ = pygame.font.Font(resource_path('font.ttf'), self.height // 5)
            screen.blit(self.cost_img, self.cost_rect)
            screen.blit(font_.render(str(self.cost), True, (243, 220, 20)), self.cost_rect.move(self.width // 15, self.height // 15))

    def try_push(self, events, move_x=0, move_y=0, eventTypeRequire=pygame.MOUSEBUTTONUP):
        return self.rect.move(move_x, move_y).collidepoint(*pygame.mouse.get_pos()) and eventTypeRequire in [e.type for
                                                                                                             e in events
                                                                                                             ]


class StoneTowerFirstType(StoneTower):
    def attack(self, enemy):
        if super(StoneTowerFirstType, self).attack(enemy):
            self.stones[-1].goal_x -= 35


class StoneTowerSecondType(StoneTower):
    def attack(self, enemy):
        if super(StoneTowerSecondType, self).attack(enemy):
            self.stones[-1].goal_x -= 35

    def draw(self, screen):
        mx, my = -7.119999999993524, -15
        screen.blit(self.imgs[self.level][0], (self.x - mx, self.y + self.pos))
        y = 22
        x = 8
        for stn in self.stones:
            stn.y -= y
            stn.x += x
            if stn.isOnTower:
                stn.draw(screen)
            stn.x -= x
            stn.y += y
        screen.blit(self.imgs[self.level][2], (self.x, self.y))
        screen.blit(self.imgs[self.level][1],
                    (self.x, my + self.y + self.pos + self.imgs[self.level][0].get_height() - 2))
        for stn in self.stones:
            stn.x += x
            stn.y -= y
            if not stn.isOnTower:
                stn.draw(screen)
            stn.x -= x
            stn.y += y


class StoneTowerThirdType(StoneTower):
    def attack(self, enemy):
        if super(StoneTowerThirdType, self).attack(enemy):
            self.stones[-1].goal_x -= 40
            self.stones[-1].goal_y -= 10

    def draw(self, screen):
        screen.blit(self.imgs[self.level][0], (self.x, self.y + self.pos))
        for stn in self.stones:
            u = 10 * self.level
            if stn.isOnTower:
                stn.y += u
                stn.draw(screen)
                stn.y -= u
        screen.blit(self.imgs[self.level][2], (self.x, self.y))
        screen.blit(self.imgs[self.level][1],
                    (self.x, self.y + self.pos + self.imgs[self.level][0].get_height() - 2 - 5 * bool(self.level) - (
                        2 if self.level else 0)))
        for stn in self.stones:
            u = 10 * self.level
            if not stn.isOnTower:
                stn.y += u
                stn.draw(screen)
                stn.y -= u
