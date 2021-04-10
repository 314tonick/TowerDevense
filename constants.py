from tower import StoneTowerFirstType, StoneTowerSecondType, StoneTowerThirdType


class Wave:
    def __init__(self, heroes, paths, lives, speed, wait_in, fines, rewards):
        self.wait = wait_in
        self.speed = speed
        self.lives = lives
        self.paths = paths
        self.heroes = heroes
        self.fines = fines
        self.rewards = rewards
        self.i = 0

    def next(self):
        if self.i == len(self.heroes):
            raise StopIteration
        else:
            self.i += 1
            return self.paths[self.i - 1], self.heroes[self.i - 1], self.speed, self.lives[self.i - 1], self.fines[
                self.i - 1], self.rewards[self.i - 1]


WIDTH = 1160
HEIGHT = 700
HERO_WIDTH = HERO_HEIGHT = 100
WAIT_BETWEEN_WAVES = 100
SCORPION, OLD_MAN, GOBLIN = 'scorpion', 'oldMan', 'goblin'
STONE_TOWER_CLASSES = [StoneTowerFirstType, StoneTowerSecondType, StoneTowerThirdType]
WAVES = [
    Wave([SCORPION] * 5, [1] * 5, [10] * 5, 1.3, 100, [1] * 5, [10] * 5),
    Wave([SCORPION] * 10, [0, 1, 2] * 4, [10, 20, 30, 40, 50] * 2, 1.7, 100, [1, 2] * 5, [10, 15, 20] * 4),
    Wave([SCORPION], [1], [200], 1, 1, [10], [50]),
    Wave([OLD_MAN] * 5, [1] * 5, [20] * 5, 1.3, 90, [2] * 5, [30] * 5),
    Wave([SCORPION, OLD_MAN] * 5, [0, 1, 2] * 4, [20, 30, 40, 50] * 3, 1.5, 130, [2, 3] * 5, [20, 30, 40] * 5),
    Wave([SCORPION, OLD_MAN], [0, 2], [300, 300], 1.2, 1, [10], [70])
]
LIVES = 20
PRICES = [[50, 20, 30, 25], [90, 30, 50, 45], [150, 50, 100, 75]]
DELAY = 4
STONE_TOWER = 'stone_tower'
STONE_TOWER_IMG = [
    [['1.png', '2.png', '3.png'], ['1.png', '2.png', '6.png'], ['4.png', '5.png', '7.png']],
    [['8.png', '9.png', '12.png'], ['8.png', '9.png', '13.png'], ['10.png', '11.png', '14.png']],
    [['20.png', '21.png', '15.png'], ['22.png', '23.png', '16.png'], ['18.png', '19.png', '17.png']]
]
STONE_IMGS = [
    ['29.png', ['30.png', '31.png', '32.png', '33.png', '34.png']],
    ['35.png', ['36.png', '37.png', '38.png', '39.png']],
    # ['29.png', ['30.png', '31.png', '32.png', '33.png', '34.png']],
    ['40.png', ['41.png', '42.png', '43.png', '44.png']],
]
STONE_TOWERS = [
    {'type_': 0, 'uron': 10, 'speed': 0.4, 'range_': 150},
    # {'type_': 1, 'uron': 10, 'speed': 0.3, 'range_': 200},
    {'type_': 1, 'uron': 20, 'speed': 0.5, 'range_': 180},
    {'type_': 2, 'uron': 35, 'speed': 0.6, 'range_': 220},
]
COINS = 100
TOWER_WIDTH, TOWER_HEIGHT = 0.8, 0.8
TOWER_SPEED = 0.4
