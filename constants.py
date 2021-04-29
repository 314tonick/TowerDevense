from tower import StoneTowerFirstType, StoneTowerSecondType, StoneTowerThirdType
from utils import resource_path


def get_levels():
    f = open(resource_path('levels.txt'))
    le = []
    for line in f.readlines():
        le.append(Level(*eval(line)))
    f.close()
    return le


class Level:
    def __init__(self, waves, lives, coins, onThree, onTwo, onOne, coinsOneStar, coinsTwoStar, coinsThreeStar, ifLost):
        self.onOne = onOne
        self.onTwo = onTwo
        self.onThree = onThree
        self.coins = coins
        self.lives = lives
        self.waves = waves
        self.getCoins = [coinsOneStar, coinsTwoStar, coinsThreeStar]
        self.ifLost = ifLost

    def reset(self):
        for wave in self.waves:
            wave.reset()


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

    def reset(self):
        self.i = 0

    def next(self):
        if self.i == len(self.heroes):
            raise StopIteration
        else:
            self.i += 1
            return self.paths[self.i - 1], self.heroes[self.i - 1], self.speed, self.lives[self.i - 1], self.fines[
                self.i - 1], self.rewards[self.i - 1]


LENGTH_OF_FREEZE = 50
FREEZE_COST = 50
WIDTH = 1160
HEIGHT = 700
HERO_WIDTH = HERO_HEIGHT = 100
WAIT_BETWEEN_WAVES = 100
SCORPION, OLD_MAN, GOBLIN = 'scorpion', 'oldMan', 'goblin'
STONE_TOWER_CLASSES = [StoneTowerFirstType, StoneTowerSecondType, StoneTowerThirdType]
PRICES = [[50, 20, 30, 25], [90, 30, 50, 45], [150, 50, 100, 75]]
LIVES_ON_HELP = 5
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
COINS = 1000
TOWER_WIDTH, TOWER_HEIGHT = 0.8, 0.8
TOWER_SPEED = 0.4
LEVELS = get_levels()
NUMBER_OF_LEVELS = len(LEVELS)
print(NUMBER_OF_LEVELS)